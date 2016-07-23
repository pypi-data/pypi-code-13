"""
ccli/lib/connectwise/company_api/api.py

This file contains the source for the company API.
"""
from __future__ import (print_function, absolute_import)

from ..common import ConnectwiseApi


####################################################################################################
# Classes

class ConnectwiseCompanyApi(ConnectwiseApi):
    """
    Class for interfacing with the ConnectWise Company SOAP API.
    """

    def __init__(self):
        super(ConnectwiseCompanyApi, self).__init__('CompanyApi.asmx')

    @ConnectwiseApi.handle_errors
    def get_company(self, company_id):
        """
        Get a company from ConnectWise via the company record ID.

        :param company_id: ConnectWise record ID of the company.
        :type company_id: int

        :return:
        """
        res = self.client.service.GetCompany(self.credentials, company_id)
        return res
