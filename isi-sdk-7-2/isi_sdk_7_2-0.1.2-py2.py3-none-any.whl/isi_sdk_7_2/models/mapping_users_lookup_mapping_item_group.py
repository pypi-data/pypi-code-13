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


class MappingUsersLookupMappingItemGroup(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        MappingUsersLookupMappingItemGroup - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'dn': 'str',
            'dns_domain': 'str',
            'domain': 'str',
            'email': 'str',
            'enabled': 'bool',
            'expired': 'bool',
            'expiry': 'int',
            'gecos': 'str',
            'generated_gid': 'bool',
            'generated_uid': 'bool',
            'generated_upn': 'bool',
            'gid': 'GroupMember',
            'home_directory': 'str',
            'id': 'str',
            'locked': 'bool',
            'max_password_age': 'int',
            'member_of': 'list[GroupMember]',
            'name': 'str',
            'on_disk_group_identity': 'GroupMember',
            'on_disk_user_identity': 'GroupMember',
            'password_expired': 'bool',
            'password_expires': 'bool',
            'password_expiry': 'int',
            'password_last_set': 'int',
            'primary_group_sid': 'GroupMember',
            'prompt_password_change': 'bool',
            'provider': 'str',
            'sam_account_name': 'str',
            'shell': 'str',
            'sid': 'GroupMember',
            'type': 'str',
            'uid': 'GroupMember',
            'upn': 'str',
            'user_can_change_password': 'bool'
        }

        self.attribute_map = {
            'dn': 'dn',
            'dns_domain': 'dns_domain',
            'domain': 'domain',
            'email': 'email',
            'enabled': 'enabled',
            'expired': 'expired',
            'expiry': 'expiry',
            'gecos': 'gecos',
            'generated_gid': 'generated_gid',
            'generated_uid': 'generated_uid',
            'generated_upn': 'generated_upn',
            'gid': 'gid',
            'home_directory': 'home_directory',
            'id': 'id',
            'locked': 'locked',
            'max_password_age': 'max_password_age',
            'member_of': 'member_of',
            'name': 'name',
            'on_disk_group_identity': 'on_disk_group_identity',
            'on_disk_user_identity': 'on_disk_user_identity',
            'password_expired': 'password_expired',
            'password_expires': 'password_expires',
            'password_expiry': 'password_expiry',
            'password_last_set': 'password_last_set',
            'primary_group_sid': 'primary_group_sid',
            'prompt_password_change': 'prompt_password_change',
            'provider': 'provider',
            'sam_account_name': 'sam_account_name',
            'shell': 'shell',
            'sid': 'sid',
            'type': 'type',
            'uid': 'uid',
            'upn': 'upn',
            'user_can_change_password': 'user_can_change_password'
        }

        self._dn = None
        self._dns_domain = None
        self._domain = None
        self._email = None
        self._enabled = None
        self._expired = None
        self._expiry = None
        self._gecos = None
        self._generated_gid = None
        self._generated_uid = None
        self._generated_upn = None
        self._gid = None
        self._home_directory = None
        self._id = None
        self._locked = None
        self._max_password_age = None
        self._member_of = None
        self._name = None
        self._on_disk_group_identity = None
        self._on_disk_user_identity = None
        self._password_expired = None
        self._password_expires = None
        self._password_expiry = None
        self._password_last_set = None
        self._primary_group_sid = None
        self._prompt_password_change = None
        self._provider = None
        self._sam_account_name = None
        self._shell = None
        self._sid = None
        self._type = None
        self._uid = None
        self._upn = None
        self._user_can_change_password = None

    @property
    def dn(self):
        """
        Gets the dn of this MappingUsersLookupMappingItemGroup.


        :return: The dn of this MappingUsersLookupMappingItemGroup.
        :rtype: str
        """
        return self._dn

    @dn.setter
    def dn(self, dn):
        """
        Sets the dn of this MappingUsersLookupMappingItemGroup.


        :param dn: The dn of this MappingUsersLookupMappingItemGroup.
        :type: str
        """
        
        self._dn = dn

    @property
    def dns_domain(self):
        """
        Gets the dns_domain of this MappingUsersLookupMappingItemGroup.


        :return: The dns_domain of this MappingUsersLookupMappingItemGroup.
        :rtype: str
        """
        return self._dns_domain

    @dns_domain.setter
    def dns_domain(self, dns_domain):
        """
        Sets the dns_domain of this MappingUsersLookupMappingItemGroup.


        :param dns_domain: The dns_domain of this MappingUsersLookupMappingItemGroup.
        :type: str
        """
        
        self._dns_domain = dns_domain

    @property
    def domain(self):
        """
        Gets the domain of this MappingUsersLookupMappingItemGroup.


        :return: The domain of this MappingUsersLookupMappingItemGroup.
        :rtype: str
        """
        return self._domain

    @domain.setter
    def domain(self, domain):
        """
        Sets the domain of this MappingUsersLookupMappingItemGroup.


        :param domain: The domain of this MappingUsersLookupMappingItemGroup.
        :type: str
        """
        
        self._domain = domain

    @property
    def email(self):
        """
        Gets the email of this MappingUsersLookupMappingItemGroup.
        Specifies an Email address.

        :return: The email of this MappingUsersLookupMappingItemGroup.
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email):
        """
        Sets the email of this MappingUsersLookupMappingItemGroup.
        Specifies an Email address.

        :param email: The email of this MappingUsersLookupMappingItemGroup.
        :type: str
        """
        
        self._email = email

    @property
    def enabled(self):
        """
        Gets the enabled of this MappingUsersLookupMappingItemGroup.
        Auth user is enabled.

        :return: The enabled of this MappingUsersLookupMappingItemGroup.
        :rtype: bool
        """
        return self._enabled

    @enabled.setter
    def enabled(self, enabled):
        """
        Sets the enabled of this MappingUsersLookupMappingItemGroup.
        Auth user is enabled.

        :param enabled: The enabled of this MappingUsersLookupMappingItemGroup.
        :type: bool
        """
        
        self._enabled = enabled

    @property
    def expired(self):
        """
        Gets the expired of this MappingUsersLookupMappingItemGroup.
        Auth user is expired.

        :return: The expired of this MappingUsersLookupMappingItemGroup.
        :rtype: bool
        """
        return self._expired

    @expired.setter
    def expired(self, expired):
        """
        Sets the expired of this MappingUsersLookupMappingItemGroup.
        Auth user is expired.

        :param expired: The expired of this MappingUsersLookupMappingItemGroup.
        :type: bool
        """
        
        self._expired = expired

    @property
    def expiry(self):
        """
        Gets the expiry of this MappingUsersLookupMappingItemGroup.
        Epoch time at which the auth user will expire.

        :return: The expiry of this MappingUsersLookupMappingItemGroup.
        :rtype: int
        """
        return self._expiry

    @expiry.setter
    def expiry(self, expiry):
        """
        Sets the expiry of this MappingUsersLookupMappingItemGroup.
        Epoch time at which the auth user will expire.

        :param expiry: The expiry of this MappingUsersLookupMappingItemGroup.
        :type: int
        """
        
        self._expiry = expiry

    @property
    def gecos(self):
        """
        Gets the gecos of this MappingUsersLookupMappingItemGroup.
        Sets GECOS value (usually full name).

        :return: The gecos of this MappingUsersLookupMappingItemGroup.
        :rtype: str
        """
        return self._gecos

    @gecos.setter
    def gecos(self, gecos):
        """
        Sets the gecos of this MappingUsersLookupMappingItemGroup.
        Sets GECOS value (usually full name).

        :param gecos: The gecos of this MappingUsersLookupMappingItemGroup.
        :type: str
        """
        
        self._gecos = gecos

    @property
    def generated_gid(self):
        """
        Gets the generated_gid of this MappingUsersLookupMappingItemGroup.


        :return: The generated_gid of this MappingUsersLookupMappingItemGroup.
        :rtype: bool
        """
        return self._generated_gid

    @generated_gid.setter
    def generated_gid(self, generated_gid):
        """
        Sets the generated_gid of this MappingUsersLookupMappingItemGroup.


        :param generated_gid: The generated_gid of this MappingUsersLookupMappingItemGroup.
        :type: bool
        """
        
        self._generated_gid = generated_gid

    @property
    def generated_uid(self):
        """
        Gets the generated_uid of this MappingUsersLookupMappingItemGroup.


        :return: The generated_uid of this MappingUsersLookupMappingItemGroup.
        :rtype: bool
        """
        return self._generated_uid

    @generated_uid.setter
    def generated_uid(self, generated_uid):
        """
        Sets the generated_uid of this MappingUsersLookupMappingItemGroup.


        :param generated_uid: The generated_uid of this MappingUsersLookupMappingItemGroup.
        :type: bool
        """
        
        self._generated_uid = generated_uid

    @property
    def generated_upn(self):
        """
        Gets the generated_upn of this MappingUsersLookupMappingItemGroup.


        :return: The generated_upn of this MappingUsersLookupMappingItemGroup.
        :rtype: bool
        """
        return self._generated_upn

    @generated_upn.setter
    def generated_upn(self, generated_upn):
        """
        Sets the generated_upn of this MappingUsersLookupMappingItemGroup.


        :param generated_upn: The generated_upn of this MappingUsersLookupMappingItemGroup.
        :type: bool
        """
        
        self._generated_upn = generated_upn

    @property
    def gid(self):
        """
        Gets the gid of this MappingUsersLookupMappingItemGroup.
        A persona consists of either a 'type' and 'name' or a 'ID'.

        :return: The gid of this MappingUsersLookupMappingItemGroup.
        :rtype: GroupMember
        """
        return self._gid

    @gid.setter
    def gid(self, gid):
        """
        Sets the gid of this MappingUsersLookupMappingItemGroup.
        A persona consists of either a 'type' and 'name' or a 'ID'.

        :param gid: The gid of this MappingUsersLookupMappingItemGroup.
        :type: GroupMember
        """
        
        self._gid = gid

    @property
    def home_directory(self):
        """
        Gets the home_directory of this MappingUsersLookupMappingItemGroup.
        Specifies user's home directory.

        :return: The home_directory of this MappingUsersLookupMappingItemGroup.
        :rtype: str
        """
        return self._home_directory

    @home_directory.setter
    def home_directory(self, home_directory):
        """
        Sets the home_directory of this MappingUsersLookupMappingItemGroup.
        Specifies user's home directory.

        :param home_directory: The home_directory of this MappingUsersLookupMappingItemGroup.
        :type: str
        """
        
        self._home_directory = home_directory

    @property
    def id(self):
        """
        Gets the id of this MappingUsersLookupMappingItemGroup.
        The user or group ID.

        :return: The id of this MappingUsersLookupMappingItemGroup.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this MappingUsersLookupMappingItemGroup.
        The user or group ID.

        :param id: The id of this MappingUsersLookupMappingItemGroup.
        :type: str
        """
        
        self._id = id

    @property
    def locked(self):
        """
        Gets the locked of this MappingUsersLookupMappingItemGroup.
        Specifies if account is locked out.

        :return: The locked of this MappingUsersLookupMappingItemGroup.
        :rtype: bool
        """
        return self._locked

    @locked.setter
    def locked(self, locked):
        """
        Sets the locked of this MappingUsersLookupMappingItemGroup.
        Specifies if account is locked out.

        :param locked: The locked of this MappingUsersLookupMappingItemGroup.
        :type: bool
        """
        
        self._locked = locked

    @property
    def max_password_age(self):
        """
        Gets the max_password_age of this MappingUsersLookupMappingItemGroup.
        The maximum age in seconds allowed for the password before it expires.

        :return: The max_password_age of this MappingUsersLookupMappingItemGroup.
        :rtype: int
        """
        return self._max_password_age

    @max_password_age.setter
    def max_password_age(self, max_password_age):
        """
        Sets the max_password_age of this MappingUsersLookupMappingItemGroup.
        The maximum age in seconds allowed for the password before it expires.

        :param max_password_age: The max_password_age of this MappingUsersLookupMappingItemGroup.
        :type: int
        """
        
        self._max_password_age = max_password_age

    @property
    def member_of(self):
        """
        Gets the member_of of this MappingUsersLookupMappingItemGroup.


        :return: The member_of of this MappingUsersLookupMappingItemGroup.
        :rtype: list[GroupMember]
        """
        return self._member_of

    @member_of.setter
    def member_of(self, member_of):
        """
        Sets the member_of of this MappingUsersLookupMappingItemGroup.


        :param member_of: The member_of of this MappingUsersLookupMappingItemGroup.
        :type: list[GroupMember]
        """
        
        self._member_of = member_of

    @property
    def name(self):
        """
        Gets the name of this MappingUsersLookupMappingItemGroup.
        A user or group name.

        :return: The name of this MappingUsersLookupMappingItemGroup.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this MappingUsersLookupMappingItemGroup.
        A user or group name.

        :param name: The name of this MappingUsersLookupMappingItemGroup.
        :type: str
        """
        
        self._name = name

    @property
    def on_disk_group_identity(self):
        """
        Gets the on_disk_group_identity of this MappingUsersLookupMappingItemGroup.
        A persona consists of either a 'type' and 'name' or a 'ID'.

        :return: The on_disk_group_identity of this MappingUsersLookupMappingItemGroup.
        :rtype: GroupMember
        """
        return self._on_disk_group_identity

    @on_disk_group_identity.setter
    def on_disk_group_identity(self, on_disk_group_identity):
        """
        Sets the on_disk_group_identity of this MappingUsersLookupMappingItemGroup.
        A persona consists of either a 'type' and 'name' or a 'ID'.

        :param on_disk_group_identity: The on_disk_group_identity of this MappingUsersLookupMappingItemGroup.
        :type: GroupMember
        """
        
        self._on_disk_group_identity = on_disk_group_identity

    @property
    def on_disk_user_identity(self):
        """
        Gets the on_disk_user_identity of this MappingUsersLookupMappingItemGroup.
        A persona consists of either a 'type' and 'name' or a 'ID'.

        :return: The on_disk_user_identity of this MappingUsersLookupMappingItemGroup.
        :rtype: GroupMember
        """
        return self._on_disk_user_identity

    @on_disk_user_identity.setter
    def on_disk_user_identity(self, on_disk_user_identity):
        """
        Sets the on_disk_user_identity of this MappingUsersLookupMappingItemGroup.
        A persona consists of either a 'type' and 'name' or a 'ID'.

        :param on_disk_user_identity: The on_disk_user_identity of this MappingUsersLookupMappingItemGroup.
        :type: GroupMember
        """
        
        self._on_disk_user_identity = on_disk_user_identity

    @property
    def password_expired(self):
        """
        Gets the password_expired of this MappingUsersLookupMappingItemGroup.
        Specifies whether the password has expired.

        :return: The password_expired of this MappingUsersLookupMappingItemGroup.
        :rtype: bool
        """
        return self._password_expired

    @password_expired.setter
    def password_expired(self, password_expired):
        """
        Sets the password_expired of this MappingUsersLookupMappingItemGroup.
        Specifies whether the password has expired.

        :param password_expired: The password_expired of this MappingUsersLookupMappingItemGroup.
        :type: bool
        """
        
        self._password_expired = password_expired

    @property
    def password_expires(self):
        """
        Gets the password_expires of this MappingUsersLookupMappingItemGroup.
        Password is allowed to expire.

        :return: The password_expires of this MappingUsersLookupMappingItemGroup.
        :rtype: bool
        """
        return self._password_expires

    @password_expires.setter
    def password_expires(self, password_expires):
        """
        Sets the password_expires of this MappingUsersLookupMappingItemGroup.
        Password is allowed to expire.

        :param password_expires: The password_expires of this MappingUsersLookupMappingItemGroup.
        :type: bool
        """
        
        self._password_expires = password_expires

    @property
    def password_expiry(self):
        """
        Gets the password_expiry of this MappingUsersLookupMappingItemGroup.
        Specifies the time in epoch seconds the password will expire.

        :return: The password_expiry of this MappingUsersLookupMappingItemGroup.
        :rtype: int
        """
        return self._password_expiry

    @password_expiry.setter
    def password_expiry(self, password_expiry):
        """
        Sets the password_expiry of this MappingUsersLookupMappingItemGroup.
        Specifies the time in epoch seconds the password will expire.

        :param password_expiry: The password_expiry of this MappingUsersLookupMappingItemGroup.
        :type: int
        """
        
        self._password_expiry = password_expiry

    @property
    def password_last_set(self):
        """
        Gets the password_last_set of this MappingUsersLookupMappingItemGroup.
        Specifies the last time the password was set.

        :return: The password_last_set of this MappingUsersLookupMappingItemGroup.
        :rtype: int
        """
        return self._password_last_set

    @password_last_set.setter
    def password_last_set(self, password_last_set):
        """
        Sets the password_last_set of this MappingUsersLookupMappingItemGroup.
        Specifies the last time the password was set.

        :param password_last_set: The password_last_set of this MappingUsersLookupMappingItemGroup.
        :type: int
        """
        
        self._password_last_set = password_last_set

    @property
    def primary_group_sid(self):
        """
        Gets the primary_group_sid of this MappingUsersLookupMappingItemGroup.
        A persona consists of either a 'type' and 'name' or a 'ID'.

        :return: The primary_group_sid of this MappingUsersLookupMappingItemGroup.
        :rtype: GroupMember
        """
        return self._primary_group_sid

    @primary_group_sid.setter
    def primary_group_sid(self, primary_group_sid):
        """
        Sets the primary_group_sid of this MappingUsersLookupMappingItemGroup.
        A persona consists of either a 'type' and 'name' or a 'ID'.

        :param primary_group_sid: The primary_group_sid of this MappingUsersLookupMappingItemGroup.
        :type: GroupMember
        """
        
        self._primary_group_sid = primary_group_sid

    @property
    def prompt_password_change(self):
        """
        Gets the prompt_password_change of this MappingUsersLookupMappingItemGroup.
        Prompts the user to change their password on next login.

        :return: The prompt_password_change of this MappingUsersLookupMappingItemGroup.
        :rtype: bool
        """
        return self._prompt_password_change

    @prompt_password_change.setter
    def prompt_password_change(self, prompt_password_change):
        """
        Sets the prompt_password_change of this MappingUsersLookupMappingItemGroup.
        Prompts the user to change their password on next login.

        :param prompt_password_change: The prompt_password_change of this MappingUsersLookupMappingItemGroup.
        :type: bool
        """
        
        self._prompt_password_change = prompt_password_change

    @property
    def provider(self):
        """
        Gets the provider of this MappingUsersLookupMappingItemGroup.
        Specifies an authentication provider.

        :return: The provider of this MappingUsersLookupMappingItemGroup.
        :rtype: str
        """
        return self._provider

    @provider.setter
    def provider(self, provider):
        """
        Sets the provider of this MappingUsersLookupMappingItemGroup.
        Specifies an authentication provider.

        :param provider: The provider of this MappingUsersLookupMappingItemGroup.
        :type: str
        """
        
        self._provider = provider

    @property
    def sam_account_name(self):
        """
        Gets the sam_account_name of this MappingUsersLookupMappingItemGroup.


        :return: The sam_account_name of this MappingUsersLookupMappingItemGroup.
        :rtype: str
        """
        return self._sam_account_name

    @sam_account_name.setter
    def sam_account_name(self, sam_account_name):
        """
        Sets the sam_account_name of this MappingUsersLookupMappingItemGroup.


        :param sam_account_name: The sam_account_name of this MappingUsersLookupMappingItemGroup.
        :type: str
        """
        
        self._sam_account_name = sam_account_name

    @property
    def shell(self):
        """
        Gets the shell of this MappingUsersLookupMappingItemGroup.
        Sets path to user's shell.

        :return: The shell of this MappingUsersLookupMappingItemGroup.
        :rtype: str
        """
        return self._shell

    @shell.setter
    def shell(self, shell):
        """
        Sets the shell of this MappingUsersLookupMappingItemGroup.
        Sets path to user's shell.

        :param shell: The shell of this MappingUsersLookupMappingItemGroup.
        :type: str
        """
        
        self._shell = shell

    @property
    def sid(self):
        """
        Gets the sid of this MappingUsersLookupMappingItemGroup.
        A persona consists of either a 'type' and 'name' or a 'ID'.

        :return: The sid of this MappingUsersLookupMappingItemGroup.
        :rtype: GroupMember
        """
        return self._sid

    @sid.setter
    def sid(self, sid):
        """
        Sets the sid of this MappingUsersLookupMappingItemGroup.
        A persona consists of either a 'type' and 'name' or a 'ID'.

        :param sid: The sid of this MappingUsersLookupMappingItemGroup.
        :type: GroupMember
        """
        
        self._sid = sid

    @property
    def type(self):
        """
        Gets the type of this MappingUsersLookupMappingItemGroup.


        :return: The type of this MappingUsersLookupMappingItemGroup.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this MappingUsersLookupMappingItemGroup.


        :param type: The type of this MappingUsersLookupMappingItemGroup.
        :type: str
        """
        
        self._type = type

    @property
    def uid(self):
        """
        Gets the uid of this MappingUsersLookupMappingItemGroup.
        A persona consists of either a 'type' and 'name' or a 'ID'.

        :return: The uid of this MappingUsersLookupMappingItemGroup.
        :rtype: GroupMember
        """
        return self._uid

    @uid.setter
    def uid(self, uid):
        """
        Sets the uid of this MappingUsersLookupMappingItemGroup.
        A persona consists of either a 'type' and 'name' or a 'ID'.

        :param uid: The uid of this MappingUsersLookupMappingItemGroup.
        :type: GroupMember
        """
        
        self._uid = uid

    @property
    def upn(self):
        """
        Gets the upn of this MappingUsersLookupMappingItemGroup.
        The user principal name.

        :return: The upn of this MappingUsersLookupMappingItemGroup.
        :rtype: str
        """
        return self._upn

    @upn.setter
    def upn(self, upn):
        """
        Sets the upn of this MappingUsersLookupMappingItemGroup.
        The user principal name.

        :param upn: The upn of this MappingUsersLookupMappingItemGroup.
        :type: str
        """
        
        self._upn = upn

    @property
    def user_can_change_password(self):
        """
        Gets the user_can_change_password of this MappingUsersLookupMappingItemGroup.
        Specifies whether the user's password can be changed.

        :return: The user_can_change_password of this MappingUsersLookupMappingItemGroup.
        :rtype: bool
        """
        return self._user_can_change_password

    @user_can_change_password.setter
    def user_can_change_password(self, user_can_change_password):
        """
        Sets the user_can_change_password of this MappingUsersLookupMappingItemGroup.
        Specifies whether the user's password can be changed.

        :param user_can_change_password: The user_can_change_password of this MappingUsersLookupMappingItemGroup.
        :type: bool
        """
        
        self._user_can_change_password = user_can_change_password

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

