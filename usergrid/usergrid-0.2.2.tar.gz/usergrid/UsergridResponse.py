import json


# Error Example:
# {
# "error": "duplicate_unique_property_exists",
# "timestamp": 1471716304262,
# "duration": 0,
# "error_description": "Entity \"list\" requires that property named \"name\" be unique, value of pinguser_312187980816-default exists",
# "exception": "org.apache.usergrid.persistence.exceptions.DuplicateUniquePropertyExistsException"
# }

class UsergridResponse:
    def __init__(self, r):
        self.r = r
        self.status_code = r.status_code
        self.error = None
        self.error_description = None
        self.exception = None
        self.response = None

        try:
            self.response = json.loads(r.text)
        except:
            self.response = {}
            pass

        if self.status_code == 200:
            self.entity_array = self.response.get('entities', [])
        else:
            self.response = {}
            self.entity_array = []
            self.error = self.response.get('error', 'not available')
            self.error_description = self.response.get('error_description', 'not available')
            self.exception = self.response.get('exception', 'not available')

    def is_success(self):
        return 200 <= self.status_code < 300

    def is_error(self):
        return 300 <= self.status_code

    def is_user_error(self):
        return 400 <= self.status_code < 500

    def is_server_error(self):
        return 500 <= self.status_code < 600

    def first(self):
        if not self.is_error() and len(self.entity_array) > 0:
            return self.entity_array[0]
        else:
            return None

    def error_message(self):
        return '%s: %s' % (self.error, self.error_description)
