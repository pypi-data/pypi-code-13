# Copyright (c) 2014 Mirantis Inc.
#
# Licensed under the Apache License, Version 2.0 (the License);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an AS IS BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and#
# limitations under the License.
import copy
from itertools import ifilter

from cinderclient.v1 import client as cinder_client
from cinderclient import exceptions as cinder_exc

from cloudferry.lib.base import storage
from cloudferry.lib.os.identity import keystone
from cloudferry.lib.os.storage import filters as cinder_filters
from cloudferry.lib.utils import filters
from cloudferry.lib.utils import log
from cloudferry.lib.utils import mapper
from cloudferry.lib.utils import proxy_client
from cloudferry.lib.utils import retrying
from cloudferry.lib.utils import utils

import re

RE_EXTRACT_HOST = re.compile(r'//([^:^/]*)')

AVAILABLE = 'available'
IN_USE = "in-use"
CINDER_VOLUME = "cinder-volume"
LOG = log.getLogger(__name__)
ID = 'id'
DISPLAY_NAME = 'display_name'
PROJECT_ID = 'project_id'
STATUS = 'status'
TENANT_ID = 'tenant_id'
USER_ID = 'user_id'
DELETED = 'deleted'
HOST = 'host'
IGNORED_TBL_LIST = ('quotas', 'quota_usages')
QUOTA_TABLES = (
    'quotas',
    'quota_classes',
    'quota_usages',
)
SRC = 'src'
TABLE_UNIQ_KEYS = {
    'volumes': ['id'],
    'quotas': ['project_id', 'resource'],
    'quota_classes': ['class_name', 'resource'],
    'quota_usages': ['project_id', 'resource'],
    'reservations': ['project_id', 'resource', 'usage_id'],
    'volume_metadata': ['volume_id', 'key'],
    'volume_glance_metadata': ['volume_id', 'snapshot_id', 'key'],
}

VALID_STATUSES = ['available', 'in-use', 'attaching', 'detaching']
MIGRATED_VOLUMES_METADATA_KEY = 'src_volume_id'


