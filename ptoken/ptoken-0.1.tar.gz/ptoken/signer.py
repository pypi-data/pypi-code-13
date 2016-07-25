import hmac
import hashlib
import base64


class Signer:
    """
        Sign into response token
    """

    @classmethod
    def sign(cls, msg, secret_key):
        """
        Sign (hash) content
        :param msg:
        :param secret_key:
        :return:
        """
        msg = msg.encode("utf-8")
        secret_key = secret_key.encode("utf-8")
        digest = hmac.new(secret_key, msg, digestmod=hashlib.sha512).digest()
        signature = base64.b64encode(digest).decode()
        return signature

    @classmethod
    def verify(cls, signature, msg, secret_key):
        """
        Verify changed content
        :param signature:
        :param msg:
        :param secret_key:
        :return:
        """
        return cls.sign(msg, secret_key) == signature
