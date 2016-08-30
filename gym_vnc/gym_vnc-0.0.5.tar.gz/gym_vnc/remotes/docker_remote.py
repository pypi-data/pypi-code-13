from __future__ import absolute_import

import base64
import docker
import json
import logging
import os
import pipes
import six.moves.urllib.parse as urlparse
import subprocess
import sys
import threading
import uuid

from gym_vnc.remotes import healthcheck
from gym_vnc.remotes.compose import container, log_printer, progress_stream

from gym_vnc import error
from gym.utils import closer

logger = logging.getLogger(__name__)

docker_closer = closer.Closer()

def random_alphanumeric(length=14):
    buf = []
    while len(buf) < length:
        entropy = base64.encodestring(uuid.uuid4().bytes)
        bytes = [c for c in entropy if c.isalnum()]
        buf += bytes
    return ''.join(buf)[:length]

class Docker(object):
    def __init__(self, image, command=None, n=1):
        self.n = n
        self._allocator = Allocator()
        self.instances = [DockerInstance(self._allocator, image=image, command=command, label=i) for i in range(n)]

    def start(self):
        [instance.start() for instance in self.instances]
        self.start_logging()
        self.healthcheck()

    def close(self):
        [instance.close() for instance in self.instances]

    def connection_strings(self):
        return [instance.connection_string() for instance in self.instances]

    def start_logging(self):
        containers = [instance._container for instance in self.instances]
        labels = [str(instance.label) for instance in self.instances]
        log_printer.build(containers, labels)

    def healthcheck(self):
        # Wait for boot
        healthcheck.run(
            ['{}:{}'.format(instance.allocator.info['host'], instance.vnc_port) for instance in self.instances],
            ['{}:{}'.format(instance.allocator.info['host'], instance.rewarder_port) for instance in self.instances]
        )

def get_client():
    info = {}
    host = os.environ.get('DOCKER_HOST')

    client_api_version = os.environ.get('DOCKER_API_VERSION')

    # IP to use for started containers
    if host:
        info['host'] = urlparse.urlparse(host).netloc.split(':')[0]
    else:
        info['host'] = 'localhost'

    verify = os.environ.get('DOCKER_TLS_VERIFY') == '1'
    if verify: # use TLS
        assert_hostname = None
        cert_path = os.environ.get('DOCKER_CERT_PATH')
        if cert_path:
            client_cert = (os.path.join(cert_path, 'cert.pem'), os.path.join(cert_path, 'key.pem'))
            ca_cert = os.path.join(cert_path, 'ca.pem')
        else:
            client_cert = ca_cert = None

        tls_config = docker.tls.TLSConfig(
            client_cert=client_cert,
            ca_cert=ca_cert,
            verify=verify,
            assert_hostname=assert_hostname,
        )
        return docker.Client(base_url=host, tls=tls_config, version=client_api_version), info
    else:
        return docker.Client(base_url=host, version=client_api_version), info

class Allocator(object):
    def __init__(self):
        self.instance_id = 'gym-vnc-' + random_alphanumeric(length=6)
        self.client, self.info = get_client()
        self._refresh_ports()

    def _refresh_ports(self):
        ports = set()
        for container in self.client.containers():
            for port in container['Ports']:
                # {u'IP': u'0.0.0.0', u'Type': u'tcp', u'PublicPort': 5000, u'PrivatePort': 500}
                if port['Type'] == 'tcp' and 'PublicPort' in port:
                    ports.add(port['PublicPort'])
        self._ports = ports
        self._next_port = 10000

    def allocate_ports(self, num):
        while self._next_port in self._ports or (self._next_port+1) in self._ports:
            self._next_port += 1

        # Allocate two ports
        res = (self._next_port, self._next_port+1)
        self._next_port += 2

        return res

def pretty_command(command):
    return ' '.join(pipes.quote(c) for c in command)

