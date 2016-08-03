# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import copy
from dotenv import find_dotenv
from dotenv import load_dotenv
from epipearl import Epipearl
import json
import logging
import os
import re
import requests
from requests.auth import HTTPBasicAuth

settings = {
    'ca_capture_card_id': 'CHANGE_ME',
    'ca_name_id': 'CHANGE_ME',
    'ca_serial_number': 'CHANGE_ME',
    'ca_url': 'CHANGE_ME',
    'channel_encodings': {
        'audio': 'on',
        'audiochannels': '1',
        'audiopreset': 'libfaac;44100',
        'autoframesize': '',
        'codec': 'h.264',
        'fpslimit': 30,
        'vencpreset': '5',
        'vkeyframeinterval': 1,
        'vprofile': '100'
    },
    'channels': {
        'dce_live': {
            'channel_id': 'CHANGE_ME',
            'encodings': {
                'audiobitrate': 96,
                'framesize': '1920x1080',
                'vbitrate': 4000
            },
            'rtmp_url': 'CHANGE_ME',
            'stream_name': 'CHANGE_ME'
        },
        'dce_live_lowbr': {
            'channel_id': 'CHANGE_ME',
            'encodings': {
                'audiobitrate': 64,
                'framesize': '960x270',
                'vbitrate': 250
            },
            'rtmp_url': 'CHANGE_ME',
            'stream_name': 'CHANGE_ME'
        },
        'dce_pn': {
            'channel_id': 'CHANGE_ME',
            'encodings': {
                'audiobitrate': 160,
                'framesize': '1920x540',
                'vbitrate': 9000
            }
        },
        'dce_pr': {
            'channel_id': 'CHANGE_ME',
            'encodings': {
                'audiobitrate': 160,
                'framesize': '1280x720',
                'vbitrate': 9000
            }
        }
    },
    'cluster_env': 'CHANGE_ME',
    'cluster_name_id': 'CHANGE_ME',
    'date_and_time': {
        'ntp_server': '140.247.197.171',
        'timezone': 'US/Eastern'
    },
    'firmware_version': 'CHANGE_ME',
    'location_name_id': 'CHANGE_ME',
    'maintenance': {
            'permanent_logs': 'on'
            },
    'mh_admin_url': 'CHANGE_ME',
    'mh_ca_name': 'CHANGE_ME',
    'mhpearl_file_search_range': 60,
    'mhpearl_update_frequency': 120,
    'mhpearl_version': 'CHANGE_ME',
    'pn_vconnector': 'CHANGE_ME',
    'pn_vinput': 'b',
    'pr_vconnector': 'sdi',
    'pr_vinput': 'a',
    'recorders': {
            'dce_prpn': {
                'output_format': 'avi',
                'recorder_id': 'CHANGE_ME',
                'sizelimit': 64000000,
                'timelimit': 360
                }
            },
    'role': 'CHANGE_ME',
    'source_deinterlacing': 'on',
    'touchscreen': {
            'episcreen_timeout': 600
            }
    }


def pull_ca_list(url, creds=None):
    """
    get text file from `url`.

    read a text file from given url
    if basic auth needed, pass args creds['user'] and creds['pwd']
    """
    headers = {
            'User-Agent': 'python-epiclient',
            'Accept-Encoding': 'gzip, deflate',
            'Accept': 'text/html, text/*'
            }
    au = None
    if creds is not None:
        if 'user' in creds and 'pwd' in creds:
            au = HTTPBasicAuth(creds['user'], creds['pwd'])
            headers.update({'X-REQUESTED-AUTH': 'Basic'})

    try:
        response = requests.get(url, headers=headers, auth=au)
    except requests.HTTPError as e:
        logging.getLogger(__name__).warning(
                'data from url(%s) is unavailable. Error: %s' % (url, e))
        return None
    else:
        return json.loads(response.text)


def clean_name(name):
    """
    clean `name` from non_alpha.

    replaces non-alpha with underscores '_' and set the string to lower case
    """
    return re.sub('[^0-9a-zA-Z]+', '_', name.strip()).lower()


def find_ca_name(soup):
    """scrape through mhpearl html form and return ca_name."""
    tags = soup.find_all(id='ca_name')
    if len(tags) > 0 and tags[0].has_attr('value'):
        return tags[0]['value']
    else:
        return None


def find_mh_host(soup):
    """scrape through mhpearl html form and return mh_host."""
    tags = soup.find_all(id='mh_host')
    if len(tags) > 0 and tags[0].has_attr('value'):
        return tags[0]['value']
    else:
        return None


