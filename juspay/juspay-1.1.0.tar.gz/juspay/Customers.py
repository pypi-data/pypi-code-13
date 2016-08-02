import util
import sys

class Customers:

    def __init__(self):
        return

    class Customer:

        def __init__(self, kwargs):
            self.id = util.get_arg(kwargs, 'id')
            self.object = util.get_arg(kwargs, 'object')
            self.date_created = util.get_arg(kwargs, 'created')
            self.email_address = util.get_arg(kwargs, 'email_address')
            self.first_name = util.get_arg(kwargs, 'first_name')
            self.last_name = util.get_arg(kwargs, 'last_name')
            self.mobile_country_code = util.get_arg(kwargs, 'mobile_country_code')
            self.mobile_number = util.get_arg(kwargs, 'mobile_number')
            self.object_reference_id = util.get_arg(kwargs, 'object_reference_id')

    @staticmethod
    def add(**kwargs):
        method = 'POST'
        url = '/customers'
        parameters = {}

        # required_args checks for presence of necessary parameters
        required_args = {}
        for key in ['object_reference_id', 'mobile_number', 'email_address', 'first_name', 'last_name']:
            required_args[key] = False

        for key, value in kwargs.iteritems():
            parameters[key] = value
            required_args[key] = True

        # Warn user about missing necessary parameters
        for key in ['object_reference_id', 'mobile_number', 'email_address', 'first_name', 'last_name']:
            if required_args[key] is False:
                raise Exception('%s is a required argument for Customer.add()\n' % key)

        # Warn user about unhandled parameters
        for key in parameters:
            if key not in ['object_reference_id', 'mobile_number', 'email_address', 'first_name', 'last_name','mobile_country_code']:
                sys.stderr.write('%s not a valid argument for Customer.add()\n' % key)

        response = util.request(method, url, parameters).json()
        customer = Customers.Customer(response)
        return customer

    @staticmethod
    def list(**kwargs):
        method = 'GET'
        url = '/customers'
        parameters = {}
    	offset = util.get_arg(kwargs,'offset')
    	count = util.get_arg(kwargs,'count')

    	if count is None and offset is None:
            sys.stderr.write('count & offset can be passed if required.\n')

    	if count is not None:
    	    parameters["count"] = count

    	if offset is not None:
    	    parameters["offset"] = offset

        response = util.request(method, url, parameters).json()
        response = util.get_arg(response,'list')
        customers = []
        if response is not None:
            for customer in response:
                customer = Customers.Customer(customer)
                customers.append(customer)
        return customers

    @staticmethod
    def get(**kwargs):
        id = util.get_arg(kwargs,'id')

        if id is None:
            raise Exception('id is a required argument for Wallets.list()\n')

        method = 'GET'
        url = '/customers/%s' % (id)
        parameters = {}

        response = util.request(method, url, parameters).json()
        customer = Customers.Customer(response)
        return customer

    @staticmethod
    def delete(**kwargs):
        raise Exception('Not Implemented.\n')
