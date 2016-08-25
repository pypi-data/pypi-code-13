import logging

from bwc_cli.common import command


class ShowConfigBGP(command.Command):
    """Display Fabric configuration for the specified Fabric"""

    ref_or_id = 'bwc-topology.show_config_bgp'
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ShowConfigBGP, self).get_parser(prog_name)
        list_group = parser.add_mutually_exclusive_group(required=True)
        list_group.add_argument(
            '--host',
            default=None,
            help='IP of the device to be listed',
        )
        list_group.add_argument(
            '--fabric',
            default=None,
            help='Name of the fabric to list all devices',
        )
        return parser

    def take_action(self, parsed_args):
        result_json = parsed_args.result
        result = result_json['result']
        print('Show BGP Configuration')
        self.log.info(result)


class ShowTopology(command.Command):
    """Generates Topology for the specified Fabric"""

    ref_or_id = 'bwc-topology.topology_generate'
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(ShowTopology, self).get_parser(prog_name)
        parser.add_argument(
            'fabric',
            metavar='<fabric>',
            default='default',
            help='Fabric name for which topology will be displayed',
        )

        parser.add_argument(
            '--format',
            metavar='<format>',
            default='pdf',
            help='Format of the file to generate for the topology',
        )
        parser.add_argument(
            '--render_dir',
            metavar='<render_dir>',
            default='/tmp',
            help='Path where the topology file will be saved',
        )

        return parser

    def take_action(self, parsed_args):
        result_json = parsed_args.result
        result = result_json['result']
        self.log.info('Show Topology')
        print(result)
