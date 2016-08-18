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


class SpendingPulseReportTest(BaseTest):

    def setUp(self):
        keyFile = join(dirname(realpath(__file__)),"resources","mcapi_sandbox_key.p12")
        auth = OAuthAuthentication("L5BsiPgaF-O3qA36znUATgQXwJB6MRoMSdhjd7wt50c97279!50596e52466e3966546d434b7354584c4975693238513d3d",keyFile, "alias", "password")
        Config.setAuthentication(auth)
        Config.setDebug(True)

    
        
        
        
        
        
        
                
    def test_example_spendingpulse(self):
        mapObj = RequestMap()
        mapObj.set("CurrentRow", "1")
        mapObj.set("Offset", "25")
        mapObj.set("ProductLine", "Weekly Sales")
        mapObj.set("PublicationCoveragePeriod", "Week")
        mapObj.set("Country", "US")
        mapObj.set("ReportType", "reportA")
        mapObj.set("Period", "Weekly")
        mapObj.set("Sector", "sectorA")
        mapObj.set("Ecomm", "Y")
        

        

        response = SpendingPulseReport.query(mapObj)
        self.customAssertValue("2", response.get("SpendingPulseList.Count"))
        self.customAssertValue("Success", response.get("SpendingPulseList.Message"))
        self.customAssertValue("US", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].Country"))
        self.customAssertValue("US Dollars", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].CurrencyOfForSalesValue"))
        self.customAssertValue("Y", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].Ecomm"))
        self.customAssertValue("0.0012", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].ImpliedDeflatorMonthOverMonthChange"))
        self.customAssertValue("0.0011", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].ImpliedDeflatorYearOverYearChange"))
        self.customAssertValue("2015-05", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].NonGregorianReportingPeriod"))
        self.customAssertValue("Weekly", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].Period"))
        self.customAssertValue("5/14/2015", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].PeriodEndDate"))
        self.customAssertValue("5/8/2015", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].PeriodStartDate"))
        self.customAssertValue("Y", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].PriceAdjustmentFlag"))
        self.customAssertValue("0.012", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].PriceIndex3MonthMovingAverageChange"))
        self.customAssertValue("0.005", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].PriceIndexMonthOverMonthChange"))
        self.customAssertValue("0.00115", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].PriceIndexValue"))
        self.customAssertValue("0.00115", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].PriceIndexYearOverYearChange"))
        self.customAssertValue("Weekly Sales", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].ProductLine"))
        self.customAssertValue("Week", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].PublicationCoveragePeriod"))
        self.customAssertValue("reportA", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].ReportType"))
        self.customAssertValue("G", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].ReportingCalender"))
        self.customAssertValue("150", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].Sales3MonthMovingAverageChange"))
        self.customAssertValue("50", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].SalesMonthOverMonthChange"))
        self.customAssertValue("5", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].SalesValueIndex"))
        self.customAssertValue("500", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].SalesYearOverYearChange"))
        self.customAssertValue("20", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].SalesYearToDateChange"))
        self.customAssertValue("0.68", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].SameStoreSalesIndex3MonthMovingAverageChange"))
        self.customAssertValue("0.6", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].SameStoreSalesIndexYearOverYearChange"))
        self.customAssertValue("Y", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].SeasonalAdjustmentFlag"))
        self.customAssertValue("sectorA", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].Sector"))
        self.customAssertValue("seg1", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].Segment"))
        self.customAssertValue("region", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].SubGeographyValue"))
        self.customAssertValue("subA", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].SubSector"))
        self.customAssertValue("0.58", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].TransactionIndex3MonthMovingAverageChange"))
        self.customAssertValue("0.57", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].TransactionIndexMonthOverMonthChange"))
        self.customAssertValue("0.5", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].TransactionIndexValue"))
        self.customAssertValue("0.56", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[0].TransactionIndexYearOverYearChange"))
        self.customAssertValue("US", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].Country"))
        self.customAssertValue("US Dollars", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].CurrencyOfForSalesValue"))
        self.customAssertValue("Y", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].Ecomm"))
        self.customAssertValue("0.0012", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].ImpliedDeflatorMonthOverMonthChange"))
        self.customAssertValue("0.0011", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].ImpliedDeflatorYearOverYearChange"))
        self.customAssertValue("2015-05", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].NonGregorianReportingPeriod"))
        self.customAssertValue("Weekly", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].Period"))
        self.customAssertValue("5/7/2015", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].PeriodEndDate"))
        self.customAssertValue("5/1/2015", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].PeriodStartDate"))
        self.customAssertValue("Y", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].PriceAdjustmentFlag"))
        self.customAssertValue("0.013", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].PriceIndex3MonthMovingAverageChange"))
        self.customAssertValue("0.006", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].PriceIndexMonthOverMonthChange"))
        self.customAssertValue("0.000116", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].PriceIndexValue"))
        self.customAssertValue("0.00116", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].PriceIndexYearOverYearChange"))
        self.customAssertValue("Weekly Sales", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].ProductLine"))
        self.customAssertValue("Week", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].PublicationCoveragePeriod"))
        self.customAssertValue("reportA", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].ReportType"))
        self.customAssertValue("G", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].ReportingCalender"))
        self.customAssertValue("160", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].Sales3MonthMovingAverageChange"))
        self.customAssertValue("60", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].SalesMonthOverMonthChange"))
        self.customAssertValue("6", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].SalesValueIndex"))
        self.customAssertValue("600", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].SalesYearOverYearChange"))
        self.customAssertValue("30", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].SalesYearToDateChange"))
        self.customAssertValue("0.88", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].SameStoreSalesIndex3MonthMovingAverageChange"))
        self.customAssertValue("0.8", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].SameStoreSalesIndexYearOverYearChange"))
        self.customAssertValue("Y", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].SeasonalAdjustmentFlag"))
        self.customAssertValue("sectorA", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].Sector"))
        self.customAssertValue("seg1", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].Segment"))
        self.customAssertValue("region", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].SubGeographyValue"))
        self.customAssertValue("subA", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].SubSector"))
        self.customAssertValue("0.48", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].TransactionIndex3MonthMovingAverageChange"))
        self.customAssertValue("0.47", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].TransactionIndexMonthOverMonthChange"))
        self.customAssertValue("0.4", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].TransactionIndexValue"))
        self.customAssertValue("0.46", response.get("SpendingPulseList.SpendingPulseArray.SpendingPulseRecord[1].TransactionIndexYearOverYearChange"))
        

        BaseTest.putResponse("example_spendingpulse", response);

    
        
    

if __name__ == '__main__':
    unittest.main()

