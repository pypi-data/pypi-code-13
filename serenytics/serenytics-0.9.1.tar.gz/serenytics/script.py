import json
import logging
from copy import deepcopy

import time

from .helpers import SerenyticsException, make_request
from . import settings

logger = logging.getLogger(__name__)


class UnknownScript(SerenyticsException):
    def __init__(self, uuid_or_name):
        super(UnknownScript, self).__init__(u'Script with uuid or name "{}" does not exist'.format(uuid_or_name))


class Script(object):
    """
    Serenytics script
    """

    def __init__(self, config, headers):
        self._config = config
        self._headers = headers

    @property
    def name(self):
        return self._config['name']

    @property
    def uuid(self):
        return self._config['uuid']

    def run(self, params=None, async=True):
        """
        Run script

        :param params: Parameters to pass to the script execution
        :type params: dict

        :param async: Whether this call waits for the script execution to be finished.

        :returns None if async=True. If async=False, returns a dict containing information on the script execution
            - execution_status (either "SUCCESS" or "FAILURE")
            - stdout
            - stderr
            - return_code
        """
        run_url = settings.SERENYTICS_API_DOMAIN + '/api/script/' + self.uuid + '/run'
        script_params = deepcopy(params or {})

        # always run with async=True and then poll manually if result is needed synchronously
        # because using async=True on http request is limited to 5 minutes
        script_params['async'] = True
        make_request('post', run_url, data=json.dumps(script_params), headers=self._headers,
                     expected_json_status='ok')

        if not async:
            self.wait()
            logs = self.get_last_logs()
            result = logs[0]
            return {
                'execution_status': result['status'],
                'stdout': result['stdout'],
                'stderr': result['stderr'],
                'return_code': result['return_code']
            }

    def wait(self, time_before_retry_s=1):
        """
        Wait for script execution to be finished
        """
        while True:
            running = self.is_running()
            if not running:
                break
            time.sleep(time_before_retry_s)

    def is_running(self):
        """
        :return: Whether the current script is running
        """
        state_url = settings.SERENYTICS_API_DOMAIN + '/api/script/' + self.uuid + '/state'
        response = make_request('get', state_url, headers=self._headers)
        return response.json()['running']

    def get_last_logs(self):
        """
        Fetch last 10 logs
        :return:
        """
        logs_url = settings.SERENYTICS_API_DOMAIN + '/api/script/' + self.uuid + '/logs'
        response = make_request('get', logs_url, headers=self._headers)
        return response.json()['objects']
