import os
import json

from gbdx_cloud_harness.test.conftest import my_vcr
from gbdx_cloud_harness.workflow import Workflow


def test_json_build(TestApp, mock_auth):
    TestApp.task.run_name = 'Workflow_test'
    wf_obj = Workflow(TestApp.task, auth=mock_auth)
    wf_json = wf_obj._build_worklfow_json()

    tasks = wf_json['tasks']

    assert len(tasks) == 2

    custom_task_name = None
    custom_task_output_names = None

    for task in tasks:

        if task['taskType'] == 'MyCustomTask':
            inputs = task['inputs']
            outputs = task['outputs']
            assert len(inputs), 3
            assert len(outputs), 1
            custom_task_name = task['name']
            custom_task_output_names = [p['name'] for p in task['outputs']]
        elif task['taskType'] == 'StageDataToS3':
            inputs = task['inputs']
            assert len(inputs), 2

            parsed_s3_loc = [x['value'].split('/')[2:] for x in inputs if x['name'] == 'destination'][0]
            exp_names = ['not_provided', 'not_provided', 'Workflow_test', 'output_port']
            assert exp_names == parsed_s3_loc

            parsed_source = [x['source'].split(':') for x in inputs if x['name'] == 'data'][0]
            assert parsed_source[0] == custom_task_name
            assert True if parsed_source[1] in custom_task_output_names else False
        else:
            assert False  # Fail test


@my_vcr.use_cassette('gbdx_cloud_harness/test/vcr_cassettes/workflow.yaml', filter_headers=['authorization'])
def test_execute_workflow(TestApp, test_path, mock_auth):

    test_wf_file = os.path.join(test_path, 'test_valid_wf.json')

    vcr_filename = os.path.join(
        test_path, 'vcr_cassettes', 'workflow.yaml'
    )

    if os.path.isfile(vcr_filename):
        wf_obj = Workflow(TestApp.task, auth=mock_auth)
    else:
        wf_obj = Workflow(TestApp.task)

    with open(test_wf_file, 'r') as f:
        wf_json = f.read()
        print(wf_json)
        wf_obj.execute(override_wf_json=json.loads(wf_json))

    assert wf_obj.id is not None
    assert isinstance(int(wf_obj.id), int)
    assert wf_obj.status['state'] == 'pending'
    assert wf_obj.status['event'] == 'submitted'

    assert wf_obj.succeeded is False
    assert wf_obj.complete is False

    wf_obj.id = '4392617339332738708'  # A completed workflow
    wf_obj._refresh_status()

    assert wf_obj.succeeded is True
    assert wf_obj.complete is True
