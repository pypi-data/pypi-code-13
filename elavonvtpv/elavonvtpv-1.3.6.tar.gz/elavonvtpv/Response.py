from xml.dom import minidom
from xml.etree import ElementTree as Etree
import hashlib


class Response:
    def __init__(self, xml=None):
        """
        Defines a Response object
        :param xml: a string containing xml data
        """
        if xml:
            self._xml = Etree.fromstring(xml)
        else:
            self._xml = None

    def __getattr__(self, item):
        """
        Search unidentified attributes inside the ElementTree structure inside the _xml attribute.
        :param item: the name of the requested attribute
        :return: the content of the first tag named item in the ElementTree structure
        """
        return self._xml.find(item).text

    def list_xml_tags(self):
        """
        Returns a list of all xml tags inside the object.
        :return: list of strings representing the tags of the xml elements contained by the object.
        """
        return [elem.tag for elem in self._xml.iter()]

    def to_xml_string(self):
        """
        Turns the xml tree contained by this object into a string.
        :return: a string with the xml contained by this object.
        """
        binary = Etree.tostring(self._xml, encoding='utf8', method='xml')
        return binary.decode('utf-8')

    def to_pretty_xml(self):
        """
        Turns the xml tree contained by this object into a pretty string for easy reading.
        :return: a string with the xml contained by this object.
        """
        return minidom.parseString(self.to_xml_string()).toprettyxml()

    def __hash(self):
        """
        Builds the response hash from the data contained within
        :return: the hash string that will latter be cyphered
        """
        res = "%s.%s.%s.%s.%s.%s.%s" % (str(self.timestamp), str(self.merchant_id), str(self.order_id), str(self.result)
                                        , str(self.message), str(self.pas_ref), str(self.auth_code))
        return res.encode('utf-8')

    def __sha1_hash(self, secret):
        """
        returns a secure hash in SHA-1 for this response
        :param secret: the shared secret between Elavon and your account
        :return: secure hash in SHA-1
        """
        sha1_hash = hashlib.sha1(self.__hash()).hexdigest()
        sha1_hash += ".%s" % secret

        return hashlib.sha1(sha1_hash.encode('utf-8')).digest()

    def validate_origin(self, secret):
        """
        validates the request hash to check if the response was really sent by Elavon
        :param secret: the shared secret between Elavon and your account
        :return: a boolean value indicating the validity of the response hash
        """
        try:
            return self.sha1hash is self.__sha1_hash(secret)
        except AttributeError:
            return False
