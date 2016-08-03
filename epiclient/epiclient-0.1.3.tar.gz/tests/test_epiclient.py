# ````/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_epiclient
----------------------------------

Tests for `epiclient` module.
"""
import copy
import logging
from mock import call
from mock import MagicMock
import os
import pytest
import sys
import requests


import json

from epiclient.epiclient import Epiclient
from epipearl.epipearl import Epipearl
from epipearl.errors import SettingConfigError

from conftest import read_datafile


epiphan_url = "http://fake.example.edu"
epiphan_user = "user"
epiphan_passwd = "passwd"

# control skipping live tests according to command line option --runlive
# requires env vars EPI_URL, EPI_USER, EPI_PASSWD, EPI_PUBLISH_TYPE
livetest = pytest.mark.skipif(
        not pytest.config.getoption("--runlive"),
        reason=(
            "need --runlive option to run, plus env vars",
            "EPI_URL, EPI_USER, EPI_PASSWD"))

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


class TestEpiclient(object):

    def setup(self):
        datastring = read_datafile('primary_sample_ca_settings')
        check = Epiclient.validate_json_input(datastring)
        self.primary_settings = json.loads(datastring)

        self.client = Epipearl(epiphan_url, epiphan_user, epiphan_passwd)


    def test_clear_channels_ok(self):
        mock = MagicMock(return_value=True)
        resp = Epiclient.clear_channels(mock, self.primary_settings)

        assert mock.delete_channel.call_count == 4
        assert mock.delete_recorder.call_count == 1
        mock.delete_channel.assert_any_call('1')
        mock.delete_channel.assert_any_call('2')
        mock.delete_channel.assert_any_call('3')
        mock.delete_channel.assert_any_call('4')
        mock.delete_recorder.assert_any_call('1')


    def test_create_channels_ok(self):

        def my_side_effect(*args, **kwargs):
            if args[0] == 'dce_pr':
                return '8'
            elif args[0] == 'dce_pn':
                return '10'
            elif args[0] == 'dce_live':
                return '11'
            elif args[0] == 'dce_live_lowbr':
                return '5'
            elif args[0] == 'dce_prpn':
                return '3'

        mock = MagicMock()
        mock.create_channel.side_effect = my_side_effect
        mock.create_recorder.side_effect = my_side_effect
        resp = Epiclient.create_channels(mock, self.primary_settings)

        assert mock.create_channel.call_count == 4
        mock.create_channel.assert_any_call('dce_pr')
        mock.create_channel.assert_any_call('dce_pn')
        mock.create_channel.assert_any_call('dce_live')
        mock.create_channel.assert_any_call('dce_live_lowbr')
        mock.create_recorder.assert_any_call('dce_prpn')
        assert self.primary_settings['channels'][
                'dce_pr']['channel_id'] == '8'
        assert self.primary_settings['channels'][
                'dce_pn']['channel_id'] == '10'
        assert self.primary_settings['channels'][
                'dce_live']['channel_id'] == '11'
        assert self.primary_settings['channels'][
                'dce_live_lowbr']['channel_id'] == '5'
        assert self.primary_settings['recorders'][
                'dce_prpn']['recorder_id'] == '3'


    def test_create_channels_error(self):

        def my_side_effect(*args, **kwargs):
            if args[0] == 'dce_pr':
                return '8'
            elif args[0] == 'dce_pn':
                return '10'
            elif args[0] == 'dce_live':
                return '11'
            elif args[0] == 'dce_live_lowbr':
                return '5'
            elif args[0] == 'dce_prpn':
                raise requests.HTTPError('another fake error')

        mock = MagicMock()
        mock.create_channel.side_effect = my_side_effect
        mock.create_recorder.side_effect = my_side_effect

        with pytest.raises(requests.HTTPError) as e:
            resp = Epiclient.create_channels(mock, self.primary_settings)
        assert 'another fake error' in e.value.message


    def test_configure_channel_layout_ok(self):
        pr_layout = read_datafile('sample_layout_pr')
        pn_layout = read_datafile('sample_layout_pn')
        live_layout = read_datafile('sample_layout_live')
        mock = MagicMock()
        mock.set_channel_layout.response_value = True

        resp = Epiclient.configure_channel_layouts(mock, self.primary_settings)

        assert mock.set_channel_layout.call_count == 4
        mock.set_channel_layout.assert_any_call(
                channel_id='1', layout=pr_layout)
        mock.set_channel_layout.assert_any_call(
                channel_id='2', layout=pn_layout)
        mock.set_channel_layout.assert_any_call(
                channel_id='3', layout=live_layout)
        mock.set_channel_layout.assert_any_call(
                channel_id='4', layout=live_layout)


    def test_configure_channel_encodings_ok(self):
        mock = MagicMock()
        mock.set_params.response_value = True

        resp = Epiclient.configure_channel_encodings(
                mock, self.primary_settings)

        assert mock.set_params.call_count == 4

        enc = copy.copy(self.primary_settings['channel_encodings'])
        enc.update(self.primary_settings['channels']['dce_pr']['encodings'])
        mock.set_params.assert_any_call(channel='1', params=enc)

        enc = copy.copy(self.primary_settings['channel_encodings'])
        enc.update(self.primary_settings['channels']['dce_pn']['encodings'])
        mock.set_params.assert_any_call(channel='2', params=enc)

        enc = copy.copy(self.primary_settings['channel_encodings'])
        enc.update(self.primary_settings['channels']['dce_live']['encodings'])
        mock.set_params.assert_any_call(channel='3', params=enc)

        enc = copy.copy(self.primary_settings['channel_encodings'])
        enc.update(self.primary_settings['channels'][
            'dce_live_lowbr']['encodings'])
        mock.set_params.assert_any_call(channel='4', params=enc)


    def test_configure_live_streaming_ok(self):
        mock = MagicMock()
        mock.set_channel_rtmp.return_value = True

        resp = Epiclient.configure_live_streaming(
                mock, self.primary_settings,
                rtmp_usr='soylent', rtmp_pwd='green')

        assert mock.set_channel_rtmp.call_count == 2

        mock.set_channel_rtmp.assert_any_call(
                channel_id='3',
                rtmp_url='rtmp://p.blobblob.i.streamingservice.org/EntryPoint',
                rtmp_stream='my-dev-epiphan',
                rtmp_usr='soylent',
                rtmp_pwd='green')

        mock.set_channel_rtmp.assert_any_call(
                channel_id='4',
                rtmp_url='rtmp://p.blobblob.i.streamingservice.org/EntryPoint',
                rtmp_stream='my-dev-epiphan',
                rtmp_usr='soylent',
                rtmp_pwd='green')


    def test_configure_general_settings_ok(self):
        mock = MagicMock()
        mock.return_value = True

        resp = Epiclient.configure_general_settings(mock, self.primary_settings)

        mock.set_ntp.assert_called_once()
        mock.set_ntp.assert_called_with(
                server='0.nz.pool.ntp.org', timezone='US/Alaska')
        mock.set_touchscreen.assert_called_once()
        mock.set_touchscreen.assert_called_with(screen_timeout=579)
        mock.set_permanent_logs.assert_called_once()
        mock.set_permanent_logs.assert_called_with(log_enabled=True)


    def test_configure_mhpearl_ok(self):
        mock = MagicMock()
        mock.return_value = True

        resp = Epiclient.configure_mhpearl(
                mock, self.primary_settings,
                mh_digest_usr='andromeda', mh_digest_pwd='strain')

        mock.set_mhpearl_settings.assert_called_once()
        mock.set_mhpearl_settings.assert_called_with(
                device_name='my-dev-epiphan',
                device_channel='1',
                file_search_range_in_seconds=58,
                admin_server_url="http://cluster.dev.url.edu",
                admin_server_usr='andromeda',
                admin_server_pwd='strain',
                update_frequency_in_seconds=123,
                backup_agent=False)


    def test_configure_deinterlacing_sources_ok(self):
        mock = MagicMock()
        mock.set_deinterlacing_source.return_value = True
        infocfg = {
                'channels': [
                    {'id': '1', 'name': 'dce_pr'},
                    {'id': '2', 'name': 'dce_live_lowbr'},
                    {'id': '3', 'name': 'dce_live'},
                    {'id': '4', 'name': 'dce_pn'}
                    ],
                'recorders': [
                    {'id': '1', 'name': 'dce_prpn'}
                    ],
                'sources': [
                    {'id': 'D12345678.hdmi-a', 'name': 'HDMI-A'},
                    {'id': 'D12345678.hdmi-b', 'name': 'HDMI-B'},
                    {'id': 'D12345678.sdi-a', 'name': 'SDI-A'},
                    {'id': 'D12345678.sdi-b', 'name': 'SDI-B'},
                    {'id': 'D12345678.vga-a', 'name': 'VGA-A'},
                    {'id': 'D12345678.vga-b', 'name': 'VGA-B'},
                    {'id': 'D12345678.analog-a', 'name': 'Analog-A Audio'},
                    {'id': 'D12345678.analog-b', 'name': 'Analog-B Audio'},
                    {'id': 'D12345678.hdmi-a-audio', 'name': 'HDMI-A Audio'},
                    {'id': 'D12345678.hdmi-b-audio', 'name': 'HDMI-B Audio'},
                    {'id': 'D12345678.sdi-a-audio', 'name': 'SDI-A Audio'},
                    {'id': 'D12345678.sdi-b-audio', 'name': 'SDI-B Audio'},
                    ]
                }

        resp = Epiclient.configure_deinterlacing_sources(
                mock, self.primary_settings, infocfg['sources'])

        expected = [
                call.set_deinterlacing(
                    source_name='D12345678.hdmi-a', deinterlacing=True),
                call.set_deinterlacing(
                    source_name='D12345678.hdmi-b', deinterlacing=True),
                call.set_deinterlacing(
                    source_name='D12345678.sdi-a', deinterlacing=True),
                call.set_deinterlacing(
                    source_name='D12345678.sdi-b', deinterlacing=True),
                call.set_deinterlacing(
                    source_name='D12345678.vga-a', deinterlacing=True),
                call.set_deinterlacing(
                    source_name='D12345678.vga-b', deinterlacing=True),
                ]
        mock.mock_calls == expected


    @livetest
    def test_live_configure_channel_layout(self):
        pr_layout = read_datafile('sample_layout_pr')
        pn_layout = read_datafile('sample_layout_pn')
        live_layout = read_datafile('sample_layout_live')

        ca_url = os.environ['EPI_URL']
        epi = Epipearl(
                ca_url, os.environ['EPI_USER'], os.environ['EPI_PASSWD'])

        resp = Epiclient.configure_channel_layouts(epi, self.primary_settings)

        assert resp == 'blu'
