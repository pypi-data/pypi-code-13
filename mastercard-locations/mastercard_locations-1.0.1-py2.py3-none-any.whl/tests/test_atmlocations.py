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


class ATMLocationsTest(BaseTest):

    def setUp(self):
        keyFile = join(dirname(realpath(__file__)),"resources","mcapi_sandbox_key.p12")
        auth = OAuthAuthentication("L5BsiPgaF-O3qA36znUATgQXwJB6MRoMSdhjd7wt50c97279!50596e52466e3966546d434b7354584c4975693238513d3d",keyFile, "alias", "password")
        Config.setAuthentication(auth)
        Config.setDebug(True)

    
        
        
        
        
        
        
                
    def test_atm_locations(self):
        mapObj = RequestMap()
        mapObj.set("PageOffset", "0")
        mapObj.set("PageLength", "5")
        mapObj.set("PostalCode", "11101")
        

        

        response = ATMLocations.query(mapObj)
        self.customAssertValue("0", response.get("Atms.PageOffset"))
        self.customAssertValue("26", response.get("Atms.TotalCount"))
        self.customAssertValue("Sandbox ATM Location 1", response.get("Atms.Atm[0].Location.Name"))
        self.customAssertValue("0.9320591049747101", response.get("Atms.Atm[0].Location.Distance"))
        self.customAssertValue("MILE", response.get("Atms.Atm[0].Location.DistanceUnit"))
        self.customAssertValue("4201 Leverton Cove Road", response.get("Atms.Atm[0].Location.Address.Line1"))
        self.customAssertValue("SPRINGFIELD", response.get("Atms.Atm[0].Location.Address.City"))
        self.customAssertValue("11101", response.get("Atms.Atm[0].Location.Address.PostalCode"))
        self.customAssertValue("UYQQQQ", response.get("Atms.Atm[0].Location.Address.CountrySubdivision.Name"))
        self.customAssertValue("QQ", response.get("Atms.Atm[0].Location.Address.CountrySubdivision.Code"))
        self.customAssertValue("UYQQQRR", response.get("Atms.Atm[0].Location.Address.Country.Name"))
        self.customAssertValue("UYQ", response.get("Atms.Atm[0].Location.Address.Country.Code"))
        self.customAssertValue("38.76006576913497", response.get("Atms.Atm[0].Location.Point.Latitude"))
        self.customAssertValue("-90.74615107952418", response.get("Atms.Atm[0].Location.Point.Longitude"))
        self.customAssertValue("OTHER", response.get("Atms.Atm[0].Location.LocationType.Type"))
        self.customAssertValue("NO", response.get("Atms.Atm[0].HandicapAccessible"))
        self.customAssertValue("NO", response.get("Atms.Atm[0].Camera"))
        self.customAssertValue("UNKNOWN", response.get("Atms.Atm[0].Availability"))
        self.customAssertValue("UNKNOWN", response.get("Atms.Atm[0].AccessFees"))
        self.customAssertValue("Sandbox ATM 1", response.get("Atms.Atm[0].Owner"))
        self.customAssertValue("NO", response.get("Atms.Atm[0].SharedDeposit"))
        self.customAssertValue("NO", response.get("Atms.Atm[0].SurchargeFreeAlliance"))
        self.customAssertValue("DOES_NOT_PARTICIPATE_IN_SFA", response.get("Atms.Atm[0].SurchargeFreeAllianceNetwork"))
        self.customAssertValue("Sandbox", response.get("Atms.Atm[0].Sponsor"))
        self.customAssertValue("1", response.get("Atms.Atm[0].SupportEMV"))
        self.customAssertValue("1", response.get("Atms.Atm[0].InternationalMaestroAccepted"))
        

        BaseTest.putResponse("atm_locations", response);

    
        
    

if __name__ == '__main__':
    unittest.main()

