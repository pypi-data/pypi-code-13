#
# Copyright (c) 2016 MasterCard International Incorporated
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are
# permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this list of
# conditions and the following disclaimer.
# Redistributions in binary form must reproduce the above copyright notice, this list of
# conditions and the following disclaimer in the documentation and/or other materials
# provided with the distribution.
# Neither the name of the MasterCard International Incorporated nor the names of its
# contributors may be used to endorse or promote products derived from this software
# without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT
# SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
#

import unittest
from mastercardapicore import RequestMap, Config, OAuthAuthentication
from os.path import dirname, realpath, join
from base_test import BaseTest
from mastercardmerchantidentifier import *


class MerchantIdentifierTest(BaseTest):

    def setUp(self):
        keyFile = join(dirname(realpath(__file__)),"resources","mcapi_sandbox_key.p12")
        auth = OAuthAuthentication("L5BsiPgaF-O3qA36znUATgQXwJB6MRoMSdhjd7wt50c97279!50596e52466e3966546d434b7354584c4975693238513d3d",keyFile, "alias", "password")
        Config.setAuthentication(auth)
        Config.setDebug(True)

    
        
        
        
        
        
        
                
    def test_example_merchant_identifier(self):
        mapObj = RequestMap()
        mapObj.set("MerchantId", "MICROSOFT")
        mapObj.set("Type", "FuzzyMatch")
        

        

        response = MerchantIdentifier.query(mapObj)
        self.customAssertValue("7 merchants found.", response.get("MerchantIds.Message"))
        self.customAssertValue("ONE MICROSOFT WAY", response.get("MerchantIds.ReturnedMerchants.Merchant[0].Address.Line1"))
        self.customAssertValue("REDMOND", response.get("MerchantIds.ReturnedMerchants.Merchant[0].Address.City"))
        self.customAssertValue("98052", response.get("MerchantIds.ReturnedMerchants.Merchant[0].Address.PostalCode"))
        self.customAssertValue("WA", response.get("MerchantIds.ReturnedMerchants.Merchant[0].Address.CountrySubdivision.Code"))
        self.customAssertValue("8003865550", response.get("MerchantIds.ReturnedMerchants.Merchant[0].PhoneNumber"))
        self.customAssertValue("4816 - COMPUTER NETWORK-INFORMATION SERVICES", response.get("MerchantIds.ReturnedMerchants.Merchant[0].MerchantCategory"))
        self.customAssertValue("MICROSOFT", response.get("MerchantIds.ReturnedMerchants.Merchant[0].MerchantDbaName"))
        self.customAssertValue("MICROSOFT*ONECAREBILL.MS.NETWA", response.get("MerchantIds.ReturnedMerchants.Merchant[0].DescriptorText"))
        self.customAssertValue("MICROSOFT CORPORATION", response.get("MerchantIds.ReturnedMerchants.Merchant[0].LegalCorporateName"))
        self.customAssertValue("288560095", response.get("MerchantIds.ReturnedMerchants.Merchant[0].LocationId"))
        self.customAssertValue("ONE MICROSOFT WAY", response.get("MerchantIds.ReturnedMerchants.Merchant[1].Address.Line1"))
        self.customAssertValue("REDMOND", response.get("MerchantIds.ReturnedMerchants.Merchant[1].Address.City"))
        self.customAssertValue("98052", response.get("MerchantIds.ReturnedMerchants.Merchant[1].Address.PostalCode"))
        self.customAssertValue("WA", response.get("MerchantIds.ReturnedMerchants.Merchant[1].Address.CountrySubdivision.Code"))
        self.customAssertValue("8003865550", response.get("MerchantIds.ReturnedMerchants.Merchant[1].PhoneNumber"))
        self.customAssertValue("4816 - COMPUTER NETWORK-INFORMATION SERVICES", response.get("MerchantIds.ReturnedMerchants.Merchant[1].MerchantCategory"))
        self.customAssertValue("MICROSOFT", response.get("MerchantIds.ReturnedMerchants.Merchant[1].MerchantDbaName"))
        self.customAssertValue("MICROSOFT*ONECARE08003865550WA", response.get("MerchantIds.ReturnedMerchants.Merchant[1].DescriptorText"))
        self.customAssertValue("MICROSOFT CORPORATION", response.get("MerchantIds.ReturnedMerchants.Merchant[1].LegalCorporateName"))
        self.customAssertValue("288560095", response.get("MerchantIds.ReturnedMerchants.Merchant[1].LocationId"))
        self.customAssertValue("ONE MICROSOFT WAY", response.get("MerchantIds.ReturnedMerchants.Merchant[2].Address.Line1"))
        self.customAssertValue("REDMOND", response.get("MerchantIds.ReturnedMerchants.Merchant[2].Address.City"))
        self.customAssertValue("98052", response.get("MerchantIds.ReturnedMerchants.Merchant[2].Address.PostalCode"))
        self.customAssertValue("WA", response.get("MerchantIds.ReturnedMerchants.Merchant[2].Address.CountrySubdivision.Code"))
        self.customAssertValue("8003865550", response.get("MerchantIds.ReturnedMerchants.Merchant[2].PhoneNumber"))
        self.customAssertValue("4816 - COMPUTER NETWORK-INFORMATION SERVICES", response.get("MerchantIds.ReturnedMerchants.Merchant[2].MerchantCategory"))
        self.customAssertValue("MICROSOFT", response.get("MerchantIds.ReturnedMerchants.Merchant[2].MerchantDbaName"))
        self.customAssertValue("MICROSOFT*ONECARE800-888-4081WA", response.get("MerchantIds.ReturnedMerchants.Merchant[2].DescriptorText"))
        self.customAssertValue("MICROSOFT CORPORATION", response.get("MerchantIds.ReturnedMerchants.Merchant[2].LegalCorporateName"))
        self.customAssertValue("0", response.get("MerchantIds.ReturnedMerchants.Merchant[2].LocationId"))
        

        BaseTest.putResponse("example_merchant_identifier", response);

    
        
    

if __name__ == '__main__':
    unittest.main()