class CinderStorage(storage.Storage):

    """Implements basic functionality around cinder client"""

    def __init__(self, config, cloud):
        super(CinderStorage, self).__init__(config)
        self.ssh_host = config.cloud.ssh_host
        self.mysql_host = config.mysql.db_host \
            if config.mysql.db_host else self.ssh_host
        self.cloud = cloud
        self.identity_client = cloud.resources[utils.IDENTITY_RESOURCE]
        self.mysql_connector = cloud.mysql_connector('cinder')
        self.volume_filter = None
        self.filter_tenant_id = None
        self.tenant_name_map = mapper.Mapper('tenant_map')

    @property
    def cinder_client(self):
        return self.proxy(self.get_client(self.config), self.config)

    def get_client(self, params=None, tenant=None):
        params = params or self.config

        return cinder_client.Client(
            params.cloud.user,
            params.cloud.password,
            tenant or params.cloud.tenant,
            params.cloud.auth_url,
            cacert=params.cloud.cacert,
            insecure=params.cloud.insecure,
            region_name=params.cloud.region,
            endpoint_type=(params.cloud.cinder_endpoint_type or
                           params.cloud.endpoint_type)
        )

    def get_filter(self):
        if self.volume_filter is None:
            with open(self.config.migrate.filter_path, 'r') as f:
                filter_yaml = filters.FilterYaml(f)
                filter_yaml.read()

            self.volume_filter = cinder_filters.CinderFilters(
                self.cinder_client, filter_yaml)

        return self.volume_filter

    def read_info(self, target='volumes', **kwargs):
        if target == 'volumes':
            return self._read_info_volumes(**kwargs)
        if target == 'resources':
            return self._read_info_resources(**kwargs)

    def _read_info_resources(self, **kwargs):
        res = dict()
        self.filter_tenant_id = kwargs.get('tenant_id', None)
        res['quotas'] = self._read_info_quota()
        return res

    def _read_info_volumes(self, **kwargs):
        info = {utils.VOLUMES_TYPE: {}}
        for vol in self.get_volumes_list(search_opts=kwargs):
            if vol.status not in ['available', 'in-use']:
                continue

            volume = self.convert_volume(vol)
            snapshots = {}
            if self.config.migrate.keep_volume_snapshots:
                search_opts = {'volume_id': volume['id']}
                for snap in self.get_snapshots_list(search_opts=search_opts):
                    snapshot = self.convert_snapshot(snap,
                                                     volume)
                    snapshots[snapshot['id']] = snapshot
            info[utils.VOLUMES_TYPE][vol.id] = {utils.VOLUME_BODY: volume,
                                                'snapshots': snapshots,
                                                utils.META_INFO: {
                                                }}
        return info

    def get_quota(self, tenant_id):
        # TODO: update to cinderclient==1.6.0 will eliminate the need in _info
        # pylint: disable=protected-access
        return copy.deepcopy(self.cinder_client.quotas.get(tenant_id)._info)

    def update_quota(self, tenant, quota_dict):
        # TODO: update to cinderclient==1.6.0 will eliminate the need in _info
        try:
            new_quota = self.cinder_client.quotas.update(tenant.id,
                                                         **quota_dict)
            # pylint: disable=protected-access
            return copy.deepcopy(new_quota._info)
        except cinder_exc.ClientException as e:
            LOG.warning("Failed to update quota for tenant '%s' (%s): %s",
                        tenant.name, tenant.id, e)

    def _read_info_quota(self):
        """cinderclient allows user to update cinder quotas for tenant ID
        and tenant name, and it treats those quotas as different objects,
        so user may get confused to see different output for `cinder
        quota-show <tenant ID>` and `cinder quota-show <tenant name>`. This
        behavior is ignored during migration and only quotas by tenant ID
        are migrated."""

        tenants = []
        if self.cloud.position == 'src' and self.filter_tenant_id:
            if isinstance(self.filter_tenant_id, list):
                filtered_tenants = self.filter_tenant_id
            else:
                filtered_tenants = [self.filter_tenant_id]
            for t in filtered_tenants:
                tenant = self.identity_client.try_get_tenant_by_id(t)
                if tenant:
                    tenants.append(tenant)
        else:
            tenants = self.identity_client.get_tenants_list()
        quotas = []
        for t in tenants:
            quota = self.get_quota(t.id)

            # quota UUID is not required
            quota.pop('id')
            LOG.debug("Retrieved cinder quota for tenant '%s' (%s): %s",
                      t.name, t.id, quota)

            quota['tenant_name'] = self.tenant_name_map.map(t.name)

            quotas.append(quota)
        return quotas

    def _deploy_quota(self, quotas):
        quotas_res = []
        for quota in quotas:
            ks = self.identity_client
            tenant_name = quota.pop('tenant_name')

            tenant = ks.try_get_tenant_by_name(tenant_name)

            if tenant is None:
                LOG.warning("Tenant '%s' is not present in destination, "
                            "cinder quotas migration for that tenant will be "
                            "skipped.", tenant_name)
                continue

            tenant_id = tenant.id

            existing_quotas = self.get_quota(tenant_id)
            existing_quotas.pop('id')

            for k in set(quota.keys()).difference(set(existing_quotas.keys())):
                quota.pop(k)

            quotas_identical = all([existing_quotas[k] == quota[k]
                                    for k in quota])

            if quotas_identical:
                LOG.info("Source cloud cinder quotas for tenant '%s' (%s) "
                         "match existing quotas in destination and will not "
                         "be updated.", tenant_name, tenant_id)
                continue

            LOG.debug("Updating cinder quota for tenant '%s' (%s) with "
                      "%s", tenant_name, tenant_id, quota)
            dst_quota = self.update_quota(tenant, quota)
            if dst_quota:
                quotas_res.append(dst_quota)
        return quotas_res

    def _deploy_resources(self, info):
        res = {
            'volumes': {
                'quotas': self._deploy_quota(info['quotas'])
            }
        }
        return res

    def deploy(self, info, target='volumes', *args, **kwargs):
        if target == 'resources':
            return self._deploy_resources(info)
        if target == 'volumes':
            return self.deploy_volumes(info)

    def attach_volume_to_instance(self, volume_info):
        if 'instance' in volume_info[utils.META_INFO]:
            if volume_info[utils.META_INFO]['instance']:
                self.attach_volume(
                    volume_info[utils.VOLUME_BODY]['id'],
                    volume_info[utils.META_INFO]['instance']['instance']['id'],
                    volume_info[utils.VOLUME_BODY]['device'])

    def filter_volumes(self, volumes):
        filtering_enabled = self.cloud.position == SRC

        if filtering_enabled:
            flts = self.get_filter().get_filters()
            for f in flts:
                volumes = ifilter(f, volumes)
            volumes = list(volumes)

            def get_name(volume):
                if isinstance(volume, dict):
                    return volume.get(DISPLAY_NAME, volume['id'])
                return getattr(volume, DISPLAY_NAME, None) or volume.id

            LOG.info("Filtered volumes: %s",
                     ", ".join((str(get_name(i)) for i in volumes)))
        return [vol for vol in volumes
                if cinder_filters.CinderFilters.get_col(vol, 'status').lower()
                in VALID_STATUSES]

    def get_volumes_list(self, detailed=True, search_opts=None):
        search_opts = search_opts or {}
        search_opts['all_tenants'] = 1
        volumes = self.cinder_client.volumes.list(detailed, search_opts)

        volumes = self.filter_volumes(volumes)

        return volumes

    def get_migrated_volume(self, volume_id):
        """:returns: volume which was created from another volume using
        :create_volume_from_volume: method"""
        for v in self.get_volumes_list():
            if v.metadata.get(MIGRATED_VOLUMES_METADATA_KEY) == volume_id:
                return v

    def get_snapshots_list(self, detailed=True, search_opts=None):
        return self.cinder_client.volume_snapshots.list(detailed, search_opts)

    def create_snapshot(self, volume_id, force=False,
                        display_name=None, display_description=None):
        return self.cinder_client.volume_snapshots.create(volume_id,
                                                          force,
                                                          display_name,
                                                          display_description)

    def create_volume_from_volume(self, volume, tenant_id):
        """Creates volume based on values from :param volume: and adds
        metadata in order to not copy already copied volumes

        :param volume: CF volume object (dict)

        :raises: retrying.TimeoutExceeded if volume did not become available
        in migrate.storage_backend_timeout time
        """

        glance = self.cloud.resources[utils.IMAGE_RESOURCE]
        compute = self.cloud.resources[utils.COMPUTE_RESOURCE]
        az_mapper = compute.attr_override

        metadata = volume.get('metadata', {})
        metadata[MIGRATED_VOLUMES_METADATA_KEY] = volume['id']

        image_id = None
        if volume['bootable']:
            image_metadata = volume['volume_image_metadata']
            dst_image = glance.get_matching_image(
                uuid=image_metadata['image_id'],
                size=image_metadata['size'],
                name=image_metadata['image_name'],
                checksum=image_metadata['checksum'])
            if dst_image:
                image_id = dst_image.id

        src_az = compute.get_availability_zone(volume['availability_zone'])

        created_volume = self.create_volume(
            size=volume['size'],
            project_id=tenant_id,
            display_name=volume['display_name'],
            display_description=volume['display_description'],
            availability_zone=src_az or az_mapper.get_attr(
                volume, 'availability_zone'),
            metadata=metadata,
            imageRef=image_id)

        timeout = self.config.migrate.storage_backend_timeout
        retryer = retrying.Retry(max_time=timeout,
                                 predicate=lambda v: v.status == 'available',
                                 predicate_retval_as_arg=True,
                                 retry_message="Volume is not available")

        retryer.run(self.get_volume_by_id, created_volume.id)

        return created_volume

    def create_volume(self, size, **kwargs):
        """Creates volume of given size
        :raises: OverLimit in case quota exceeds for tenant
        """
        cinder = self.cinder_client
        tenant_id = kwargs.get('project_id')

        # if volume needs to be created in non-admin tenant, re-auth is
        # required in that tenant
        if tenant_id:
            identity = self.cloud.resources[utils.IDENTITY_RESOURCE]
            ks = identity.keystone_client
            user = self.config.cloud.user
            with keystone.AddAdminUserToNonAdminTenant(ks, user, tenant_id):
                tenant = ks.tenants.get(tenant_id)
                cinder = self.proxy(self.get_client(tenant=tenant.name),
                                    self.config)

                with proxy_client.expect_exception(cinder_exc.OverLimit):
                    return cinder.volumes.create(size, **kwargs)
        else:
            with proxy_client.expect_exception(cinder_exc.OverLimit):
                return cinder.volumes.create(size, **kwargs)

    def delete_volume(self, volume_id):
        volume = self.get_volume_by_id(volume_id)
        self.cinder_client.volumes.delete(volume)

    def get_volume_by_id(self, volume_id):
        return self.cinder_client.volumes.get(volume_id)

    def update_volume(self, volume_id, **kwargs):
        volume = self.get_volume_by_id(volume_id)
        return self.cinder_client.volumes.update(volume, **kwargs)

    def attach_volume(self, volume_id, instance_id, mountpoint, mode='rw'):
        volume = self.get_volume_by_id(volume_id)
        return self.cinder_client.volumes.attach(volume,
                                                 instance_uuid=instance_id,
                                                 mountpoint=mountpoint,
                                                 mode=mode)

    def detach_volume(self, volume_id):
        return self.cinder_client.volumes.detach(volume_id)

    def finish(self, vol):
        try:
            with proxy_client.expect_exception(cinder_exc.BadRequest):
                self.cinder_client.volumes.set_bootable(
                    vol[utils.VOLUME_BODY]['id'],
                    vol[utils.VOLUME_BODY]['bootable'])
        except cinder_exc.BadRequest:
            LOG.info("Can't update bootable flag of volume with id = %s "
                     "using API, trying to use DB...",
                     vol[utils.VOLUME_BODY]['id'])
            self.__patch_option_bootable_of_volume(
                vol[utils.VOLUME_BODY]['id'],
                vol[utils.VOLUME_BODY]['bootable'])

    def upload_volume_to_image(self, volume_id, force, image_name,
                               container_format, disk_format):
        volume = self.get_volume_by_id(volume_id)
        resp, image = self.cinder_client.volumes.upload_to_image(
            volume=volume,
            force=force,
            image_name=image_name,
            container_format=container_format,
            disk_format=disk_format)
        return resp, image['os-volume_upload_image']['image_id']

    def get_status(self, resource_id):
        return self.cinder_client.volumes.get(resource_id).status

    def deploy_volumes(self, info):
        new_ids = {}
        for vol_id, vol in info[utils.VOLUMES_TYPE].iteritems():
            vol_for_deploy = self.convert_to_params(vol)
            volume = self.create_volume(**vol_for_deploy)
            vol[utils.VOLUME_BODY]['id'] = volume.id
            timeout = self.config.migrate.storage_backend_timeout
            self.try_wait_for_status(volume.id, self.get_status, AVAILABLE,
                                     timeout=timeout)

            self.finish(vol)
            new_ids[volume.id] = vol_id
        return new_ids

    @staticmethod
    def convert_volume(vol):
        volume = {
            'id': vol.id,
            'size': vol.size,
            'display_name': vol.display_name,
            'display_description': vol.display_description,
            'volume_type': (
                None if vol.volume_type == u'None' else vol.volume_type),
            'availability_zone': vol.availability_zone,
            'device': vol.attachments[0][
                'device'] if vol.attachments else None,
            'bootable': vol.bootable.lower() == 'true',
            'volume_image_metadata': {},
            'host': None,
            'path': None,
            'project_id': getattr(vol, 'os-vol-tenant-attr:tenant_id'),
            'metadata': vol.metadata
        }
        if 'volume_image_metadata' in vol.__dict__:
            volume['volume_image_metadata'] = {
                'image_id': vol.volume_image_metadata['image_id'],
                'checksum': vol.volume_image_metadata['checksum'],
                'image_name': vol.volume_image_metadata.get('image_name'),
                'size': int(vol.volume_image_metadata.get('size', 0))
            }
        return volume

    @staticmethod
    def convert_snapshot(snap, volume):

        snapshot = {
            'id': snap.id,
            'volume_id': snap.volume_id,
            'tenant_id': snap.project_id,
            'display_name': snap.display_name,
            'display_description': snap.display_description,
            'created_at': snap.created_at,
            'size': snap.size,
            'vol_path': volume['path']
        }

        return snapshot

    @staticmethod
    def convert_to_params(vol):
        volume_body = vol[utils.VOLUME_BODY]
        info = {
            'size': volume_body['size'],
            'display_name': volume_body['display_name'],
            'display_description': volume_body['display_description'],
            'volume_type': volume_body['volume_type'],
            'availability_zone': volume_body['availability_zone'],
        }
        if 'image' in vol[utils.META_INFO]:
            if vol[utils.META_INFO]['image']:
                info['imageRef'] = vol[utils.META_INFO]['image']['id']
        return info

    def __patch_option_bootable_of_volume(self, volume_id, bootable):
        cmd = ('UPDATE volumes SET volumes.bootable=%s WHERE '
               'volumes.id="%s"') % (int(bootable), volume_id)
        self.mysql_connector.execute(cmd)

    def download_table_from_db_to_file(self, table_name, file_name):
        self.mysql_connector.execute("SELECT * FROM %s INTO OUTFILE '%s';" %
                                     (table_name, file_name))

    def upload_table_to_db(self, table_name, file_name):
        self.mysql_connector.execute("LOAD DATA INFILE '%s' INTO TABLE %s" %
                                     (file_name, table_name))

    def update_column_with_condition(self, table_name, column,
                                     old_value, new_value):

        self.mysql_connector.execute("UPDATE %s SET %s='%s' WHERE %s='%s'" %
                                     (table_name, column, new_value, column,
                                         old_value))

    def update_column(self, table_name, column_name, new_value):
        self.mysql_connector.execute("UPDATE %s SET %s='%s'" %
                                     (table_name, column_name, new_value))

    def get_volume_path_iscsi(self, vol_id):
        cmd = "SELECT provider_location FROM volumes WHERE id='%s';" % vol_id

        result = self.cloud.mysql_connector.execute(cmd)

        if not result:
            raise Exception('There is no such raw in Cinder DB with the '
                            'specified volume_id=%s' % vol_id)

        provider_location = result.fetchone()[0]
        provider_location_list = provider_location.split()

        iscsi_target_id = provider_location_list[1]
        lun = provider_location_list[2]
        ip = provider_location_list[0].split(',')[0]

        volume_path = '/dev/disk/by-path/ip-%s-iscsi-%s-lun-%s' % (
            ip,
            iscsi_target_id,
            lun)

        return volume_path