class DockerInstance(object):
    def __init__(self, allocator, image, command=None, label='main'):
        self._docker_closer_id = docker_closer.register(self)

        self.label = label
        self.allocator = allocator
        self.image = image
        self.command = command or []

        self._container_id = None
        self._closed = False

        self._container = None

        self.vnc_port = None
        self.rewarder_port = None

    def connection_string(self):
        host = self.allocator.info['host']
        return '{}:{}+{}'.format(host, self.vnc_port, self.rewarder_port)

    def start(self, attempts=5):
        for attempt in range(attempts):
            self._spawn()
            e = self._start()
            if e is None:
                return
        raise error.Error('[{}] Could not start container after {} attempts. Last error: {}'.format(self.label, attempts, e))

    def _cmdline(self):
        return ['docker', 'run',
                '-p', '{}:5900'.format(self.vnc_port),
                '-p', '{}:15900'.format(self.rewarder_port),
                self.image] + self.command

    def _spawn(self):
        if self.image is None:
            raise error.Error('No image specified')
        assert self._container_id is None

        self.vnc_port, self.rewarder_port = self.allocator.allocate_ports(2)
        logger.info('[%s] Creating container: image=%s command=%s. Run the same thing by hand as: %s', self.label, self.image, self.command, pretty_command(self._cmdline()))

        try:
            container = self._spawn_container()
        except docker.errors.NotFound as e:
            # Looks like we need to pull the image
            assert 'No such image' in e.explanation, 'Expected NotFound error message message to include "No such image", but it was: {}. This is probably just a bug in this assertion and the assumption was incorrect'.format(e.explanation)

            logger.info('Image %s not present locally; pulling', self.image)
            self._pull_image()
            # Try spawning again
            container = self._spawn_container()

        self._container_id = container['Id']

    def _pull_image(self):
        output = self.client.pull(self.image, stream=True)
        return progress_stream.get_digest_from_pull(
            progress_stream.stream_output(output, sys.stdout))

        # docker-compose uses this:
        # try:
        # except StreamOutputError as e:
        #     if not ignore_pull_failures:
        #         raise
        #     else:
        #         log.error(six.text_type(e))


    def _spawn_container(self):
        # launch instance, and refresh if error
        container = self.client.create_container(
            image=self.image,
            command=self.command,
            name='{}-{}'.format(self.allocator.instance_id, self.label),
            host_config=self.client.create_host_config(
                port_bindings={
                    5900: self.vnc_port,
                    15900: self.rewarder_port,
                },
            ),
            labels={
                'com.openai.automanaged': 'true',
            }
        )
        return container

    def _start(self):
        logger.debug('[%s] Starting container: id=%s', self.label, self._container_id)
        try:
            self.client.start(container=self._container_id)
        except docker.errors.APIError as e:
            if 'port is already allocated' in e.explanation:
                logger.info('[%s] Could not start container: %s', self.label, e)
                self._remove()
                return e
            else:
                raise
        else:
            self._container = container.Container.from_id(self.client, self._container_id)
            return None

    def _remove(self):
        logger.info("Killing and removing container: id=%s. (If this command errors, you can always kill all automanaged environments on this Docker daemon via: docker rm -f $(docker ps -q -a -f 'label=com.openai.automanaged=true')", self._container_id)
        self.client.remove_container(container=self._container_id, force=True)
        self._container_id = None

    def __del__(self):
        self.close()

    def close(self):
        if self._closed:
            return

        docker_closer.unregister(self._docker_closer_id)

        # Make sure it's actually started
        if self._container_id:
            self._remove()

        self._closed = True

    @property
    def client(self):
        return self.allocator.client

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)

    # docker run --name test --rm -ti -p 5900:5900 -p 15900:15900 quay.io/openai/vnc-core-envs
    instance = Docker(
        image='quay.io/openai/vnc-core-envs',
        command=['-o'],
        n=2,
    )
    instance.start()
    import ipdb;ipdb.set_trace()