def save_cfg(ca_name, cfg):
    """save configs in file."""
    filename = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            '{}.json'.format(ca_name))

    with open(filename, "w") as f:
        f.write(json.dumps(cfg, sort_keys=True, indent=4))


def main():
    """
    pull json with list of CAs from ca-status and loop through CAs, generating
    corresponding json settings input file.
    """

    # set environment for main()
    dotenv_filepath = os.path.expanduser('~/.epiclient.env')
    resp = load_dotenv(dotenv_filepath)
    if resp is None:
        print 'missing `~/.epiclient.env` file!`'
        exit(1)


    ca_list = pull_ca_list(
            url=os.environ.get('CA_STATS_URL'),
            creds={
                'user': os.environ.get('CA_STATS_USER'),
                'pwd': os.environ.get('CA_STATS_PASSWD')
                }
            )

    for ca in ca_list:
        if not ca['pingable']:
            print 'skipping device {}'.format(ca['name'])
            continue

        cfg = copy.copy(settings)
        cfg['role'] = ca['role'].lower()
        cfg['ca_name_id'] = clean_name(ca['name'])
        cfg['ca_url'] = 'http://{}'.format(ca['address'])
        cfg['ca_serial_number'] = ca['ca_attributes']['serial_number']
        cfg['location_name_id'] = ca['location'].lower().replace(' ', '_')

        for firmware in ca['ca_attributes']['firmware_info']:
            if firmware.startswith('FIRMWARE_VERSION'):
                cfg['firmware_version'] = firmware.split('\"')[1]

        # guessing environment
        if ca['name'].startswith('prod'):
            rtmp_acct = '345252'
            cfg['cluster_env'] = 'prod'
        else:
            rtmp_acct = '355694'
            cfg['cluster_env'] = 'dev'

        rtmp_url = 'rtmp://p.ep{}'.format(rtmp_acct)
        # config depending on role
        if cfg['role'] == 'primary' or cfg['role'] == 'experimental':
            cfg['mh_ca_name'] = ca['name']
        else:
            cfg['mh_ca_name'] = None
            rtmp_url = 'rtmp://b.ep{}'.format(rtmp_acct)
            rtmp_url += '.i.akamaientrypoint.net/EntryPoint'
        cfg['channels']['dce_live']['rtmp_url'] = rtmp_url
        cfg['channels']['dce_live']['stream_name'] = \
                '{}-presenter-delivery.stream-{}_1_200@{}'.format(
                        ca['name'],
                        cfg['channels']['dce_live']['encodings']['framesize'],
                        rtmp_acct)
        cfg['channels']['dce_live_lowbr']['rtmp_url'] = rtmp_url
        cfg['channels']['dce_live_lowbr']['stream_name'] = \
                '{}-presenter-delivery.stream-{}_1_200@{}'.format(
                        ca['name'],
                        cfg['channels']['dce_live_lowbr']['encodings']['framesize'],
                        rtmp_acct)


        # guessing pn connector
        cfg['pn_vconnector'] = 'sdi'  # preferred connector is sdi
        if 'ca_attributes' in ca:
            channels = ca['ca_attributes']['channels']
            for ch in channels:
                if ch.startswith('m'):
                    continue  # skip if this is a recorder

                if 'hdmi' in channels[ch]['name'].lower():
                    # trusting channel was named after connectors
                    cfg['pn_vconnector'] = 'hdmi'

        cli = Epipearl(
                cfg['ca_url'],
                os.environ.get('EPIPEARL_USER'), os.environ.get('EPIPEARL_PASSWD'))

        try:
            infocfg = cli.get_infocfg()
        except Exception as e:
            print 'Error while pulling infocfg from device({}) - {}'.format(
                    cli.url, e.message)
            continue
        else:
            cfg['ca_capture_card_id'] = infocfg[
                    'sources'][0]['id'].split('.')[0]

        try:
            resp = cli.get('admin/mhcfg')
        except Exception as e:
            print 'Error while pulling infocfg from device({}) - {}'.format(
                    cli.url, e.message)
            continue
        else:
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, 'html.parser')
                cfg['mh_admin_url'] = find_mh_host(soup)
                if cfg['mh_ca_name'] is None:
                    cfg['mh_ca_name'] = find_ca_name(soup)

        print 'saving cfg({})'.format(cfg['ca_name_id'])
        save_cfg(ca['name'], cfg)



#
# main
#
if __name__ == "__main__":
    main()
