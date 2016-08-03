from urlparse import urlparse
import json
import os
import requests


EXIT_STATUS = ['Aborted', 'Done', 'Error', 'Failed']
SAMPLE_NODE_USERNAME = 'vagrant'
SAMPLE_NODE_PASSWORD = 'foobar123'
SAMPLE_NODES = [
    {'name': 'vm0', 'ip': '192.168.33.10', 'username': SAMPLE_NODE_USERNAME, 'password': SAMPLE_NODE_PASSWORD},
    {'name': 'vm1', 'ip': '192.168.33.11', 'username': SAMPLE_NODE_USERNAME, 'password': SAMPLE_NODE_PASSWORD},
    {'name': 'vm2', 'ip': '192.168.33.12', 'username': SAMPLE_NODE_USERNAME, 'password': SAMPLE_NODE_PASSWORD},
]


def return_message(status_code, msg):
    return {
        'message': msg,
        'http_status': status_code,
    }


def get_docker_host():
    """
    Fetch the DOCKER_HOST environment variable and parse the IP.
    """

    # raw_dockerhost will return something like:
    # tcp://192.168.56.132:2376
    dockerhost = os.getenv('DOCKER_HOST', None)

    if dockerhost:
        return dockerhost.split(':')[-2].strip('//')
    else:
        return False


def get_provisioner_url(url='localhost'):
    """
    Try to construct the URL for provisioner based on
    number of input sources. Fall back to http://localhost:8080
    """
    env_url = os.getenv('PROV_URL', False)
    docker_host = get_docker_host()

    if env_url:
        url = env_url
    elif docker_host:
        url = docker_host

    # Add http if missing
    if not urlparse(url).scheme:
        url = 'http://{}'.format(url)

    # Append 8080 if localhost
    if docker_host or 'localhost' in url:
        url = '{}:8080'.format(url)

    return url


def create_task(
    ip=None,
    username=None,
    password=None,
    role=None,
    extra_vars=None,
    only_tags=None,
    provisioner_url=None,
):

    if ip and username and password and role:
        endpoint = '{}/job'.format(provisioner_url)
        payload = {
            'ip': ip,
            'username': username,
            'password': password,
            'role': role,
            'extra_vars': extra_vars,
            'only_tags': only_tags,
        }
        r = requests.post(endpoint, data=json.dumps(payload))
        return return_message(r.status_code, r.content)
    else:
        return return_message(400, 'Missing provisioner_url arguments.')


def get_roles(provisioner_url=None):
    if provisioner_url:
        endpoint = '{}/roles'.format(provisioner_url)
        r = requests.get(endpoint)
        return return_message(r.status_code, r.json())
    else:
        return return_message(400, 'Missing provisioner_url arguments.')


def get_jobs(provisioner_url=None):
    if provisioner_url:
        endpoint = '{}/job'.format(provisioner_url)
        r = requests.get(endpoint)
        return return_message(r.status_code, r.json())
    else:
        return return_message(400, 'Missing provisioner_url arguments.')


def get_status(
    uuid=None,
    provisioner_url=None,
):
    if uuid and provisioner_url:
        endpoint = '{}/job/{}'.format(provisioner_url, uuid)
        r = requests.get(endpoint)
        return return_message(r.status_code, r.json())
    elif not uuid:
        return return_message(400, 'Missing UUIDs.')
    elif not provisioner_url:
        return return_message(400, 'Missing provisioner_url arguments.')


def abort_task(
    uuid=None,
    provisioner_url=None,
):
    if uuid:
        endpoint = '{}/job/{}'.format(provisioner_url, uuid)
        r = requests.delete(endpoint)
        return return_message(r.status_code, r.json)
    elif not uuid:
        return return_message(400, 'Missing UUIDs.')
    elif not provisioner_url:
        return return_message(400, 'Missing provisioner_url arguments.')


def get_redis_status(provisioner_url=None):
    if provisioner_url:
        endpoint = '{}/redis_status'.format(provisioner_url)
        r = requests.get(endpoint)
        return return_message(r.status_code, r.content)
    else:
        return return_message(400, 'Missing provisioner_url arguments.')
