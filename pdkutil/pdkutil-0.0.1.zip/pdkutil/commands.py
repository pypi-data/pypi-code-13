# Copyright 2016 Cloudbase Solutions Srl
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import logging

from barbicanclient import barbican as barbican_client
from cliff.show import ShowOne
from cliff.command import Command
import pdkutil


class Get(ShowOne):
    "Retrieve a container ref by specifying the container name"

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(Get, self).get_parser(prog_name)
        pdkutil.PDKUtil().build_parser(parser)
        parser.add_argument('container_reference',
                             metavar='<container-reference>')
        return parser

    def take_action(self, parsed_args):
        barbican = pdkutil.PDKUtil().create_client(parsed_args)
        columns = ('Reference',
                   'Name',
                   )
        data = (parsed_args.container_reference,
                'This container does not exist.',
                )
        for container in barbican.containers.list():
            if parsed_args.container_reference == container.container_ref:
                columns = ('Reference',
                           'Name',
                           'Created',
                           'Status',
                           'Secrets'
                           )
                data = (container.container_ref,
                        container.name,
                        container.created,
                        container.status,
                        '\n'.join(value.secret_ref for key, value in container.secrets.items())
                        )
        return (columns, data)


class Store(ShowOne):
    "Stores a file to a barbican container."

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(Store, self).get_parser(prog_name)
        pdkutil.PDKUtil().build_parser(parser)
        parser.add_argument('filename',
                            metavar='<filename>')
        parser.add_argument('container_name',
                            metavar='<container-name>')
        return parser

    def read_in_chunks(self, file_object, chunk_size=1000):
        while True:
            data = file_object.read(chunk_size)
            if not data:
                break
            yield data

    def take_action(self, parsed_args):
        barbican = pdkutil.PDKUtil().create_client(parsed_args)
        my_container = barbican.containers.create(
            name=parsed_args.container_name)
        f = open(parsed_args.filename, 'rb')
        secret_number = 1
        for piece in self.read_in_chunks(f):
            secret_payload = piece
            secret = barbican.secrets.create(
                name=u'Secret ' + str(secret_number), payload=secret_payload)
            secret_reference = secret.store()
            my_container.add(str(secret_number),
                barbican.secrets.get(secret_reference))
            secret_number+=1
        container_reference = my_container.store()

        columns = ('PDK_file',
                   'Container_name',
                   'Container_reference',
                   )
        data = (parsed_args.filename,
                parsed_args.container_name,
                container_reference,
                )
        return (columns, data)
