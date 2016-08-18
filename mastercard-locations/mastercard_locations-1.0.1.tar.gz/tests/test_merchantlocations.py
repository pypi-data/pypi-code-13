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
from mastercardlocations import *


class MerchantLocationsTest(BaseTest):

    def setUp(self):
        keyFile = join(dirname(realpath(__file__)),"resources","mcapi_sandbox_key.p12")
        auth = OAuthAuthentication("L5BsiPgaF-O3qA36znUATgQXwJB6MRoMSdhjd7wt50c97279!50596e52466e3966546d434b7354584c4975693238513d3d",keyFile, "alias", "password")
        Config.setAuthentication(auth)
        Config.setDebug(True)

    
        
        
        
        
        
        
                
    def test_example_merchants(self):
        mapObj = RequestMap()
        mapObj.set("Details", "acceptance.paypass")
        mapObj.set("PageOffset", "0")
        mapObj.set("PageLength", "5")
        mapObj.set("Latitude", "38.53463")
        mapObj.set("Longitude", "-90.286781")
        

        

        response = MerchantLocations.query(mapObj)
        self.customAssertValue("0", response.get("Merchants.PageOffset"))
        self.customAssertValue("3", response.get("Merchants.TotalCount"))
        self.customAssertValue("36564", response.get("Merchants.Merchant[0].Id"))
        self.customAssertValue("Merchant 36564", response.get("Merchants.Merchant[0].Name"))
        self.customAssertValue("7 - Dry Cleaners And Laundry Services", response.get("Merchants.Merchant[0].Category"))
        self.customAssertValue("Merchant 36564", response.get("Merchants.Merchant[0].Location.Name"))
        self.customAssertValue("0.9320591049747101", response.get("Merchants.Merchant[0].Location.Distance"))
        self.customAssertValue("MILE", response.get("Merchants.Merchant[0].Location.DistanceUnit"))
        self.customAssertValue("3822 West Fork Street", response.get("Merchants.Merchant[0].Location.Address.Line1"))
        self.customAssertValue("Great Falls", response.get("Merchants.Merchant[0].Location.Address.City"))
        self.customAssertValue("51765", response.get("Merchants.Merchant[0].Location.Address.PostalCode"))
        self.customAssertValue("Country Subdivision 517521", response.get("Merchants.Merchant[0].Location.Address.CountrySubdivision.Name"))
        self.customAssertValue("Country Subdivision Code 517521", response.get("Merchants.Merchant[0].Location.Address.CountrySubdivision.Code"))
        self.customAssertValue("Country 5175215", response.get("Merchants.Merchant[0].Location.Address.Country.Name"))
        self.customAssertValue("Country Code 5175215", response.get("Merchants.Merchant[0].Location.Address.Country.Code"))
        self.customAssertValue("38.52114017591121", response.get("Merchants.Merchant[0].Location.Point.Latitude"))
        self.customAssertValue("-90.28678100000002", response.get("Merchants.Merchant[0].Location.Point.Longitude"))
        self.customAssertValue("true", response.get("Merchants.Merchant[0].Acceptance.PayPass.Register"))
        

        BaseTest.putResponse("example_merchants", response);

    
        
    

if __name__ == '__main__':
    unittest.main()

