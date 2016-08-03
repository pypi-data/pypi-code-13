# -*- coding: utf-8 -*-

"""
epiclient
---------------
epipearl client to configure device as dce capture-agent for opencast
"""

import copy
from jinja2 import Template
import json
import jsonspec.validators
import logging
import os
import pkg_resources
import requests

from epipearl.errors import EpipearlError


logger = logging.getLogger(__name__)


class EpiclientError(Exception):
    """base class for epiclient module errors."""


class Epiclient(object):
    _role_settings_schema_filename = 'role_settings_schema.json'

    _layout_single_channel_template = Template('''{
    "audio": [
        {
            "settings": {
                "source": "{{source_id}}.{{aconnector}}-{{ainput}}-audio"
            },
            "type": "source"
        }
    ],
    "background": "#000000",
    "nosignal": {
        "id": "default"
    },
    "video": [
        {
            "position": {
                "height": "100%",
                "keep_aspect_ratio": true,
                "left": "0%",
                "top": "0%",
                "width": "100%"
            },
            "settings": {
                "source": "{{source_id}}.{{vconnector}}-{{vinput}}"
            },
            "type": "source"
        }
    ]
}
''')

    _layout_combined_channels_template = Template('''{
    "audio": [
        {
            "settings": {
                "source": "{{source_id}}.{{pr_aconnector}}-{{pr_ainput}}-audio"
            },
            "type": "source"
        }
    ],
    "nosignal": {
        "id": "default"
    },
    "background": "#000000",
    "video": [
        {
            "crop": {},
            "position": {
                "keep_aspect_ratio": true,
                "height": "100%",
                "width": "50%",
                "left": "0%",
                "top": "0%"
            },
            "settings": {
                "source": "{{source_id}}.{{pr_vconnector}}-{{pr_vinput}}"
            },
            "type": "source"
        },
        {
            "crop": {},
            "position": {
                "keep_aspect_ratio": true,
                "height": "100%",
                "width": "50%",
                "left": "50%",
                "top": "0%"
            },
            "settings": {
                "source": "{{source_id}}.{{pn_vconnector}}-{{pn_vinput}}"
            },
            "type": "source"
        }
    ]
}''')

    @classmethod
    def get_json_schema_fullpath(cls, json_schema_filename):
        """return the fullpath in the package, for the json schema."""
        resource_path = os.path.join('json_schema', json_schema_filename)
        return pkg_resources.resource_filename(__name__, resource_path)


    @classmethod
    def validate_json_input(cls, json_inputstring):
        """validates a json against role_settings schema."""

        filename = cls.get_json_schema_fullpath(
                cls._role_settings_schema_filename)
        with open(filename, 'r') as myfile:
            schema_string = myfile.read()

        json_data = json.loads(json_inputstring)
        json_schema = json.loads(schema_string)

        try:
            validator = jsonspec.validators.load(json_schema)
        except jsonspec.validators.CompilationError as e:
            msg = 'error loading schema: {}'.format(e.message)
            logger.error(msg)
            raise e

        try:
            resp = validator.validate(json_data)
        except jsonspec.validators.ValidationError as e:
            msg = 'error validating againts json_schema({}): {}'.format(
                    filename, e.message)
            logger.error(msg)
            raise e

        return True


    @classmethod
    def fetch_infocfg(cls, client):
        """get infocfg from capture agent."""
        try:
            r_infocfg = client.get_infocfg()
        except Exception as e:
            msg = 'failed to get_infocfg for device({}) - {}'.format(
                    client.url, e.message)
            logger.error(msg)
            raise e
        else:
            return r_infocfg


    @classmethod
    def clear_channels(cls, client, settings):
        """delete all dce channels and recorders for given epipearl client."""
        for rec_name in settings['recorders']:
            try:
                client.delete_channel_or_recorder_by_name(rec_name)
            except EpipearlError as e:
                msg = 'failed during clear recorder('
                msg += '{})({}) from epiphan({}) - {}'. format(
                        rec_name,
                        settings['recorders'][rec_name]['recorder_id'],
                        client.url, e.message)
                logger.error(msg)
                raise e

        for channel_name in settings['channels']:
            try:
                client.delete_channel_or_recorder_by_name(channel_name)
            except EpipearlError as e:
                msg = 'failed during clear channel('
                msg += '{})({}) from epiphan({}) - {}'.format(
                        channel_name,
                        settings['channels'][channel_name]['channel_id'],
                        client.url, e.message)
                logger.error(msg)
                raise e

        return True


    @classmethod
    def configure_deinterlacing_sources(
            cls, client, settings, sources=None):
        """enabled/disable deinterlacing in video sources."""
        if sources is None:
            infocfg = cls.fetch_infocfg(client)
            if len(infocfg['sources']) > 0:
                sources = infocfg['sources']
            else:
                msg = 'failed to deinterlacing: no sources found'
                msg += ' in infocfg response for device({})'.format(
                        client.url)
                logger.error(msg)
                raise EpiclientError(msg)

        deinterlacing = settings['source_deinterlacing'] == 'on'
        for s in sources:
            if 'audio' not in s['name'].lower():
                try:
                    client.set_deinterlacing_source(
                            source_name=s['id'],
                            deinterlacing=deinterlacing)
                except EpipearlError as e:
                    msg = 'failed to deinterlacing source('
                    msg += '{}) in epiphan({}) - {}'.format(
                            s['id'], client.url, e.message)
                    logger.error(msg)
                    raise e

        return True


    @classmethod
    def create_channels(cls, client, settings):
        """create dce channels and recorders for given epipearl client."""
        for channel_name in settings['channels']:
            try:
                channel_id = client.create_channel(channel_name)
            except EpipearlError as e:
                msg = 'failed to create channel({}) - {}'.format(
                        channel_name, e.message)
                logger.error(msg)
                raise e
            else:
                settings['channels'][channel_name]['channel_id'] = channel_id

        for rec_name in settings['recorders']:
            try:
                rec_id = client.create_recorder(rec_name)
            except EpipearlError as e:
                msg = 'failed to create recorder({}) - {}'.format(
                        rec_name, e.message)
                logger.error(msg)
                raise e
            else:
                settings['recorders'][rec_name]['recorder_id'] = rec_id

        return settings


    @classmethod
    def _set_channel_layout(
            cls, client,
            channel_name, channel_id,
            layout):
        try:
            client.set_channel_layout(
                    channel_id=channel_id,
                    layout=layout)
        except EpipearlError as e:
            msg = 'failed to set layout for channel({})({}) - {}'.format(
                    channel_name, channel_id, e.message)
            logger.error(msg)
            raise e
        else:
            return True


    @classmethod
    def configure_channel_layouts(cls, client, settings):
        """set layouts for dce channels."""
        pr_ch = settings['channels']['dce_pr']
        pn_ch = settings['channels']['dce_pn']

        # presenter channel
        l = cls._layout_single_channel_template.render(
                source_id=settings['ca_capture_card_id'],
                vconnector=settings['pr_vconnector'],
                vinput=settings['pr_vinput'],
                aconnector=settings['pr_vconnector'],
                ainput=settings['pr_vinput'])
        layout = l.replace(' ', '').replace('\n', '')
        cls._set_channel_layout(
                client=client,
                channel_name='dce_pr', channel_id=pr_ch['channel_id'],
                layout=layout)

        # presentation channel
        l = cls._layout_single_channel_template.render(
                source_id=settings['ca_capture_card_id'],
                vconnector=settings['pn_vconnector'],
                vinput=settings['pn_vinput'],
                aconnector=settings['pr_vconnector'],  # audio from pr
                ainput=settings['pr_vinput'])
        layout = l.replace(' ', '').replace('\n', '')
        cls._set_channel_layout(
                client=client,
                channel_name='dce_pn', channel_id=pn_ch['channel_id'],
                layout=layout)

        # combined source channels
        l = cls._layout_combined_channels_template.render(
                source_id=settings['ca_capture_card_id'],
                pr_vconnector=settings['pr_vconnector'],
                pr_vinput=settings['pr_vinput'],
                pn_vconnector=settings['pn_vconnector'],
                pn_vinput=settings['pn_vinput'],
                pr_aconnector=settings['pr_vconnector'],
                pr_ainput=settings['pr_vinput'])
        layout = l.replace(' ', '').replace('\n', '')
        for channel_name in ['dce_live', 'dce_live_lowbr']:
            channel_id = settings['channels'][channel_name]['channel_id']
            cls._set_channel_layout(
                    client=client,
                    channel_name=channel_name,
                    channel_id=channel_id,
                    layout=layout)
        return True


    @classmethod
    def _set_encodings(
            cls, client, channel_id, channel_name,
            encoding_settings):
        try:
            resp = client.set_params(
                    channel=channel_id, params=encoding_settings)
        except (requests.HTTPError,
                requests.RequestException,
                requests.ConnectionError,
                requests.Timeout) as e:
            msg = 'failed to configure encodings for channel({})({})'.format(
                    channel_name, channel_id)
            msg += '- failed to call {}/set_params - {}'.format(
                    client.url,  e.message)
            logger.error(msg)
            raise e
        else:
            return True


    @classmethod
    def configure_channel_encodings(cls, client, settings):
        """set channel encodings for dce channels."""
        for (channel_name, ch) in settings['channels'].items():
            # merge common and specific encodings for this channel
            encodings = copy.copy(settings['channel_encodings'])
            encodings.update(ch['encodings'])

            cls._set_encodings(
                    client=client, channel_id=ch['channel_id'],
                    channel_name=channel_name,
                    encoding_settings=encodings)

    @classmethod
    def _set_live(
            cls, client, channel_id, channel_name,
            rtmp_url, rtmp_stream, rtmp_usr, rtmp_pwd):
        try:
            client.set_channel_rtmp(
                    channel_id=channel_id,
                    rtmp_url=rtmp_url,
                    rtmp_stream=rtmp_stream,
                    rtmp_usr=rtmp_usr,
                    rtmp_pwd=rtmp_pwd)
        except EpipearlError as e:
            msg = 'failed to configure rtmp for channel({})({}) - {}'.format(
                    channel_id, channel_name, e.message)
            logger.error(msg)
            raise e
        else:
            return True


    @classmethod
    def start_live(cls, client, channel_id, startlive=True):
        params = {'publish_type': '6'}
        if not startlive:
            params['publish_type'] = 0

        try:
            client.set_params(channel_id, params)
        except EpipearlError as e:
            msg = 'failed to {} live channel({}) in device({}) - {}'.format(
                    'start' if startlive else 'stop',
                    channel_id, client.url, e.message)
            logger.error(msg)
            raise e
        else:
            return True


    @classmethod
    def configure_live_streaming(
            cls, client, settings,
            rtmp_usr=None, rtmp_pwd=None):
        """set rtmp configs for dce live channels."""
        for (channel_name, ch) in settings['channels'].items():
            if 'live' in channel_name:
                try:
                    cls._set_live(
                        client,
                        channel_id=ch['channel_id'],
                        channel_name=channel_name,
                        rtmp_url=ch['rtmp_url'],
                        rtmp_stream=ch['stream_name'],
                        rtmp_usr=rtmp_usr,
                        rtmp_pwd=rtmp_pwd)
                except EpipearlError as e:
                    msg = 'failed to configure live in channel({}:{})'.format(
                            channel_name, ch['channel_id'])
                    logger.error(msg)
                    raise e

                # set streaming non-stop
                cls.start_live(client, ch['channel_id'])
        return True


    @classmethod
    def configure_recorder_channels(cls, client, settings):
        """set dce_pr and dce_pn as recorder channels."""
        channel_list = [
                settings['channels']['dce_pr']['channel_id'],
                settings['channels']['dce_pn']['channel_id']
                ]

        try:
            client.set_recorder_channels(
                    settings['recorders']['dce_prpn']['recorder_id'],
                    channel_list)
        except EpipearlError as e:
            msg = 'failed to set channels({}) in recorder({}) - {}'.format(
                    channel_list,
                    settings['recorders']['dce_prpn']['recorder_id'],
                    e.message)
            logger.error(msg)
            raise e
        return True


    @classmethod
    def configure_recorder_settings(cls, client, settings):
        prpn = settings['recorders']['dce_prpn']
        try:
            client.set_recorder_settings(
                    prpn['recorder_id'],
                    recording_timelimit_in_minutes=prpn['timelimit'],
                    recording_sizelimit_in_kbytes=prpn['sizelimit'],
                    output_format=prpn['output_format'])
        except EpipearlError as e:
            msg = 'failed to set recorder(dce_prpn:{}} settings - {}'.format(
                    prpn['recorder_id'], e.message)
            logger.error(msg)
            raise e
        return True


    @classmethod
    def configure_general_settings(cls, client, settings):
        """ntp, touchscreen, permanent_logs."""
        try:
            client.set_ntp(
                server=settings['date_and_time']['ntp_server'],
                timezone=settings['date_and_time']['timezone'])
        except EpipearlError as e:
            msg = 'failed to configure date_and_time for epiphan({}) - {}'.\
                    format(client.url, e.message)
            logger.error(msg)
            raise e

        try:
            client.set_permanent_logs(
                    log_enabled=settings[
                        'maintenance']['permanent_logs'] == 'on')
        except EpipearlError as e:
            msg = 'failed to configure permanent logs for epiphan({}) - {}'.\
                    format(client.url, e.message)
            logger.error(msg)
            raise e

        try:
            client.set_touchscreen(
                    screen_timeout=settings[
                        'touchscreen']['episcreen_timeout'])
        except EpipearlError as e:
            msg = 'failed to configure touchscreen for epiphan({}) - {}'.\
                    format(client.url, e.message)
            logger.error(msg)
            raise e

        return True


    @classmethod
    def configure_mhpearl(
            cls, client, settings,
            mh_digest_usr=None, mh_digest_pwd=None):
        try:
            client.set_mhpearl_settings(
                    device_name=settings['mh_ca_name'],
                    device_channel=settings[
                        'recorders']['dce_prpn']['recorder_id'],
                    file_search_range_in_seconds=settings[
                        'mhpearl_file_search_range'],
                    admin_server_url=settings['mh_admin_url'],
                    admin_server_usr=mh_digest_usr,
                    admin_server_pwd=mh_digest_pwd,
                    update_frequency_in_seconds=settings[
                        'mhpearl_update_frequency'],
                    backup_agent=(settings['role'] == 'secondary'))
        except EpipearlError as e:
            msg = 'failed to configure mhpear for epiphan({}) - {}'.\
                    format(client.url, e.message)
            logger.error(msg)
            raise e
        else:
            return True
