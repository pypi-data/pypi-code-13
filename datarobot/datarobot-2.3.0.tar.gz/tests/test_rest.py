import json

import pytest
import responses

from datarobot import Project, AppPlatformError
from datarobot import errors
from .utils import SDKTestcase, assert_raised_regex


class Test400LevelErrors(SDKTestcase):

    @responses.activate
    def test_401_error_message(self):
        """For whatever reason, the `requests` library completely ignores the
        body in a 401 error, so, here is our own message
        """
        responses.add(
            responses.GET,
            'https://host_name.com/projects/',
            status=401,
        )

        with pytest.raises(AppPlatformError) as exc_info:
            Project.list()
        assert_raised_regex(exc_info, 'not properly authenticated')

    @responses.activate
    def test_403_error_message(self):
        """Same deal here, the `requests` library completely ignores the
        body in a 403 error, so, here is our own message
        """
        responses.add(
            responses.GET,
            'https://host_name.com/projects/',
            status=403,
        )

        with pytest.raises(AppPlatformError) as exc_info:
            Project.list()
        assert_raised_regex(exc_info, 'permissions')

    @responses.activate
    def test_model_already_added_exception(self):
        responses.add(
            responses.POST,
            'https://host_name.com/projects/p-id/models/',
            status=422,
            body=json.dumps({'message': u'Model already added', 'errorName': u'JobAlreadyAdded'})
        )

        with pytest.raises(errors.JobAlreadyRequested):
            Project('p-id').train('some-blueprint-id')

    @responses.activate
    def test_extracts_error_message(self):
        data = {'message': 'project p-id has been deleted'}
        responses.add(responses.GET, 'https://host_name.com/projects/p-id/models/',
                      status=422,
                      body=json.dumps(data),
                      content_type='application/json')

        with pytest.raises(AppPlatformError) as exc_info:
            Project('p-id').get_models()
        assert_raised_regex(exc_info, 'project p-id has been deleted')
