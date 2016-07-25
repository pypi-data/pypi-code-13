import json, time
from .signer import Signer
from .cipher import Cipher


class Payload:
    """
        Payload store token information
        :__token_ttl_: lifetime of token
        :__remember_ttl_: lifetime of remember key
        :__uid_: account id
        :__secret_key_: Secret Key
        :____signature_: Signature is be generated
        :__salt_: salt for encrypt
    """

    __token_ttl_ = 300  #: second
    __remember_ttl_ = 0  #: second
    __salt_ = ""
    __secret_key_ = ""
    __random_str_ = None
    __signature_ = None
    __expired_at_ = None
    __remember_expired_at_ = None

    __uid_ = None
    __additional_data_ = ""
    __remember_key_ = None

    def __init__(self, uid=None, additional_data="", secret_key="", salt="", token_ttl=300, remember_ttl=0):
        self.__token_ttl_ = token_ttl
        self.__remember_ttl_ = remember_ttl
        self.__secret_key_ = secret_key
        self.__uid_ = uid
        self.__salt_ = salt
        self.__additional_data_ = additional_data
        self.generate_random_str()

    @classmethod
    def new(cls, uid=None, additional_data="", secret_key="", salt="", token_ttl=300, remember_ttl=0):
        return Payload(uid, additional_data, secret_key, salt, token_ttl, remember_ttl)

    @property
    def token_ttl(self):
        return self.__token_ttl_

    @property
    def remember_ttl(self):
        return self.__remember_ttl_

    @property
    def salt(self):
        return self.__salt_

    @property
    def secret_key(self):
        return self.__secret_key_

    @property
    def uid(self):
        return self.__uid_

    @property
    def additional_data(self):
        return self.__additional_data_

    @property
    def remember_key(self):
        if self.__remember_key_ is None:
            self.__remember_key_ = Cipher.generate_salt(64)
        return self.__remember_key_

    @property
    def remember_expired_at(self):
        if self.__remember_expired_at_ is None:
            self.__remember_expired_at_ = int(time.time()) + self.remember_ttl

        return self.__remember_expired_at_

    def generate_random_str(self):
        """
        Generate random string
        :return:
        """
        self.__random_str_ = Cipher.generate_salt(32)

    def serialize(self, **kwargs):
        """
            Serialize object to json and list

        :return: list, json
        """
        data = {
            "uid": self.uid,
            "iv": self.__random_str_,
            "expired_at": int(time.time()) + self.token_ttl if self.__expired_at_ is None else self.__expired_at_,
            "remember_key": self.remember_key,
            "remember_expired_at": self.remember_expired_at
        }
        data.update(kwargs)

        if self.additional_data is not None and not self.additional_data == "":
            data["additional_data"] = self.additional_data

        return data, json.dumps(data)

    def load(self, data):
        """
        Load data from json to object
        :param data: json string
        :type data: str
        :return: True if success
        """
        try:
            data = json.loads(data)

            self.__uid_ = data["uid"]
            self.__signature_ = data["signature"]
            self.__random_str_ = data["iv"]
            self.__expired_at_ = data["expired_at"]
            self.__remember_expired_at_ = data["remember_expired_at"]
            self.__remember_key_ = data["remember_key"] if "remember_key" in data else None
            self.__additional_data_ = data["additional_data"] if "additional_data" in data else None

            return True, data
        except:
            return False

    def __sign_(self):
        """
        Create sign and encrypt
        :return:
        """
        arr, json_str = self.serialize()
        salt = self.salt + self.__random_str_

        return Cipher.encrypt(Signer.sign(json_str, self.__secret_key_), self.secret_key, salt)

    def sign(self):
        """
        Call __sign_ and store sign to object
        :return:
        """
        self.__signature_ = self.__sign_()
        return self.serialize(signature=self.__signature_)

    def verify(self, remember_key=None):
        """
        Verify signature
        :return:
        """
        guess_signature = Cipher.decrypt(self.__signature_, self.secret_key, self.salt + self.__random_str_)
        if guess_signature is None:
            return False

        if not self.__sign_() == self.__signature_:
            return False

        if self.__expired_at_ < int(time.time()):
            if remember_key is not None and remember_key == self.remember_key \
                    and self.remember_expired_at > int(time.time()):
                return True

            return False

        return True
