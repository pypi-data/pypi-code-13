from textwrap import dedent
from warnings import warn

from nose.plugins import Plugin
from testrail import TestRail

class TestRailReporter(Plugin):
    '''TODO: fill this out -- it's used as the help in nosetests -h for
    --with-testrailreporter'''

    def addError(test, err):
        self._collect_result(test, self.error_id)

    def addFailure(test, err):
        self._collect_result(test, 5)

    def addSkipped(test):
        self._collect_result(test, self.skip_id)

    def addSuccess(test):
        self._collect_result(test, 1)

    def begin(self):
        self.results = dict()
        if self.client is not None:
            self._existing_cases    = self._build_cases()
            self._existing_sections = self._build_sections()

    def configure(self, options, conf):
        self.api_key    = options.testrail_api_key
        self.email      = options.testrail_email
        self.error_id   = int(options.testrail_error_id or 5)
        self.project_id = int(options.testrail_project_id or 0)
        self.run_name   = options.testrail_run_name
        self.skip_id    = int(options.testrail_skip_id or 1)
        self.suite_id   = int(options.testrail_suite_id or 1)
        self.url        = options.testrail_url

        if self.url and self.email and self.api_key and self.run_name:
            self.client = TestRail(project_id=self.project_id, email=self.email,
                                   key=self.api_key, url=self.url)
        else:
            self.client = None
            warn(dedent('''
                !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                ! THIS RUN WILL NOT BE REPORTED TO TESTRAIL !
                !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                You specified --with-testrailreporter. This requires the
                following options:
                --testrail_api_key  current value: {}
                --testrail_email    current value: {}
                --testrail_run_name current value: {}
                --testrail_url      current value: {}
                '''.format(self.run_name, self.api_key, self.email, self.url)))

    def options(self, parser, env):
        super(TestRailReporter, self).options(parser, env)

        # TODO: Add help strings to all of these
        parser.add_option('--testrail_api_key',    dest='testrail_api_key')
        parser.add_option('--testrail_email',      dest='testrail_email')
        parser.add_option('--testrail_error_id',   dest='testrail_error_id')
        parser.add_option('--testrail_project_id', dest='testrail_project_id')
        parser.add_option('--testrail_run_name',   dest='testrail_run_name')
        parser.add_option('--testrail_skip_id',    dest='testrail_skip_id')
        parser.add_option('--testrail_suite_id',   dest='testrail_suite_id')
        parser.add_option('--testrail_url',        dest='testrail_url')

    def _build_cases(self):
        returned_cases = dict()
        raw_cases = self.client.api.cases(suite_id=self.suite_id)
        for case in raw_cases:
            returned_cases[case['title']] = dict(case_id=case['id'],
                                                 section_id=case['section_id'])
        return returned_cases

    def _build_results(self, run_id):
        tests = self._build_tests(run_id)
        returned_results = list()
        for case_id in tests.keys():
            if self.results.get(case_id, None) is not None:
                returned_results.append(dict(test_id=tests[case_id]['test_id'],
                                             status_id=self.results[case_id]))
        return returned_results

    def _build_sections(self):
        returned_sections = dict()
        raw_sections = self.client.api.sections(project_id=self.project_id,
                                                suite_id=self.suite_id)
        for section in raw_sections:
            returned_sections[section['name']] = dict(section_id=section['id'])
        return returned_sections

    def _build_tests(self, run_id):
        returned_tests = dict()
        raw_tests = self.client.api.tests(run_id)
        for test in raw_tests:
            returned_tests[test['case_id']] = dict(test_id=test['id'])
        return returned_tests

    def _create_case(self, case, section_id):
        payload = dict(section_id=section_id, title=case)
        response = self.client.api.add_case(payload)
        case_id = response['id']
        self.existing_cases[case] = dict(case_id=case_id, section_id=section_id)
        return case_id

    def _create_section(self, name):
        payload = dict(project_id=self.project_id, suite_id=self.suite_id,
                       name=name)
        response = self.client.api.add_section(payload)
        section_id = response['id']
        self.existing_sections[name] = dict(section_id=section_id)
        return section_id

    def _fetch_run_id(self):
        raw_runs = self.client.api.runs(self.project_id)
        for run in raw_runs:
            if self.run_name == run['name']:
                return run['id']

        payload  = dict(project_id=self.project_id, suite_id=self.suite_id,
                        name=self.run_name)
        response = self.client.api.add_run(payload)
        return response['id']

    def _collect_result(self, test, status_id):
        # TODO: figure out how to rip the data used below out of incoming "test"
        if case in self.existing_cases.keys():
            case_id = self.existing_cases[case]['case_id']
        else:
            section = section.split('.')[1].replace('test_', '')
            if section not in self.existing_sections.keys():
                section_id = self._create_section(name=section)
            else:
                section_id = self.existing_sections[section]['section_id']
            case_id = self._create_case(case, section_id)

        if test_passed:
            status_id = 1
        else:
            self.close_run = False
            status_id = 5
        self.results[case_id] = status_id

    def _publish_run(self):
        run_id = self._fetch_run_id()
        results = self._build_results(run_id)
        self.client.api.add_results(results, run_id)
        if self.close_run:
            self.client.api.close_run(run_id)
