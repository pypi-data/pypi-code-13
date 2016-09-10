# -*- coding: utf-8 -*-
"""
This is a very unofficial SDK for interacting with HackerRank for Work.
This was developed as a result of really bad, customer-facing, API support from HR.
Development of this has been an exercise in reverse-engineering. I have been use a proxy
in order to sniff requests made to HR and have used deductive logic to determine what
values are allowed, etc.

Use at your own risk
"""
import requests
from pypandoc import convert_file 
import json
from urlparse import urljoin

class HackerRankAuthError(Exception):
    pass

class HackerRankValueError(Exception):
    pass

class HackerRankClient(object):
    def __init__(self, token):
        self.headers = {'Content-Type' : 'application/json'} 
        self.base_url = 'https://www.hackerrank.com/x/api/v1/'
        self.query_string = {'access_token': token}
        self.validate_auth()

    def validate_auth(self):
        """Validates token by doing a GET for timezones which any kind of user should have access to"""
        endpoint = urljoin(self.base_url, 'users/timezones')
        test_req = requests.get(endpoint, params=self.query_string, headers=self.headers) 
        resp = test_req.json()
        try:
            if 'Invalid' in resp['message']:
                raise HackerRankAuthError("Invalid Access Token specified") 
        except KeyError:
            # No error
            pass

    def _caller(self, endpoint, query_string=None, data=None, headers=None, method='GET'):
        url = urljoin(self.base_url, endpoint)
        if query_string:
            self.query_string.update(query_string)

        if headers:
            self.headers.update(headers)

        if not data:
            data = dict()

        if method == 'POST':
            r = requests.post(url, params=self.query_string, data=data, headers=self.headers)
        elif method == 'PUT':
            r = requests.put(url, params=self.query_string, data=data, headers=self.headers)
        elif method == 'GET':
            r = requests.get(url, params=self.query_string, headers=self.headers)

        try:
            return r.json()
        except ValueError:
            return r.status_code


    def get_tests_list(self):
        """Get all the tests"""
        params = dict(access='live', limit=100)
        endpoint = 'tests'
        return self._caller(endpoint, query_string=params)


    def get_test(self, test_id):
        """ Retrieve a test object by id"""
        endpoint = 'tests/%s' % test_id
        return self._caller(endpoint)


    def create_test(self, name, duration):
        """
        Create a test object
        args:
            name: the name of the test, type: str
            duration: the duration, in minutes, of the test, type: int
        """
        endpoint = 'tests'
        create_data = dict(name=name, duration=duration)
        test_id = self._caller(endpoint, method="POST", data=json.dumps(create_data))

        get_test_endpoint = 'tests/%s' % test_id

        return self._caller(get_test_endpoint)


    def update_test(self, test_id, data, purge_tags=True):
        """
        # Note that other kwargs may still work, these are simply the ones that have been tested
        VALID KWARGS:
            key: name, val_type: string, desc: The name you want the test to have.
            key: instructions, val_type: string, desc: The instructions for the test
            key: duration, val_type: integer, desc: The number, in mintues, of the test time limit
            key: purge_tags, val_type: boolean, desc: When 'tags' in 'data' whether to add to existing tags or purge current tags
            key: collect_candidate_details, val_type: list, desc: The info you wish to collect from a candidate. Valid values are: full_name, work_experience, city, roll_number, email_address, year_of_graduation, cgpa, gpa, univ, phone_number, contact_recruiter, branch, major, degree, gender, role, resume, pgdegree, city_graduation
            key: custom_acknowledge_text, val_type: str, desc: Any statement you wish candidates to acknowledge prior to commencing a test
            key: test_admins, val_type: str, desc: the email address of the test administrator
            key: sudorank_setupscript, val_type: str, desc: the setup script to run to bootstrap test VMs for SudoRank questions
            key: sudorank_disable_check_agent, val_type: str, desc: sets up the Hacker Rank checking agent which allows for VMs to still be graded even if candidates leave the machine in an unreachable state
        """
        endpoint = 'tests/%s' % test_id

        if 'custom_acknowledge_text' in data.keys():
            data['enable_acknowledgement'] = True

        if not purge_tags and 'tags' in data.keys():
            current_test = self.get_test(test_id)
            data['tags'] += current_test['data']['tags']
            # If purge_tags is true when can just leave the normal behavior which is to purge when PUT

        if 'collect_info' in data.keys():
            data['collect_info'] = '|'.join(data['collect_info'])

        if 'sudorank_os' in data.keys():
            if data['sudorank_os'] not in ('rhel7', 'ubuntu'):
                #TODO: Validation for when questions require RH OS and a user attempts to update the os value to ubuntu
                raise HackerRankValueError("You specified a bad OS option, only 'rhel7' and 'ubuntu' are valid options")

        return self._caller(endpoint, method='PUT', data=json.dumps(data))


    def get_all_questions(self, question_type='all', qfilter='sudorank'):
        """
        Get all the questions available to the authenticated account

        key: question_type, type: str, desc: Whether to get personal, hackerrank, or all questions
        key: qfilter, type: str, desc: What type of questions to get. It can only be one value. Valid values are sudorank, coding, database, design (aka Front End), android, project (aka Java Project), multiple (Generic multiple choice), text (Subjective), and diagram
        """
        # Yes, 'undefined' is actually a part of the URI
        endpoint = 'tests/undefined/library'
        valid_question_types = [
            'sudorank',
            'coding',
            'database',
            'design',
            'android',
            'project',
            'multiple',
            'text',
            'diagram'
        ]
        questions = []
        if question_type in ('personal', 'all'):
            if qfilter == 'all':
                for qtype in valid_question_types:
                    p_query = dict(library='personal_all', filter=qtype)
                    personal_questions = self._caller(endpoint, query_string=p_query)['model']['questions']
                    questions += personal_questions
            else:
                p_query = dict(library='personal_all', filter=qfilter)
                personal_questions = self._caller(endpoint, query_string=p_query)['model']['questions']
                questions += personal_questions

        if question_type in ('hackerrank', 'all'):
            if qfilter == 'all':
                for qtype in valid_question_types:
                    hr_query = dict(library='hackerrank', filter=qtype)
                    personal_questions = self._caller(endpoint, query_string=hr_query)['model']['questions']
                    questions += personal_questions
            else:
                hr_query = dict(library='hackerrank', filter=qfilter)
                hr_questions = self._caller(endpoint, query_string=hr_query)['model']['questions']
                questions += hr_questions

        return questions


    def create_question(self, test_id, **kwargs):
        """
        Create a question on a test in HackerRank.
        Required kwargs: name, type, question, score
        kwargs:
            key:type, val_type: string, desc: what kind of question is it, coding, sudorank, etc
            key:question, val_type: string, desc: html of the question description
            key:score, val_type: integer, desc: the score to give the question
            key:name, val_type: string, desc: the name of the question
            key:internal_notes, val_type: string, desc: any internal use only notes

            SUDORANK TYPE SPECIFIC KWARGS
            key:sudorank_os, val_type:string, desc:when type of sudorank, the os, whether rhel7 or agnostic
            key:visible_tags_array, val_type:list, desc:a list of tags for the question to have
            key:setup, val_type: string, desc: the setup script for the question
            key:solve, val_type: string, desc: the 'solution' script
            key:check, val_type: string, desc: the 'check' script
            key:cleanup, val_type: string, desc: any cleanup script

            CODING TYPE SPECIFIC KWARGS
            note that test cases are a different method
            key:allowedLanguages, val_type:string, desc: the languages you want to allow. Valid values are: c,clojure,cobol,cpp,csharp,d,erlang,fortran,fsharp,go,groovy,haskell,java,java8,javascript,lua,objectivec,ocaml,pascal,perl,php,python,python3,racket,ruby,rust,sbcl,scala,smalltalk,swift,visualbasic,r,bash,octave
            key:allowedLanguages, val_type:string, desc: the languages you want to allow. Valid values are: c,clojure,cobol,cpp,csharp,d,erlang,fortran,fsharp,go,groovy,haskell,java,java8,javascript,lua,objectivec,ocaml,pascal,perl,php,python,python3,racket,ruby,rust,sbcl,scala,smalltalk,swift,visualbasic,r,bash,octave
            >> NOTE: The below should be read dynamically, for example, $languageKey_template is not an actual valid value, but python_template is valid as is php_template. Use the allowedLanguages values from above as reference
            key: $languageKey_template, val_type:string, desc: the boilerplate code that you want candidates to be able to edit
            key: $languageKey_template_head, val_type:string, desc: the boilerplate code that is NOT editable by candidates that is to be prepended to the 'template' boilerplate
            key: $languageKey_template_tail, val_type:string, desc: the boilerplate code that is NOT editable by candidates that is to be appended to the 'template' boilerplate
        """
        endpoint = 'tests/%s/questions' % test_id
        create_data = dict(
            type=kwargs['type'],
            tid=test_id,
            name=kwargs['name'],
            score=kwargs['score'],
            visible_tags_array=kwargs['visible_tags_array'],
            internal_notes=kwargs['internal_notes'],
        )

        question_id = self._caller(endpoint, method='POST', data=json.dumps(create_data))['model']['id']
        # This is how the webapp does it, first does a minimal data POST, then a PUT
        self.update_question(test_id, question_id, **kwargs)


    def update_question(self, test_id, question_id, **kwargs):
        """
        Updates a pre-existing question in HackerRank
        kwargs:
            key:type, val_type: string, desc: what kind of question is it, coding, sudorank, etc
            key:question, val_type: string, desc: html of the question description
            key:score, val_type: integer, desc: the score to give the question
            key:name, val_type: string, desc: the name of the question
            key:visible_tags_array, val_type:list, desc:a list of tags for the question to have
            key:internal_notes, val_type: string, desc: any internal use only notes

            SUDORANK TYPE SPECIFIC KWARGS
            key:sudorank_os, val_type:string, desc:when type of sudorank, the os, whether rhel7 or agnostic
            key:visible_tags_array, val_type:list, desc:a list of tags for the question to have
            key:setup, val_type: string, desc: the setup script for the question
            key:solve, val_type: string, desc: the 'solution' script
            key:check, val_type: string, desc: the 'check' script
            key:cleanup, val_type: string, desc: any cleanup script

            CODING TYPE SPECIFIC KWARGS
            note that test cases are a different method
            key:allowedLanguages, val_type:string, desc: the languages you want to allow. Valid values are: c,clojure,cobol,cpp,csharp,d,erlang,fortran,fsharp,go,groovy,haskell,java,java8,javascript,lua,objectivec,ocaml,pascal,perl,php,python,python3,racket,ruby,rust,sbcl,scala,smalltalk,swift,visualbasic,r,bash,octave
            >> NOTE: The below should be read dynamically, for example, $languageKey_template is not an actual valid value, but python_template is valid as is php_template. Use the allowedLanguages values from above as reference
            key: $languageKey_template, val_type:string, desc: the boilerplate code that you want candidates to be able to edit
            key: $languageKey_template_head, val_type:string, desc: the boilerplate code that is NOT editable by candidates that is to be prepended to the 'template' boilerplate
            key: $languageKey_template_tail, val_type:string, desc: the boilerplate code that is NOT editable by candidates that is to be appended to the 'template' boilerplate
        """

        endpoint = 'tests/%s/questions/%s' % (test_id, question_id)
        #TODO Validate that the question is in-fact writeable by the authenticated user

        if kwargs['type'] == 'sudorank':
            kwargs['sudorank_scripts'] = dict()

            if 'setup' in kwargs.keys():
                kwargs['sudorank_scripts']['setup'] = kwargs.pop('setup')
            if 'solve' in kwargs.keys():
                kwargs['sudorank_scripts']['solve'] = kwargs.pop('solve')
            if 'check' in kwargs.keys():
                kwargs['sudorank_scripts']['check'] = kwargs.pop('check')
            if 'cleanup' in kwargs.keys():
                kwargs['sudorank_scripts']['cleanup'] = kwargs.pop('cleanup')

        return self._caller(endpoint, method='PUT', data=json.dumps(kwargs))


    def get_test_cases(self, test_id, question_id):
        """ Get all the current test cases for a particular question"""  
        endpoint = 'tests/%s/questions/%s/testcases' % (test_id, question_id)
        return self._caller(endpoint)['models']


    def update_test_case(self, test_id, question_id, test_case_id, **kwargs):
        """ 
        Updates a test case for a coding type question 
        kwargs:
            name: The name that the test case should have, type: string
            sample: whether to mark this as a sample test case, type: boolean
            type: one of Easy, Medium, or Hard
            score: the value of the test case, type: integer
            input: that which should be inputed to the test case
            output: the expected output of the test case
        """

        endpoint = 'tests/%s/questions/%s/testcases/%s' % (test_id, question_id, test_case_id)
        kwargs['id'] = test_case_id
        return self._caller(endpoint, method="PUT", data=json.dumps(kwargs))


