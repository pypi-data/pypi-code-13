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


class RetailUnitsMetricsTest(BaseTest):

    def setUp(self):
        keyFile = join(dirname(realpath(__file__)),"resources","mcapi_sandbox_key.p12")
        auth = OAuthAuthentication("L5BsiPgaF-O3qA36znUATgQXwJB6MRoMSdhjd7wt50c97279!50596e52466e3966546d434b7354584c4975693238513d3d",keyFile, "alias", "password")
        Config.setAuthentication(auth)
        Config.setDebug(True)

    
        
        
        
        
        
        
                
    def test_example_retail_unit_metrics(self):
        mapObj = RequestMap()
        mapObj.set("PageOffset", "1")
        mapObj.set("PageLength", "10")
        mapObj.set("RetailUnitType", "State")
        mapObj.set("RetailUnitId", "4")
        

        

        response = RetailUnitsMetrics.query(mapObj)
        self.customAssertValue("1", response.get("RetailUnitMetricResponse.PageOffset"))
        self.customAssertValue("4", response.get("RetailUnitMetricResponse.TotalCount"))
        self.customAssertValue("4", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[0].RetailUnitId"))
        self.customAssertValue("STATE", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[0].RetailUnitType"))
        self.customAssertValue("2016/03", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[0].Period"))
        self.customAssertValue("100", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[0].RLIScores.CompositeIndustry"))
        self.customAssertValue("All Retail", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[0].RLIScores.CompositeIndustryName"))
        self.customAssertValue("500", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[0].RLIScores.Sales"))
        self.customAssertValue("500", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[0].RLIScores.Transactions"))
        self.customAssertValue("300", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[0].RLIScores.TicketSize"))
        self.customAssertValue("700", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[0].RLIScores.Growth"))
        self.customAssertValue("600", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[0].RLIScores.Stability"))
        self.customAssertValue("400", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[0].RLIScores.Composite"))
        self.customAssertValue("4", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[1].RetailUnitId"))
        self.customAssertValue("STATE", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[1].RetailUnitType"))
        self.customAssertValue("2016/03", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[1].Period"))
        self.customAssertValue("102", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[1].RLIScores.CompositeIndustry"))
        self.customAssertValue("Eating Places", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[1].RLIScores.CompositeIndustryName"))
        self.customAssertValue("445", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[1].RLIScores.Sales"))
        self.customAssertValue("445", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[1].RLIScores.Transactions"))
        self.customAssertValue("334", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[1].RLIScores.TicketSize"))
        self.customAssertValue("556", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[1].RLIScores.Growth"))
        self.customAssertValue("556", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[1].RLIScores.Stability"))
        self.customAssertValue("445", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[1].RLIScores.Composite"))
        self.customAssertValue("4", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[2].RetailUnitId"))
        self.customAssertValue("STATE", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[2].RetailUnitType"))
        self.customAssertValue("2016/03", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[2].Period"))
        self.customAssertValue("103", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[2].RLIScores.CompositeIndustry"))
        self.customAssertValue("Exclude Eating", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[2].RLIScores.CompositeIndustryName"))
        self.customAssertValue("500", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[2].RLIScores.Sales"))
        self.customAssertValue("500", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[2].RLIScores.Transactions"))
        self.customAssertValue("300", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[2].RLIScores.TicketSize"))
        self.customAssertValue("700", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[2].RLIScores.Growth"))
        self.customAssertValue("600", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[2].RLIScores.Stability"))
        self.customAssertValue("400", response.get("RetailUnitMetricResponse.RetailUnitMetrics.RetailUnitMetric[2].RLIScores.Composite"))
        

        BaseTest.putResponse("example_retail_unit_metrics", response);

    
        
    

if __name__ == '__main__':
    unittest.main()

