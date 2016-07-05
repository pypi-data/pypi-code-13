# coding=utf-8
"""
Idealista API
"""
__copyright__ = 'Copyright 2016, DNest'

from xml.etree.ElementTree import Element, SubElement


class IdealistaAPI(object):
    aggregator = ''
    code = ''

    def __init__(self, aggregator, code):
        self.aggregator = aggregator
        self.code = code

    def _add_props_to_xml(self, parent, values_dict):
        for key in values_dict:
            if key == '_in':
                continue

            value = values_dict[key]
            try:
                value_in = value['_in']
            except:
                value_in = {}
            key_xml = SubElement(parent, key, value_in)

            if type(value) == list:
                for item in value:
                    self._add_props_to_xml(key_xml, item)
            elif type(value) == dict:
                self._add_props_to_xml(key_xml, value)
            else:
                if type(value) in [float, int, long]:
                    key_xml.text = str(value)
                else:
                    key_xml.text = value

    def _make_xml(self, property_list):

        # Clients
        clients = Element('clients')

        # Client
        client = SubElement(clients, 'client')

        # Add data to client
        self._add_props_to_xml(client, {
            'aggregator': self.aggregator,
            'code': self.code
        })

        # Add properties
        properties_xml = SubElement(client, 'secondhandListing')
        for property in property_list:
            property_xml = SubElement(properties_xml, 'property')
            self._add_props_to_xml(property_xml, property)

        return clients

    def get_xml(self, property_list):
        return self._make_xml(property_list)
