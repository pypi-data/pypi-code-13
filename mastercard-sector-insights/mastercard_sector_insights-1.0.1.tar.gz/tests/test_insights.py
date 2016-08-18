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
from mastercardsectorinsights import *


class InsightsTest(BaseTest):

    def setUp(self):
        keyFile = join(dirname(realpath(__file__)),"resources","mcapi_sandbox_key.p12")
        auth = OAuthAuthentication("L5BsiPgaF-O3qA36znUATgQXwJB6MRoMSdhjd7wt50c97279!50596e52466e3966546d434b7354584c4975693238513d3d",keyFile, "alias", "password")
        Config.setAuthentication(auth)
        Config.setDebug(True)

    
        
        
        
        
        
        
                
    def test_example_insights(self):
        mapObj = RequestMap()
        mapObj.set("CurrentRow", "1")
        mapObj.set("Offset", "25")
        mapObj.set("Country", "US")
        

        

        response = Insights.query(mapObj)
        self.customAssertValue("70", response.get("SectorRecordList.Count"))
        self.customAssertValue("Success", response.get("SectorRecordList.Message"))
        self.customAssertValue("US", response.get("SectorRecordList.SectorRecordArray.SectorRecord[0].Country"))
        self.customAssertValue("U.S. Natural and Organic Grocery Stores", response.get("SectorRecordList.SectorRecordArray.SectorRecord[0].Sector"))
        self.customAssertValue("NO", response.get("SectorRecordList.SectorRecordArray.SectorRecord[0].Ecomm"))
        self.customAssertValue("Monthly", response.get("SectorRecordList.SectorRecordArray.SectorRecord[0].Period"))
        self.customAssertValue("11/30/2014", response.get("SectorRecordList.SectorRecordArray.SectorRecord[0].BeginDate"))
        self.customAssertValue("1/3/2015", response.get("SectorRecordList.SectorRecordArray.SectorRecord[0].EndDate"))
        self.customAssertValue("0.049201983", response.get("SectorRecordList.SectorRecordArray.SectorRecord[0].SalesIndex"))
        self.customAssertValue("-0.029602284", response.get("SectorRecordList.SectorRecordArray.SectorRecord[0].AverageTicketIndex"))
        self.customAssertValue("7146577.851", response.get("SectorRecordList.SectorRecordArray.SectorRecord[0].SalesIndexValue"))
        self.customAssertValue("US", response.get("SectorRecordList.SectorRecordArray.SectorRecord[1].Country"))
        self.customAssertValue("U.S. Natural and Organic Grocery Stores", response.get("SectorRecordList.SectorRecordArray.SectorRecord[1].Sector"))
        self.customAssertValue("NO", response.get("SectorRecordList.SectorRecordArray.SectorRecord[1].Ecomm"))
        self.customAssertValue("Monthly", response.get("SectorRecordList.SectorRecordArray.SectorRecord[1].Period"))
        self.customAssertValue("11/2/2014", response.get("SectorRecordList.SectorRecordArray.SectorRecord[1].BeginDate"))
        self.customAssertValue("11/29/2014", response.get("SectorRecordList.SectorRecordArray.SectorRecord[1].EndDate"))
        self.customAssertValue("0.074896863", response.get("SectorRecordList.SectorRecordArray.SectorRecord[1].SalesIndex"))
        self.customAssertValue("-0.007884916", response.get("SectorRecordList.SectorRecordArray.SectorRecord[1].AverageTicketIndex"))
        self.customAssertValue("5390273.888", response.get("SectorRecordList.SectorRecordArray.SectorRecord[1].SalesIndexValue"))
        self.customAssertValue("US", response.get("SectorRecordList.SectorRecordArray.SectorRecord[2].Country"))
        self.customAssertValue("U.S. Natural and Organic Grocery Stores", response.get("SectorRecordList.SectorRecordArray.SectorRecord[2].Sector"))
        self.customAssertValue("NO", response.get("SectorRecordList.SectorRecordArray.SectorRecord[2].Ecomm"))
        self.customAssertValue("Monthly", response.get("SectorRecordList.SectorRecordArray.SectorRecord[2].Period"))
        self.customAssertValue("10/5/2014", response.get("SectorRecordList.SectorRecordArray.SectorRecord[2].BeginDate"))
        self.customAssertValue("11/1/2014", response.get("SectorRecordList.SectorRecordArray.SectorRecord[2].EndDate"))
        self.customAssertValue("0.077937282", response.get("SectorRecordList.SectorRecordArray.SectorRecord[2].SalesIndex"))
        self.customAssertValue("-0.010073866", response.get("SectorRecordList.SectorRecordArray.SectorRecord[2].AverageTicketIndex"))
        self.customAssertValue("4776139.381", response.get("SectorRecordList.SectorRecordArray.SectorRecord[2].SalesIndexValue"))
        self.customAssertValue("US", response.get("SectorRecordList.SectorRecordArray.SectorRecord[3].Country"))
        self.customAssertValue("U.S. Natural and Organic Grocery Stores", response.get("SectorRecordList.SectorRecordArray.SectorRecord[3].Sector"))
        self.customAssertValue("NO", response.get("SectorRecordList.SectorRecordArray.SectorRecord[3].Ecomm"))
        self.customAssertValue("Monthly", response.get("SectorRecordList.SectorRecordArray.SectorRecord[3].Period"))
        self.customAssertValue("9/7/2014", response.get("SectorRecordList.SectorRecordArray.SectorRecord[3].BeginDate"))
        self.customAssertValue("10/4/2014", response.get("SectorRecordList.SectorRecordArray.SectorRecord[3].EndDate"))
        self.customAssertValue("0.089992028", response.get("SectorRecordList.SectorRecordArray.SectorRecord[3].SalesIndex"))
        self.customAssertValue("-0.00577838", response.get("SectorRecordList.SectorRecordArray.SectorRecord[3].AverageTicketIndex"))
        self.customAssertValue("4716899.304", response.get("SectorRecordList.SectorRecordArray.SectorRecord[3].SalesIndexValue"))
        

        BaseTest.putResponse("example_insights", response);

    
        
    

if __name__ == '__main__':
    unittest.main()

