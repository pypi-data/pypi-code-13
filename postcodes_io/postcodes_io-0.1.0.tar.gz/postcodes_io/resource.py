from postcodes_io.helper import http_get, http_post


class Postcodes:
    """
    Postcodes resource

    Access point for almost all restful requests

    Refer to http://postcodes.io/docs for full API endpoints
    """

    def __init__(self, base_url: str = 'https://api.postcodes.io'):
        """
        Creates postcodes object using a base url.

        :param base_url: base url of the restful service.  Default to the free service at https://api.postcodes.io.
        """
        self.end_point = '{}/{}'.format(base_url.rstrip('/'), 'postcodes')

    def get(self, postcode: str) -> dict:
        """
        Lookup a postcode

        :param postcode: postcode to lookup
        :return: dict of a postcode's details
        """

        return http_get('{}/{}'.format(self.end_point, postcode))

    def get_many(self, postcodes: list) -> list:
        """
        Bulk lookup postcode
        :param postcodes: list of postcodes
        :return: list of dicts containing postcodes' details
        """
        return http_post(self.end_point, data={'postcodes': postcodes})

    def nearest_by_geo(self, latitude: float, longitude: float):
        """
        Get nearest postcodes for a given longitude & latitude

        :param latitude:
        :param longitude:
        :return: dict of postcode's details
        """
        return http_get(self.end_point, params={'latitude': latitude, 'longitude': longitude})

    def validate(self, postcode: str) -> bool:
        """
        Validate a postcode

        :param postcode:
        :return: True if postcode is valie, False otherwise
        """
        return http_get('{}/{}/validate'.format(self.end_point, postcode))

    def nearest(self, postcode: str) -> dict:
        """
        Nearest postcodes for postcode

        :param postcode:
        :return: dict of postcode
        """
        return http_get('{}/{}/nearest'.format(self.end_point, postcode))

    def autocomplete(self, partial_postcode: str) -> list:
        """
        Autocomplete a postcode partial

        :param partial_postcode:
        :return: list of suggestions
        """
        return http_get('{}/{}/autocomplete'.format(self.end_point, partial_postcode))

    def query(self, postcode: str):
        """
        Query for postcode

        :param postcode:
        :return:
        """
        return http_get(self.end_point, params={'q': postcode})
