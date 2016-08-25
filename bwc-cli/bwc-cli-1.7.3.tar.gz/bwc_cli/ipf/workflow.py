import logging

from bwc_cli.common import command


class WorkflowBGP(command.Command):
    """Execute the IP Fabric Workflow and display the details"""

    ref_or_id = 'bwc-ipfabric.configure_fabric'
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(WorkflowBGP, self).get_parser(prog_name)
        parser.add_argument(
            'fabric',
            metavar='<fabric>',
            help='Fabric on which the BGP workflow will be executed',
        )
        return parser

    def take_action(self, parsed_args):
        # The response of this is tricky. The last step in the Workflow is what
        # we will display.
        # Success or Failure will be done for the last set of the workflow.
        self.log.info('IP Fabric Workflow')
        print 'Workflow:', parsed_args.ref_or_id
        print 'Status:', parsed_args.execution_status
        print 'Id:', parsed_args.execution_id
        result_json = parsed_args.result
        tasks = result_json['tasks']
        final_task = tasks[-1]
        print final_task['result']['result']
