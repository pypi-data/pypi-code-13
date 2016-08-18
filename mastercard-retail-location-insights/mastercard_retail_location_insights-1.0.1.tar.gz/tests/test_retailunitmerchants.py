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
from mastercardretaillocationinsights import *


class RetailUnitMerchantsTest(BaseTest):

    def setUp(self):
        keyFile = join(dirname(realpath(__file__)),"resources","mcapi_sandbox_key.p12")
        auth = OAuthAuthentication("L5BsiPgaF-O3qA36znUATgQXwJB6MRoMSdhjd7wt50c97279!50596e52466e3966546d434b7354584c4975693238513d3d",keyFile, "alias", "password")
        Config.setAuthentication(auth)
        Config.setDebug(True)

    
        
        
        
        
        
        
                
    def test_example_retail_unit_merchants(self):
        mapObj = RequestMap()
        mapObj.set("PageOffset", "1")
        mapObj.set("PageLength", "100")
        mapObj.set("RetailUnitType", "State")
        mapObj.set("RetailUnitId", "4")
        

        

        response = RetailUnitMerchants.query(mapObj)
        self.customAssertValue("1", response.get("RetailUnitMerchantResponse.PageOffset"))
        self.customAssertValue("12", response.get("RetailUnitMerchantResponse.TotalCount"))
        self.customAssertValue("2016/03", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[0].Period"))
        self.customAssertValue("AUS", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[0].RetailUnit.CountryCode"))
        self.customAssertValue("74", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[0].Merchant.Id"))
        self.customAssertValue("PROFIX SERVICE CTR", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[0].Merchant.Name"))
        self.customAssertValue("B", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[0].Merchant.ChannelOfDistribution"))
        self.customAssertValue("MRS", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[0].Merchant.Industry"))
        self.customAssertValue("Maintenance and Repair Se", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[0].Merchant.IndustryName"))
        self.customAssertValue("96 THE PARADE", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[0].Merchant.StreetAddress"))
        self.customAssertValue("NORWOOD", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[0].Merchant.City"))
        self.customAssertValue("5067", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[0].Merchant.PostalCode"))
        self.customAssertValue("SA", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[0].Merchant.CountrySubdivision"))
        self.customAssertValue("AUS", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[0].Merchant.CountryCode"))
        self.customAssertValue("-34.921538", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[0].Merchant.Latitude"))
        self.customAssertValue("138.631115", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[0].Merchant.Longitude"))
        self.customAssertValue("2016/03", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[1].Period"))
        self.customAssertValue("AUS", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[1].RetailUnit.CountryCode"))
        self.customAssertValue("75", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[1].Merchant.Id"))
        self.customAssertValue("DR DAVID CARMAN", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[1].Merchant.Name"))
        self.customAssertValue("B", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[1].Merchant.ChannelOfDistribution"))
        self.customAssertValue("HCS", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[1].Merchant.Industry"))
        self.customAssertValue("Health Care and Social As", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[1].Merchant.IndustryName"))
        self.customAssertValue("48 KING WILLIAM ROAD", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[1].Merchant.StreetAddress"))
        self.customAssertValue("GOODWOOD", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[1].Merchant.City"))
        self.customAssertValue("5034", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[1].Merchant.PostalCode"))
        self.customAssertValue("SA", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[1].Merchant.CountrySubdivision"))
        self.customAssertValue("AUS", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[1].Merchant.CountryCode"))
        self.customAssertValue("-34.948616", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[1].Merchant.Latitude"))
        self.customAssertValue("138.599496", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[1].Merchant.Longitude"))
        self.customAssertValue("2016/03", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[2].Period"))
        self.customAssertValue("AUS", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[2].RetailUnit.CountryCode"))
        self.customAssertValue("76", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[2].Merchant.Id"))
        self.customAssertValue("SUNRISE CHILDREN ASSO", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[2].Merchant.Name"))
        self.customAssertValue("C", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[2].Merchant.ChannelOfDistribution"))
        self.customAssertValue("RCP", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[2].Merchant.Industry"))
        self.customAssertValue("Religious", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[2].Merchant.IndustryName"))
        self.customAssertValue("46 A ST ANNS PLACE", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[2].Merchant.StreetAddress"))
        self.customAssertValue("PARKSIDE", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[2].Merchant.City"))
        self.customAssertValue("5063", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[2].Merchant.PostalCode"))
        self.customAssertValue("SA", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[2].Merchant.CountrySubdivision"))
        self.customAssertValue("AUS", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[2].Merchant.CountryCode"))
        self.customAssertValue("-34.942697", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[2].Merchant.Latitude"))
        self.customAssertValue("138.615377", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[2].Merchant.Longitude"))
        self.customAssertValue("2016/03", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[3].Period"))
        self.customAssertValue("AUS", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[3].RetailUnit.CountryCode"))
        self.customAssertValue("77", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[3].Merchant.Id"))
        self.customAssertValue("BEST BUY MOTORS", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[3].Merchant.Name"))
        self.customAssertValue("B", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[3].Merchant.ChannelOfDistribution"))
        self.customAssertValue("AUC", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[3].Merchant.Industry"))
        self.customAssertValue("Automotive Used Only Car ", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[3].Merchant.IndustryName"))
        self.customAssertValue("232 HAMPSTEAD ROAD", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[3].Merchant.StreetAddress"))
        self.customAssertValue("CLEARVIEW", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[3].Merchant.City"))
        self.customAssertValue("5085", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[3].Merchant.PostalCode"))
        self.customAssertValue("SA", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[3].Merchant.CountrySubdivision"))
        self.customAssertValue("AUS", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[3].Merchant.CountryCode"))
        self.customAssertValue("-34.860851", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[3].Merchant.Latitude"))
        self.customAssertValue("138.618136", response.get("RetailUnitMerchantResponse.RetailUnitMerchants.RetailUnitMerchant[3].Merchant.Longitude"))
        

        BaseTest.putResponse("example_retail_unit_merchants", response);

    
        
    

if __name__ == '__main__':
    unittest.main()

