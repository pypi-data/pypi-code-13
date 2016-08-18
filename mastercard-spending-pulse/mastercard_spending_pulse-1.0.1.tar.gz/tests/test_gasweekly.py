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


class GasWeeklyTest(BaseTest):

    def setUp(self):
        keyFile = join(dirname(realpath(__file__)),"resources","mcapi_sandbox_key.p12")
        auth = OAuthAuthentication("L5BsiPgaF-O3qA36znUATgQXwJB6MRoMSdhjd7wt50c97279!50596e52466e3966546d434b7354584c4975693238513d3d",keyFile, "alias", "password")
        Config.setAuthentication(auth)
        Config.setDebug(True)

    
        
        
        
        
        
        
                
    def test_example_gasweekly(self):
        mapObj = RequestMap()
        mapObj.set("CurrentRow", "1")
        mapObj.set("Offset", "25")
        

        

        response = GasWeekly.query(mapObj)
        self.customAssertValue("4", response.get("GasWeeklyList.Count"))
        self.customAssertValue("US", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[0].Country"))
        self.customAssertValue("NE", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[0].PADDCode"))
        self.customAssertValue("5", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[0].PADDMillionsofBarrelsSold"))
        self.customAssertValue("0.001", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[0].PADDPercentChangeInBarrelsFromPriorWeek"))
        self.customAssertValue("0.002", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[0].PADDPercentChangeinBarrelsfrom52WeeksAgo"))
        self.customAssertValue("Week", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[0].Period"))
        self.customAssertValue("US Gasoline Weekly", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[0].ProductLine"))
        self.customAssertValue("Week", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[0].PublicationCoveragePeriod"))
        self.customAssertValue("Gas", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[0].ReportType"))
        self.customAssertValue("Gas", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[0].Sector"))
        self.customAssertValue("Gas", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[0].Segment"))
        self.customAssertValue("Gas", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[0].SubSector"))
        self.customAssertValue("5", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[0].TotalBarrelsChangeFromPriorWeek"))
        self.customAssertValue("40", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[0].TotalMillionsOfBarrels4WeekAverage"))
        self.customAssertValue("15", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[0].TotalMillionsOfBarrelsDailyAverage"))
        self.customAssertValue("40", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[0].TotalMillionsOfBarrelsSold"))
        self.customAssertValue("0.005", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[0].TotalPercentChangeInBarrelsFrom52WeeksAgo"))
        self.customAssertValue("0.004", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[0].TotalPercentChangeInBarrelsFromPriorWeek"))
        self.customAssertValue("0.006", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[0].TotalPercentChangeInThe4WeekAverageFrom52WeeksAgo"))
        self.customAssertValue("6/12/2015", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[0].WeekEndDate"))
        self.customAssertValue("US", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[1].Country"))
        self.customAssertValue("CA", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[1].PADDCode"))
        self.customAssertValue("5", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[1].PADDMillionsofBarrelsSold"))
        self.customAssertValue("0.015", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[1].PADDPercentChangeInBarrelsFromPriorWeek"))
        self.customAssertValue("0.025", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[1].PADDPercentChangeinBarrelsfrom52WeeksAgo"))
        self.customAssertValue("Week", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[1].Period"))
        self.customAssertValue("US Gasoline Weekly", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[1].ProductLine"))
        self.customAssertValue("Week", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[1].PublicationCoveragePeriod"))
        self.customAssertValue("Gas", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[1].ReportType"))
        self.customAssertValue("Gas", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[1].Sector"))
        self.customAssertValue("Gas", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[1].Segment"))
        self.customAssertValue("Gas", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[1].SubSector"))
        self.customAssertValue("5", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[1].TotalBarrelsChangeFromPriorWeek"))
        self.customAssertValue("40", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[1].TotalMillionsOfBarrels4WeekAverage"))
        self.customAssertValue("15", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[1].TotalMillionsOfBarrelsDailyAverage"))
        self.customAssertValue("40", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[1].TotalMillionsOfBarrelsSold"))
        self.customAssertValue("0.005", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[1].TotalPercentChangeInBarrelsFrom52WeeksAgo"))
        self.customAssertValue("0.004", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[1].TotalPercentChangeInBarrelsFromPriorWeek"))
        self.customAssertValue("0.006", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[1].TotalPercentChangeInThe4WeekAverageFrom52WeeksAgo"))
        self.customAssertValue("6/12/2015", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[1].WeekEndDate"))
        self.customAssertValue("US", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[2].Country"))
        self.customAssertValue("NE", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[2].PADDCode"))
        self.customAssertValue("6", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[2].PADDMillionsofBarrelsSold"))
        self.customAssertValue("0.002", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[2].PADDPercentChangeInBarrelsFromPriorWeek"))
        self.customAssertValue("0.003", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[2].PADDPercentChangeinBarrelsfrom52WeeksAgo"))
        self.customAssertValue("Week", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[2].Period"))
        self.customAssertValue("US Gasoline Weekly", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[2].ProductLine"))
        self.customAssertValue("Week", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[2].PublicationCoveragePeriod"))
        self.customAssertValue("Gas", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[2].ReportType"))
        self.customAssertValue("Gas", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[2].Sector"))
        self.customAssertValue("Gas", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[2].Segment"))
        self.customAssertValue("Gas", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[2].SubSector"))
        self.customAssertValue("6", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[2].TotalBarrelsChangeFromPriorWeek"))
        self.customAssertValue("50", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[2].TotalMillionsOfBarrels4WeekAverage"))
        self.customAssertValue("16", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[2].TotalMillionsOfBarrelsDailyAverage"))
        self.customAssertValue("50", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[2].TotalMillionsOfBarrelsSold"))
        self.customAssertValue("0.006", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[2].TotalPercentChangeInBarrelsFrom52WeeksAgo"))
        self.customAssertValue("0.005", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[2].TotalPercentChangeInBarrelsFromPriorWeek"))
        self.customAssertValue("0.007", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[2].TotalPercentChangeInThe4WeekAverageFrom52WeeksAgo"))
        self.customAssertValue("6/5/2015", response.get("GasWeeklyList.GasWeeklyArray.GasWeeklyRecord[2].WeekEndDate"))
        self.customAssertValue("Success", response.get("GasWeeklyList.Message"))
        

        BaseTest.putResponse("example_gasweekly", response);

    
        
    

if __name__ == '__main__':
    unittest.main()

