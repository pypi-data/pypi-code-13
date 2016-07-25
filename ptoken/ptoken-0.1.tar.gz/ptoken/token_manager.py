from .cipher import Cipher
from .payload import Payload
from hashlib import md5
from .cache.frontend import Frontend


class TokenManager:
    """
        Generate token from uid
        Verify token from request
    """
    __instance_ = None  # type: TokenManager

    __cache_ = None  # type: Frontend
    __secret_key_ = ""  # type: str
    __token_ttl_ = 300  # type: int
    __remember_ttl_ = 31536000  # type: int

    def __init__(self, secret_key="", token_ttl=300, remember_ttl=31536000, cache=None):

        """

        :param secret_key:
        :type secret_key: str
        :param token_ttl:
        :type token_ttl: int
        :param remember_ttl: Lifetime of remember key (seconds)
        :type remember_ttl: int
        :param cache:
        """
        self.__cache_ = cache  # type: Frontend
        self.__secret_key_ = secret_key
        self.__token_ttl_ = token_ttl
        self.__remember_ttl_ = remember_ttl

    @classmethod
    def getInstance(cls, secret_key="", token_ttl=300, remember_ttl=31536000, cache=None):

        """
        Create new instance if it didn't created
        :param cache:
        :type cache: Frontend
        :param token_ttl:
        :param remember_ttl:
        :param secret_key:
        :type secret_key: str
        :return:
        """

        if TokenManager.__instance_ is None:
            TokenManager.__instance_ = TokenManager(secret_key=secret_key, token_ttl=token_ttl,
                                                    remember_ttl=remember_ttl,
                                                    cache=cache)
        return TokenManager.__instance_

    def is_not_used(self):
        pass

    def to_token(self, uid):
        """
        Generate token by create payload and call __payload_to_token
        :param uid:
        :param secret_key:
        :type secret_key str
        :param token_ttl
        :param remember_ttl
        :return:
        """
        salt = md5(self.__secret_key_.encode("utf-8")).hexdigest()
        pl = Payload.new(uid=uid, secret_key=self.__secret_key_, salt=salt, token_ttl=self.__token_ttl_,
                         remember_ttl=self.__remember_ttl_)
        token = Cipher.encrypt(pl.sign()[1].encode(), self.__secret_key_, salt)

        return token, pl.remember_key

    def from_token(self, token, remember_token=None):
        """
        Decrypt token and verify token
        :param token:
        :param remember_token:
        :return:
        """

        if self.__cache_.has("token-%s" % token):  # Return False if token be blocked
            return False

        salt = md5(self.__secret_key_.encode("utf-8")).hexdigest()
        token = Cipher.decrypt(token, self.__secret_key_, salt)
        if token is None:
            return False

        pl = Payload(secret_key=self.__secret_key_, salt=salt)
        if not pl.load(token):
            return False

        return pl if pl.verify(remember_token) else False

    def block_token(self, token):
        """
        Block token by store to cache blocked list
        :param token:
        :param secret_key:
        :return:
        """
        if self.__cache_ is not None:
            if not self.from_token(token):
                return False
            self.__cache_.set("token-%s" % token, "", ttl=self.__token_ttl_)
            return True
        else:
            return False

    def refresh(self, token, remember_token=None):
        """
        Block old token and genenrate new token
        :param token:
        :param remember_token:
        :return:
        """
        pl = self.from_token(token)
        if pl is not False:
            uid = pl.uid
            self.block_token(token)
            return self.to_token(uid)
        return False
