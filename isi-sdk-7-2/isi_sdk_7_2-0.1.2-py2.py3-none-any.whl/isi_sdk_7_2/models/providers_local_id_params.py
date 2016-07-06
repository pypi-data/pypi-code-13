# coding: utf-8

"""
Copyright 2016 SmartBear Software

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

    Ref: https://github.com/swagger-api/swagger-codegen
"""

from pprint import pformat
from six import iteritems
import re


class ProvidersLocalIdParams(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        ProvidersLocalIdParams - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'authentication': 'bool',
            'create_home_directory': 'bool',
            'home_directory_template': 'str',
            'lockout_duration': 'int',
            'lockout_threshold': 'int',
            'lockout_window': 'int',
            'login_shell': 'str',
            'machine_name': 'str',
            'max_password_age': 'int',
            'min_password_age': 'int',
            'min_password_length': 'int',
            'name': 'str',
            'password_complexity': 'list[str]',
            'password_history_length': 'int',
            'password_prompt_time': 'int'
        }

        self.attribute_map = {
            'authentication': 'authentication',
            'create_home_directory': 'create_home_directory',
            'home_directory_template': 'home_directory_template',
            'lockout_duration': 'lockout_duration',
            'lockout_threshold': 'lockout_threshold',
            'lockout_window': 'lockout_window',
            'login_shell': 'login_shell',
            'machine_name': 'machine_name',
            'max_password_age': 'max_password_age',
            'min_password_age': 'min_password_age',
            'min_password_length': 'min_password_length',
            'name': 'name',
            'password_complexity': 'password_complexity',
            'password_history_length': 'password_history_length',
            'password_prompt_time': 'password_prompt_time'
        }

        self._authentication = None
        self._create_home_directory = None
        self._home_directory_template = None
        self._lockout_duration = None
        self._lockout_threshold = None
        self._lockout_window = None
        self._login_shell = None
        self._machine_name = None
        self._max_password_age = None
        self._min_password_age = None
        self._min_password_length = None
        self._name = None
        self._password_complexity = None
        self._password_history_length = None
        self._password_prompt_time = None

    @property
    def authentication(self):
        """
        Gets the authentication of this ProvidersLocalIdParams.
        Enables use of provider for authentication as well as identity.

        :return: The authentication of this ProvidersLocalIdParams.
        :rtype: bool
        """
        return self._authentication

    @authentication.setter
    def authentication(self, authentication):
        """
        Sets the authentication of this ProvidersLocalIdParams.
        Enables use of provider for authentication as well as identity.

        :param authentication: The authentication of this ProvidersLocalIdParams.
        :type: bool
        """
        
        self._authentication = authentication

    @property
    def create_home_directory(self):
        """
        Gets the create_home_directory of this ProvidersLocalIdParams.
        Automatically create home directory on first login.

        :return: The create_home_directory of this ProvidersLocalIdParams.
        :rtype: bool
        """
        return self._create_home_directory

    @create_home_directory.setter
    def create_home_directory(self, create_home_directory):
        """
        Sets the create_home_directory of this ProvidersLocalIdParams.
        Automatically create home directory on first login.

        :param create_home_directory: The create_home_directory of this ProvidersLocalIdParams.
        :type: bool
        """
        
        self._create_home_directory = create_home_directory

    @property
    def home_directory_template(self):
        """
        Gets the home_directory_template of this ProvidersLocalIdParams.
        Specifies home directory template path.

        :return: The home_directory_template of this ProvidersLocalIdParams.
        :rtype: str
        """
        return self._home_directory_template

    @home_directory_template.setter
    def home_directory_template(self, home_directory_template):
        """
        Sets the home_directory_template of this ProvidersLocalIdParams.
        Specifies home directory template path.

        :param home_directory_template: The home_directory_template of this ProvidersLocalIdParams.
        :type: str
        """
        
        self._home_directory_template = home_directory_template

    @property
    def lockout_duration(self):
        """
        Gets the lockout_duration of this ProvidersLocalIdParams.
        Sets length of time in seconds that an account will be inaccessible after multiple failed login attempts.

        :return: The lockout_duration of this ProvidersLocalIdParams.
        :rtype: int
        """
        return self._lockout_duration

    @lockout_duration.setter
    def lockout_duration(self, lockout_duration):
        """
        Sets the lockout_duration of this ProvidersLocalIdParams.
        Sets length of time in seconds that an account will be inaccessible after multiple failed login attempts.

        :param lockout_duration: The lockout_duration of this ProvidersLocalIdParams.
        :type: int
        """
        
        self._lockout_duration = lockout_duration

    @property
    def lockout_threshold(self):
        """
        Gets the lockout_threshold of this ProvidersLocalIdParams.
        Sets the number of failed login attempts necessary for an account to be locked out.

        :return: The lockout_threshold of this ProvidersLocalIdParams.
        :rtype: int
        """
        return self._lockout_threshold

    @lockout_threshold.setter
    def lockout_threshold(self, lockout_threshold):
        """
        Sets the lockout_threshold of this ProvidersLocalIdParams.
        Sets the number of failed login attempts necessary for an account to be locked out.

        :param lockout_threshold: The lockout_threshold of this ProvidersLocalIdParams.
        :type: int
        """
        
        self._lockout_threshold = lockout_threshold

    @property
    def lockout_window(self):
        """
        Gets the lockout_window of this ProvidersLocalIdParams.
        Sets the time in seconds in which lockout_threshold failed attempts must be made for an account to be locked out.

        :return: The lockout_window of this ProvidersLocalIdParams.
        :rtype: int
        """
        return self._lockout_window

    @lockout_window.setter
    def lockout_window(self, lockout_window):
        """
        Sets the lockout_window of this ProvidersLocalIdParams.
        Sets the time in seconds in which lockout_threshold failed attempts must be made for an account to be locked out.

        :param lockout_window: The lockout_window of this ProvidersLocalIdParams.
        :type: int
        """
        
        self._lockout_window = lockout_window

    @property
    def login_shell(self):
        """
        Gets the login_shell of this ProvidersLocalIdParams.
        Sets login shell path.

        :return: The login_shell of this ProvidersLocalIdParams.
        :rtype: str
        """
        return self._login_shell

    @login_shell.setter
    def login_shell(self, login_shell):
        """
        Sets the login_shell of this ProvidersLocalIdParams.
        Sets login shell path.

        :param login_shell: The login_shell of this ProvidersLocalIdParams.
        :type: str
        """
        
        self._login_shell = login_shell

    @property
    def machine_name(self):
        """
        Gets the machine_name of this ProvidersLocalIdParams.
        Specifies domain used to qualify user and group names for this provider.

        :return: The machine_name of this ProvidersLocalIdParams.
        :rtype: str
        """
        return self._machine_name

    @machine_name.setter
    def machine_name(self, machine_name):
        """
        Sets the machine_name of this ProvidersLocalIdParams.
        Specifies domain used to qualify user and group names for this provider.

        :param machine_name: The machine_name of this ProvidersLocalIdParams.
        :type: str
        """
        
        self._machine_name = machine_name

    @property
    def max_password_age(self):
        """
        Gets the max_password_age of this ProvidersLocalIdParams.
        Sets maximum password age in seconds.

        :return: The max_password_age of this ProvidersLocalIdParams.
        :rtype: int
        """
        return self._max_password_age

    @max_password_age.setter
    def max_password_age(self, max_password_age):
        """
        Sets the max_password_age of this ProvidersLocalIdParams.
        Sets maximum password age in seconds.

        :param max_password_age: The max_password_age of this ProvidersLocalIdParams.
        :type: int
        """
        
        self._max_password_age = max_password_age

    @property
    def min_password_age(self):
        """
        Gets the min_password_age of this ProvidersLocalIdParams.
        Sets minimum password age in seconds.

        :return: The min_password_age of this ProvidersLocalIdParams.
        :rtype: int
        """
        return self._min_password_age

    @min_password_age.setter
    def min_password_age(self, min_password_age):
        """
        Sets the min_password_age of this ProvidersLocalIdParams.
        Sets minimum password age in seconds.

        :param min_password_age: The min_password_age of this ProvidersLocalIdParams.
        :type: int
        """
        
        self._min_password_age = min_password_age

    @property
    def min_password_length(self):
        """
        Gets the min_password_length of this ProvidersLocalIdParams.
        Sets minimum password length.

        :return: The min_password_length of this ProvidersLocalIdParams.
        :rtype: int
        """
        return self._min_password_length

    @min_password_length.setter
    def min_password_length(self, min_password_length):
        """
        Sets the min_password_length of this ProvidersLocalIdParams.
        Sets minimum password length.

        :param min_password_length: The min_password_length of this ProvidersLocalIdParams.
        :type: int
        """
        
        self._min_password_length = min_password_length

    @property
    def name(self):
        """
        Gets the name of this ProvidersLocalIdParams.
        Specifies local provider name.

        :return: The name of this ProvidersLocalIdParams.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this ProvidersLocalIdParams.
        Specifies local provider name.

        :param name: The name of this ProvidersLocalIdParams.
        :type: str
        """
        
        self._name = name

    @property
    def password_complexity(self):
        """
        Gets the password_complexity of this ProvidersLocalIdParams.
        List of cases required in a password. Options are lowercase, uppercase, numeric and symbol

        :return: The password_complexity of this ProvidersLocalIdParams.
        :rtype: list[str]
        """
        return self._password_complexity

    @password_complexity.setter
    def password_complexity(self, password_complexity):
        """
        Sets the password_complexity of this ProvidersLocalIdParams.
        List of cases required in a password. Options are lowercase, uppercase, numeric and symbol

        :param password_complexity: The password_complexity of this ProvidersLocalIdParams.
        :type: list[str]
        """
        
        self._password_complexity = password_complexity

    @property
    def password_history_length(self):
        """
        Gets the password_history_length of this ProvidersLocalIdParams.
        The number of previous passwords to store.

        :return: The password_history_length of this ProvidersLocalIdParams.
        :rtype: int
        """
        return self._password_history_length

    @password_history_length.setter
    def password_history_length(self, password_history_length):
        """
        Sets the password_history_length of this ProvidersLocalIdParams.
        The number of previous passwords to store.

        :param password_history_length: The password_history_length of this ProvidersLocalIdParams.
        :type: int
        """
        
        self._password_history_length = password_history_length

    @property
    def password_prompt_time(self):
        """
        Gets the password_prompt_time of this ProvidersLocalIdParams.
        Specifies time in seconds remaining before prompting for password change.

        :return: The password_prompt_time of this ProvidersLocalIdParams.
        :rtype: int
        """
        return self._password_prompt_time

    @password_prompt_time.setter
    def password_prompt_time(self, password_prompt_time):
        """
        Sets the password_prompt_time of this ProvidersLocalIdParams.
        Specifies time in seconds remaining before prompting for password change.

        :param password_prompt_time: The password_prompt_time of this ProvidersLocalIdParams.
        :type: int
        """
        
        self._password_prompt_time = password_prompt_time

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other

