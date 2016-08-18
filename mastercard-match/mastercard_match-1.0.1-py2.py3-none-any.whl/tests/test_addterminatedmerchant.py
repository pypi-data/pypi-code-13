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
from mastercardmatch import *


class AddTerminatedMerchantTest(BaseTest):

    def setUp(self):
        keyFile = join(dirname(realpath(__file__)),"resources","mcapi_sandbox_key.p12")
        auth = OAuthAuthentication("L5BsiPgaF-O3qA36znUATgQXwJB6MRoMSdhjd7wt50c97279!50596e52466e3966546d434b7354584c4975693238513d3d",keyFile, "alias", "password")
        Config.setAuthentication(auth)
        Config.setDebug(True)

    
        
                
    def test_example_add_terminated_merchant(self):
        mapObj = RequestMap()
        mapObj.set("AddMerchantRequest.AcquirerId", "1996")
        mapObj.set("AddMerchantRequest.Merchant.Name", "TEST TECHMERCHANT1")
        mapObj.set("AddMerchantRequest.Merchant.DoingBusinessAsName", "TEST TECHMERCHANT1")
        mapObj.set("AddMerchantRequest.Merchant.MerchantId", "788339982614722")
        mapObj.set("AddMerchantRequest.Merchant.MerchantCategory", "0742")
        mapObj.set("AddMerchantRequest.Merchant.Address.Line1", "6700 Ben Nevis")
        mapObj.set("AddMerchantRequest.Merchant.Address.Line2", "")
        mapObj.set("AddMerchantRequest.Merchant.Address.City", "GLASGOW")
        mapObj.set("AddMerchantRequest.Merchant.Address.Province", "")
        mapObj.set("AddMerchantRequest.Merchant.Address.CountrySubdivision", "MA")
        mapObj.set("AddMerchantRequest.Merchant.Address.PostalCode", "93137")
        mapObj.set("AddMerchantRequest.Merchant.Address.Country", "USA")
        mapObj.set("AddMerchantRequest.Merchant.PhoneNumber", "5675542210")
        mapObj.set("AddMerchantRequest.Merchant.AltPhoneNumber", "5672655441")
        mapObj.set("AddMerchantRequest.Merchant.NationalTaxId", "56733")
        mapObj.set("AddMerchantRequest.Merchant.CountrySubdivisionTaxId", "37354")
        mapObj.set("AddMerchantRequest.Merchant.CATFlag", "N")
        mapObj.set("AddMerchantRequest.Merchant.DateOpened", "04/12/2009")
        mapObj.set("AddMerchantRequest.Merchant.DateClosed", "03/19/2013")
        mapObj.set("AddMerchantRequest.Merchant.ServiceProvLegal", "TEST SVC PRVDER")
        mapObj.set("AddMerchantRequest.Merchant.ServiceProvDBA", "JNL ASSOC")
        mapObj.set("AddMerchantRequest.Merchant.Url[0]", "www.testjj.com")
        mapObj.set("AddMerchantRequest.Merchant.Url[1]", "www.jnltestjj.com")
        mapObj.set("AddMerchantRequest.Merchant.Principal.FirstName", "PAUL")
        mapObj.set("AddMerchantRequest.Merchant.Principal.LastName", "HEMINGHOFF")
        mapObj.set("AddMerchantRequest.Merchant.Principal.MiddleInitial", "L")
        mapObj.set("AddMerchantRequest.Merchant.Principal.Address.Line1", "2200 Shepley Drive")
        mapObj.set("AddMerchantRequest.Merchant.Principal.Address.Line2", "SUITE 789")
        mapObj.set("AddMerchantRequest.Merchant.Principal.Address.City", "BROWNSVILLE")
        mapObj.set("AddMerchantRequest.Merchant.Principal.Address.Province", "")
        mapObj.set("AddMerchantRequest.Merchant.Principal.Address.CountrySubdivision", "MO")
        mapObj.set("AddMerchantRequest.Merchant.Principal.Address.PostalCode", "89022")
        mapObj.set("AddMerchantRequest.Merchant.Principal.Address.Country", "USA")
        mapObj.set("AddMerchantRequest.Merchant.Principal.PhoneNumber", "3906541234")
        mapObj.set("AddMerchantRequest.Merchant.Principal.AltPhoneNumber", "4567390234")
        mapObj.set("AddMerchantRequest.Merchant.Principal.NationalId", "123456789")
        mapObj.set("AddMerchantRequest.Merchant.Principal.DriversLicense.Number", "3K33094")
        mapObj.set("AddMerchantRequest.Merchant.Principal.DriversLicense.CountrySubdivision", "MS")
        mapObj.set("AddMerchantRequest.Merchant.Principal.DriversLicense.Country", "USA")
        mapObj.set("AddMerchantRequest.Merchant.ReasonCode", "04")
        mapObj.set("AddMerchantRequest.Merchant.Comments", "Added for test reasons")
        

        

        response = AddTerminatedMerchant.create(mapObj)
        

        BaseTest.putResponse("example_add_terminated_merchant", response);

    
        
        
        
        
        
        
    

if __name__ == '__main__':
    unittest.main()

