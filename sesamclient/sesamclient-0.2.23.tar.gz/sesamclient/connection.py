# Copyright (C) Bouvet ASA - All Rights Reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.
import io
import json
import urllib.parse
import zipfile

import requests

from . import utils
from .dataset import Dataset
from .exceptions import PipeAlreadyExists, SystemAlreadyExists, ConfigUploadFailed
from .log import Log
from .pipe import Pipe
from .system import System


def quote_id_for_url(item_id):
    return urllib.parse.quote(urllib.parse.quote(item_id, safe=""), safe="")


class Connection:
    """This class represents a connection to a Sesam installation. This is the starting point of all interactions
    with the Sesam installation.
    """
    def __init__(self, sesamapi_base_url,
                 username=None, password=None,
                 client_certificate=None,
                 timeout=30):
        if not sesamapi_base_url.endswith("/"):
            sesamapi_base_url += "/"
        self.sesamapi_base_url = sesamapi_base_url
        self.username = username
        self.password = password
        self.timeout = timeout

        if self.username:
            auth = (self.username, self.password)
        else:
            auth = None

        headers = {
            "ACCEPT": "application/json,*/*"
        }

        self.session = session = requests.Session()
        if auth is not None:
            session.auth = auth
        if client_certificate is not None:
            session.cert = client_certificate
        session.headers = headers

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.session.close()

    def _get_requests_kwargs(self):
        kwargs = {}
        if self.timeout:
            kwargs["timeout"] = self.timeout
        return kwargs

    def do_put_request(self, url, data=None, **kwargs):
        assert url is not None
        session_put_kwargs = self._get_requests_kwargs()
        session_put_kwargs.update(kwargs)
        return self.session.put(url, data=data, **session_put_kwargs)

    def do_get_request(self, url, allowable_response_status_codes=(200, 404), **kwargs):
        assert url is not None
        session_get_kwargs = self._get_requests_kwargs()
        session_get_kwargs.update(kwargs)
        response = self.session.get(url, **session_get_kwargs)
        utils.validate_response_is_ok(response, allowable_response_status_codes)
        return response

    def do_post_request(self, url, **kwargs):
        assert url is not None
        session_post_kwargs = self._get_requests_kwargs()
        session_post_kwargs.update(kwargs)
        return self.session.post(url, **session_post_kwargs)

    def do_delete_request(self, url, **kwargs):
        assert url is not None
        session_delete_kwargs = self._get_requests_kwargs()
        session_delete_kwargs.update(kwargs)
        return self.session.delete(url, **session_delete_kwargs)

    @property
    def pipes_url(self):
        return self.sesamapi_base_url + "pipes"

    def get_pipe_url(self, pipe_id):
        return self.pipes_url + "/" + quote_id_for_url(pipe_id)

    def get_pipe_config_url(self, pipe_id):
        return self.get_pipe_url(pipe_id) + "/config"

    @property
    def logs_url(self):
        return self.sesamapi_base_url + "logs"

    def get_log_url(self, log_id):
        return self.logs_url + "/" + quote_id_for_url(log_id)

    def get_pipe_pump_url(self, pipe_id):
        return self.get_pipe_url(pipe_id) + "/pump"

    def get_pipe_entities_url(self, pipe_id):
        return self.get_pipe_url(pipe_id) + "/entities"

    @property
    def systems_url(self):
        return self.sesamapi_base_url + "systems"

    def get_system_url(self, system_id):
        return self.systems_url + "/" + quote_id_for_url(system_id)

    def get_system_config_url(self, system_id):
        return self.get_system_url(system_id) + "/config"

    @property
    def systemconfigs_url(self):
        return self.sesamapi_base_url + "systemconfigs"

    @property
    def stats_url(self):
        return self.sesamapi_base_url + "stats"

    @property
    def status_url(self):
        return self.sesamapi_base_url + "status"

    @property
    def node_metadata_url(self):
        return self.sesamapi_base_url + "metadata"

    @property
    def node_license_url(self):
        return self.sesamapi_base_url + "license"

    @property
    def datasets_url(self):
        return self.sesamapi_base_url + "datasets"

    @property
    def config_url(self):
        return self.sesamapi_base_url + "config"

    def get_dataset_url(self, dataset_id):
        return self.datasets_url + "/" + quote_id_for_url(dataset_id)

    def get_dataset_entities_url(self, dataset_id):
        return self.get_dataset_url(dataset_id) + "/entities"

    def get_dataset_entity_url(self, dataset_id, entity_id):
        return self.get_dataset_url(dataset_id) + "/entities/" + quote_id_for_url(entity_id)

    def get_dataset_metadata_url(self, dataset_id):
        return self.get_dataset_url(dataset_id) + "/metadata"

    def get_systems(self):
        systems = []

        # TODO: wrap in a utility-method and add error-detection
        response = self.do_get_request(self.systems_url, allowable_response_status_codes=[200])
        parsed_response = utils.parse_json_response(response)

        for system_json in parsed_response:
            systems.append(System(self, system_json))

        return systems

    def get_system(self, system_id):
        response = self.do_get_request(self.get_system_url(system_id))
        if response.status_code == 404:
            return None
        system_json = utils.parse_json_response(response)
        return System(self, system_json)

    def get_systemconfigs(self):
        response = self.do_get_request(self.systemconfigs_url, allowable_response_status_codes=[200])
        return utils.parse_json_response(response)

    def get_stats(self):
        """
        :return: A nested dict with metrics.
        """
        stats_response = self.do_get_request(self.stats_url, allowable_response_status_codes=[200])
        return utils.parse_json_response(stats_response)

    def get_status(self):
        """
        :return: A dict with various status-information (disk-usage, etc.)
        """
        status_response = self.do_get_request(self.status_url)
        return utils.parse_json_response(status_response)

    def get_datasets(self):
        datasets = []
        response = self.do_get_request(self.datasets_url, allowable_response_status_codes=[200])
        parsed_response = utils.parse_json_response(response)
        for dataset_json in parsed_response:
            datasets.append(Dataset(self, dataset_json))
        return datasets

    def get_dataset(self, dataset_id):
        response = self.do_get_request(self.get_dataset_url(dataset_id), )
        if response.status_code == 404:
            return None
        dataset_json = utils.parse_json_response(response)
        return Dataset(self, dataset_json)

    def get_pipes(self):
        pipes = []

        # TODO: wrap in a utility-method and add error-detection
        response = self.do_get_request(self.pipes_url, allowable_response_status_codes=[200])

        parsed_response = utils.parse_json_response(response)

        for pipe_json in parsed_response:
            pipes.append(Pipe(self, pipe_json))
        return pipes

    def get_pipe(self, pipe_id):
        # TODO: wrap in a utility-method and add error-detection
        response = self.do_get_request(self.get_pipe_url(pipe_id))
        if response.status_code == 404:
            return None
        pipe_json = utils.parse_json_response(response)
        return Pipe(self, pipe_json)

    def add_pipes(self, pipe_configs):
        response = self.do_post_request(self.pipes_url, json=pipe_configs)
        utils.validate_response_is_ok(response, allowable_response_status_codes=[201, 409])
        if response.status_code == 409:
            raise PipeAlreadyExists(response.text)

        pipe_json_list = utils.parse_json_response(response)
        pipes = [Pipe(self, pipe_json) for pipe_json in pipe_json_list]
        return pipes

    def add_systems(self, system_configs):
        response = self.do_post_request(self.systems_url, json=system_configs)
        utils.validate_response_is_ok(response, allowable_response_status_codes=[201, 409])
        if response.status_code == 409:
            raise SystemAlreadyExists(response.text)

        system_json_list = utils.parse_json_response(response)
        systems = [System(self, system_json) for system_json in system_json_list]
        return systems

    def get_logs(self):
        logs = []

        # TODO: wrap in a utility-method and add error-detection
        response = self.do_get_request(self.logs_url, allowable_response_status_codes=[200])
        parsed_response = utils.parse_json_response(response)

        for log_json in parsed_response:
            logs.append(Log(self, log_json))
        return logs

    def get_log_content(self, log_id):
        """This returns a stream with the content of the specified logfile"""
        # TODO: wrap in a utility-method and add error-detection
        response = self.do_get_request(self.get_log_url(log_id), stream=True)
        if response.status_code == 404:
            return None
        return response.raw

    def get_metadata(self):
        """Gets the current metadata for the node"""
        response = self.do_get_request(self.node_metadata_url)
        metadata = utils.parse_json_response(response)
        return metadata

    def set_metadata(self, metadata):
        """Replaces the metadata for the node with the specified dictionary"""
        response = self.do_put_request(self.node_metadata_url, json=metadata)
        utils.validate_response_is_ok(response, allowable_response_status_codes=[200])

    def get_license(self):
        """Gets the current license info for the node"""
        response = self.do_get_request(self.node_license_url)
        license_info = utils.parse_json_response(response)
        return license_info

    def set_license(self, license_key_content):
        """Replaces the license for the node with the specified license key"""
        response = self.do_put_request(self.node_license_url, data=license_key_content)
        utils.validate_response_is_ok(response, allowable_response_status_codes=[200])
        license_info = utils.parse_json_response(response)
        return license_info

    def delete_metadata(self):
        """Deleted all metadata for the node"""
        response = self.do_delete_request(self.node_metadata_url)
        utils.validate_response_is_ok(response, allowable_response_status_codes=[200])

    def get_config(self):
        """Returns the configuration of the sesam node.
        """
        response = self.do_get_request(self.config_url, allowable_response_status_codes=[200])
        utils.validate_equal_case_insensitive(response.headers["Content-Type"], "application/json")
        config = utils.parse_json_response(response)
        return config

    def get_config_as_json_string(self):
        """Returns the configuration of the sesam node as a json-string, using the same formatting
        as the raw server response.
        """
        response = self.do_get_request(self.config_url, allowable_response_status_codes=[200])
        utils.validate_equal_case_insensitive(response.headers["Content-Type"], "application/json")
        return response.text

    def get_config_as_zip(self):
        """Returns the configuration of the sesam node as a zip-archive with separate files for each pipe, system,
        etc.

        Tip: the returned bytes can be parsed like this:
               config = zipfile.ZipFile(io.BytesIO(returned_bytes)
        """
        response = self.do_get_request(self.config_url,
                                       allowable_response_status_codes=[200],
                                       headers={"ACCEPT": "application/zip"},
                                       )
        utils.validate_equal_case_insensitive(response.headers["Content-Type"], "application/zip")
        return response.content

    def upload_config(self, config,
                      force=False,
                      _use_multipart_form_data=True):
        """
        Uploads the specified configuration. The new configuration will replace any existing
        configuration. Any existing configuration entities that are not in the new configuration will
        be removed.

        :param config: The config. This can be either a filename, a file-like object, or a bytes-object. The format
                      must be either a json object (as returned by the get_config()-method, or a zip-archive (as
                      returned by the get_config_as_zip()-method).
        :param force: If this is False (the default), no changes will be made if the configuration contains any errors.
                      If it is True, the node will attempt to apply the new configuration on a best-effort basis, and
                      component with erronous configuration will get their "is-valid-config" flag set to false.
        :param _post_as_multipart_form_data: This can be set to False in order to post the config content as the
                                request-body, instead of posting it using the normal "multipart/form-data" encoding.
                                This is only used in ci-tests.

        :returns The parsed response, which will contain a "validation_errors" list. This list will be empty if the
                 upload completed with no errors or warnings.
        """
        theconfigfile_must_be_closed = False

        if isinstance(config, (dict, list)):
            # The configuration is in the form of a json object
            theconfigfile = io.BytesIO(json.dumps(config).encode("utf-8"))

        elif isinstance(config, io.IOBase):
            # The input is a file-like object
            theconfigfile = config
            theconfigfile.seek(0)

        elif isinstance(config, (bytes, bytearray)):
            # The input is the bytes of the zipfile
            theconfigfile = io.BytesIO(config)

        elif isinstance(config, str):
            # The input is a filename
            theconfigfile = open(config, "rb")
            theconfigfile_must_be_closed = True

        else:
            raise TypeError(
                "The 'config' parameter must be file-like object or a filename, but it was of type '%s'" % (
                    type(config),))

        # Try to figure out the content-type to use.
        try:
            zipfile.ZipFile(theconfigfile)
            content_type = 'application/zip'
        except zipfile.BadZipfile:
            try:
                theconfigfile.seek(0)
                json.loads(theconfigfile.read().decode("utf-8"))
                content_type = 'application/json'
            except Exception as e:
                raise TypeError(
                    "The config must be either a zip-archive or a json object! The specified config was neither: %s"
                        % (e,))

        theconfigfile.seek(0)

        request_params = {"force": "true" if force else "false"}

        try:
            if _use_multipart_form_data:
                # This is the normal case. We use the same method a browser would use when uploading a file.
                files = {'file': ('config', theconfigfile, content_type)}
                response = self.do_put_request(self.config_url,
                                               params=request_params,
                                               files=files)
            else:
                # We want to put the config content directly in the response body.
                data = theconfigfile.read()
                if content_type == 'application/zip':
                    if not isinstance(data, bytes):
                        raise TypeError(
                            "The content-type is 'application/zip', but the data isn't of type 'bytes': type(data):%s"
                                % (type(data),))
                response = self.do_put_request(self.config_url, data=data,
                                               params=request_params,
                                               headers={"Content-Type": content_type})

        finally:
            if theconfigfile_must_be_closed:
                theconfigfile.close()

        utils.validate_response_is_ok(response,
                                      allowable_response_status_codes=[200,
                                                                       400  # we will deal with any 400-errors later
                                                                       ])
        utils.validate_equal_case_insensitive(response.headers["Content-Type"], "application/json")

        parsed_response = utils.parse_json_response(response)

        if response.status_code == 400:
            raise ConfigUploadFailed(response=response, parsed_response=parsed_response)

        return parsed_response
