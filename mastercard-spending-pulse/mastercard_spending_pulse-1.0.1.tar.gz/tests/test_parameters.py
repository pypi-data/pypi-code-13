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
from mastercardspendingpulse import *


class ParametersTest(BaseTest):

    def setUp(self):
        keyFile = join(dirname(realpath(__file__)),"resources","mcapi_sandbox_key.p12")
        auth = OAuthAuthentication("L5BsiPgaF-O3qA36znUATgQXwJB6MRoMSdhjd7wt50c97279!50596e52466e3966546d434b7354584c4975693238513d3d",keyFile, "alias", "password")
        Config.setAuthentication(auth)
        Config.setDebug(True)

    
        
        
        
        
        
        
                
    def test_example_parameters(self):
        mapObj = RequestMap()
        mapObj.set("CurrentRow", "1")
        mapObj.set("Offset", "25")
        

        

        response = Parameters.query(mapObj)
        self.customAssertValue("4", response.get("ParameterList.Count"))
        self.customAssertValue("Success", response.get("ParameterList.Message"))
        self.customAssertValue("US", response.get("ParameterList.ParameterArray.Parameter[0].Country"))
        self.customAssertValue("Y", response.get("ParameterList.ParameterArray.Parameter[0].Ecomm"))
        self.customAssertValue("Weekly", response.get("ParameterList.ParameterArray.Parameter[0].Period"))
        self.customAssertValue("US Gasoline Weekly", response.get("ParameterList.ParameterArray.Parameter[0].ProductLine"))
        self.customAssertValue("Week", response.get("ParameterList.ParameterArray.Parameter[0].PublicationCoveragePeriod"))
        self.customAssertValue("Gas", response.get("ParameterList.ParameterArray.Parameter[0].ReportType"))
        self.customAssertValue("Gas", response.get("ParameterList.ParameterArray.Parameter[0].Sector"))
        self.customAssertValue("US", response.get("ParameterList.ParameterArray.Parameter[1].Country"))
        self.customAssertValue("Y", response.get("ParameterList.ParameterArray.Parameter[1].Ecomm"))
        self.customAssertValue("Monthly", response.get("ParameterList.ParameterArray.Parameter[1].Period"))
        self.customAssertValue("US Gasoline Monthly", response.get("ParameterList.ParameterArray.Parameter[1].ProductLine"))
        self.customAssertValue("Month", response.get("ParameterList.ParameterArray.Parameter[1].PublicationCoveragePeriod"))
        self.customAssertValue("Gas", response.get("ParameterList.ParameterArray.Parameter[1].ReportType"))
        self.customAssertValue("Gas", response.get("ParameterList.ParameterArray.Parameter[1].Sector"))
        self.customAssertValue("US", response.get("ParameterList.ParameterArray.Parameter[2].Country"))
        self.customAssertValue("Y", response.get("ParameterList.ParameterArray.Parameter[2].Ecomm"))
        self.customAssertValue("Weekly", response.get("ParameterList.ParameterArray.Parameter[2].Period"))
        self.customAssertValue("Weekly Sales", response.get("ParameterList.ParameterArray.Parameter[2].ProductLine"))
        self.customAssertValue("Week", response.get("ParameterList.ParameterArray.Parameter[2].PublicationCoveragePeriod"))
        self.customAssertValue("reportA", response.get("ParameterList.ParameterArray.Parameter[2].ReportType"))
        self.customAssertValue("sectorA", response.get("ParameterList.ParameterArray.Parameter[2].Sector"))
        self.customAssertValue("US", response.get("ParameterList.ParameterArray.Parameter[3].Country"))
        self.customAssertValue("Y", response.get("ParameterList.ParameterArray.Parameter[3].Ecomm"))
        self.customAssertValue("Weekly", response.get("ParameterList.ParameterArray.Parameter[3].Period"))
        self.customAssertValue("Weekly Sales", response.get("ParameterList.ParameterArray.Parameter[3].ProductLine"))
        self.customAssertValue("Week", response.get("ParameterList.ParameterArray.Parameter[3].PublicationCoveragePeriod"))
        self.customAssertValue("reportB", response.get("ParameterList.ParameterArray.Parameter[3].ReportType"))
        self.customAssertValue("sectorB", response.get("ParameterList.ParameterArray.Parameter[3].Sector"))
        

        BaseTest.putResponse("example_parameters", response);

    
        
    

if __name__ == '__main__':
    unittest.main()

