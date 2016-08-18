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
from mastercardplaces import *


class MerchantPointOfInterestTest(BaseTest):

    def setUp(self):
        keyFile = join(dirname(realpath(__file__)),"resources","mcapi_sandbox_key.p12")
        auth = OAuthAuthentication("L5BsiPgaF-O3qA36znUATgQXwJB6MRoMSdhjd7wt50c97279!50596e52466e3966546d434b7354584c4975693238513d3d",keyFile, "alias", "password")
        Config.setAuthentication(auth)
        Config.setDebug(True)

    
        
                
    def test_example_merchantpoi(self):
        mapObj = RequestMap()
        mapObj.set("pageOffset", "0")
        mapObj.set("pageLength", "10")
        mapObj.set("radiusSearch", "false")
        mapObj.set("unit", "km")
        mapObj.set("distance", "14")
        mapObj.set("place.countryCode", "USA")
        

        

        response = MerchantPointOfInterest.create(mapObj)
        self.customAssertValue("0", response.get("MerchantPOIResponse.pageOffset"))
        self.customAssertValue("2000", response.get("MerchantPOIResponse.totalCount"))
        self.customAssertValue("SABAS WESTERN WEAR", response.get("MerchantPOIResponse.places.place[0].merchantName"))
        self.customAssertValue("SABA'S WESTERN WEAR", response.get("MerchantPOIResponse.places.place[0].cleansedMerchantName"))
        self.customAssertValue("67 W BOSTON", response.get("MerchantPOIResponse.places.place[0].streetAddr"))
        self.customAssertValue("67 W BOSTON ST", response.get("MerchantPOIResponse.places.place[0].cleansedStreetAddr"))
        self.customAssertValue("CHANDLER", response.get("MerchantPOIResponse.places.place[0].cityName"))
        self.customAssertValue("CHANDLER", response.get("MerchantPOIResponse.places.place[0].cleansedCityName"))
        self.customAssertValue("AZ", response.get("MerchantPOIResponse.places.place[0].stateProvidenceCode"))
        self.customAssertValue("AZ", response.get("MerchantPOIResponse.places.place[0].cleansedStateProvidenceCode"))
        self.customAssertValue("85225", response.get("MerchantPOIResponse.places.place[0].postalCode"))
        self.customAssertValue("85225-7801", response.get("MerchantPOIResponse.places.place[0].cleansedPostalCode"))
        self.customAssertValue("USA", response.get("MerchantPOIResponse.places.place[0].countryCode"))
        self.customAssertValue("USA", response.get("MerchantPOIResponse.places.place[0].cleansedCountryCode"))
        self.customAssertValue("4809634496", response.get("MerchantPOIResponse.places.place[0].telephoneNumber"))
        self.customAssertValue("(480) 963-4496", response.get("MerchantPOIResponse.places.place[0].cleansedTelephoneNumber"))
        self.customAssertValue("5999", response.get("MerchantPOIResponse.places.place[0].mccCode"))
        self.customAssertValue("SABA'S WESTERN WEAR", response.get("MerchantPOIResponse.places.place[0].legalCorporateName"))
        self.customAssertValue("DAVID'S WESTERN STORES  INC.", response.get("MerchantPOIResponse.places.place[0].cleansedLegalCorporateName"))
        self.customAssertValue("DVG", response.get("MerchantPOIResponse.places.place[0].industry"))
        self.customAssertValue("GEN", response.get("MerchantPOIResponse.places.place[0].superIndustry"))
        self.customAssertValue("12/31/1997", response.get("MerchantPOIResponse.places.place[0].dateEstablished"))
        self.customAssertValue("FALSE", response.get("MerchantPOIResponse.places.place[0].newBusinessFlag"))
        self.customAssertValue("TRUE", response.get("MerchantPOIResponse.places.place[0].inBusiness7DayFlag"))
        self.customAssertValue("TRUE", response.get("MerchantPOIResponse.places.place[0].inBusiness30DayFlag"))
        self.customAssertValue("TRUE", response.get("MerchantPOIResponse.places.place[0].inBusiness60DayFlag"))
        self.customAssertValue("TRUE", response.get("MerchantPOIResponse.places.place[0].inBusiness90DayFlag"))
        self.customAssertValue("TRUE", response.get("MerchantPOIResponse.places.place[0].inBusiness180DayFlag"))
        self.customAssertValue("TRUE", response.get("MerchantPOIResponse.places.place[0].inBusiness360DayFlag"))
        self.customAssertValue("33.302154", response.get("MerchantPOIResponse.places.place[0].latitude"))
        self.customAssertValue("-111.842276", response.get("MerchantPOIResponse.places.place[0].longitude"))
        self.customAssertValue("STOREFRONT", response.get("MerchantPOIResponse.places.place[0].geocodeQualityIndicator"))
        self.customAssertValue("B", response.get("MerchantPOIResponse.places.place[0].primaryChannelOfDistribution"))
        self.customAssertValue("FALSE", response.get("MerchantPOIResponse.places.place[0].cashBack"))
        self.customAssertValue("FALSE", response.get("MerchantPOIResponse.places.place[0].payAtThePump"))
        self.customAssertValue("TRUE", response.get("MerchantPOIResponse.places.place[0].nfcFlag"))
        self.customAssertValue("5999", response.get("MerchantPOIResponse.places.place[0].aggregateMerchantId"))
        self.customAssertValue("NON-AGGREGATED MISCELLANEOUS AND SPECIALTY RETAIL STORES 5999", response.get("MerchantPOIResponse.places.place[0].aggregateMerchantName"))
        self.customAssertValue("5999", response.get("MerchantPOIResponse.places.place[0].keyAggregateMerchantId"))
        self.customAssertValue("10001460", response.get("MerchantPOIResponse.places.place[0].parentAggregateMerchantId"))
        self.customAssertValue("NON-AGGREGATED", response.get("MerchantPOIResponse.places.place[0].parentAggregateMerchantName"))
        self.customAssertValue("6200", response.get("MerchantPOIResponse.places.place[0].msaCode"))
        self.customAssertValue("453998", response.get("MerchantPOIResponse.places.place[0].naicsCode"))
        self.customAssertValue("753", response.get("MerchantPOIResponse.places.place[0].dmaCode"))
        self.customAssertValue("55476524", response.get("MerchantPOIResponse.places.place[0].locationId"))
        self.customAssertValue("THAKU'S MENS WEAR", response.get("MerchantPOIResponse.places.place[1].merchantName"))
        self.customAssertValue("THAKU'S MENS WEAR", response.get("MerchantPOIResponse.places.place[1].cleansedMerchantName"))
        self.customAssertValue("4320 N SCOTTSDALE ROAD", response.get("MerchantPOIResponse.places.place[1].streetAddr"))
        self.customAssertValue("4320 N SCOTTSDALE RD", response.get("MerchantPOIResponse.places.place[1].cleansedStreetAddr"))
        self.customAssertValue("SCOTTSDALE", response.get("MerchantPOIResponse.places.place[1].cityName"))
        self.customAssertValue("SCOTTSDALE", response.get("MerchantPOIResponse.places.place[1].cleansedCityName"))
        self.customAssertValue("AZ", response.get("MerchantPOIResponse.places.place[1].stateProvidenceCode"))
        self.customAssertValue("AZ", response.get("MerchantPOIResponse.places.place[1].cleansedStateProvidenceCode"))
        self.customAssertValue("85251", response.get("MerchantPOIResponse.places.place[1].postalCode"))
        self.customAssertValue("85251-3312", response.get("MerchantPOIResponse.places.place[1].cleansedPostalCode"))
        self.customAssertValue("USA", response.get("MerchantPOIResponse.places.place[1].countryCode"))
        self.customAssertValue("USA", response.get("MerchantPOIResponse.places.place[1].cleansedCountryCode"))
        self.customAssertValue("4809477070", response.get("MerchantPOIResponse.places.place[1].telephoneNumber"))
        self.customAssertValue("(480) 947-7070", response.get("MerchantPOIResponse.places.place[1].cleansedTelephoneNumber"))
        self.customAssertValue("5611", response.get("MerchantPOIResponse.places.place[1].mccCode"))
        self.customAssertValue("THAKU'S MENSWEAR", response.get("MerchantPOIResponse.places.place[1].legalCorporateName"))
        self.customAssertValue("THAKU OF HONG KONG  INC.", response.get("MerchantPOIResponse.places.place[1].cleansedLegalCorporateName"))
        self.customAssertValue("AAM", response.get("MerchantPOIResponse.places.place[1].industry"))
        self.customAssertValue("AAP", response.get("MerchantPOIResponse.places.place[1].superIndustry"))
        self.customAssertValue("12/31/1997", response.get("MerchantPOIResponse.places.place[1].dateEstablished"))
        self.customAssertValue("FALSE", response.get("MerchantPOIResponse.places.place[1].newBusinessFlag"))
        self.customAssertValue("TRUE", response.get("MerchantPOIResponse.places.place[1].inBusiness7DayFlag"))
        self.customAssertValue("TRUE", response.get("MerchantPOIResponse.places.place[1].inBusiness30DayFlag"))
        self.customAssertValue("TRUE", response.get("MerchantPOIResponse.places.place[1].inBusiness60DayFlag"))
        self.customAssertValue("TRUE", response.get("MerchantPOIResponse.places.place[1].inBusiness90DayFlag"))
        self.customAssertValue("TRUE", response.get("MerchantPOIResponse.places.place[1].inBusiness180DayFlag"))
        self.customAssertValue("TRUE", response.get("MerchantPOIResponse.places.place[1].inBusiness360DayFlag"))
        self.customAssertValue("33.499019", response.get("MerchantPOIResponse.places.place[1].latitude"))
        self.customAssertValue("-111.926223", response.get("MerchantPOIResponse.places.place[1].longitude"))
        self.customAssertValue("STOREFRONT", response.get("MerchantPOIResponse.places.place[1].geocodeQualityIndicator"))
        self.customAssertValue("B", response.get("MerchantPOIResponse.places.place[1].primaryChannelOfDistribution"))
        self.customAssertValue("FALSE", response.get("MerchantPOIResponse.places.place[1].cashBack"))
        self.customAssertValue("FALSE", response.get("MerchantPOIResponse.places.place[1].payAtThePump"))
        self.customAssertValue("TRUE", response.get("MerchantPOIResponse.places.place[1].nfcFlag"))
        self.customAssertValue("5611", response.get("MerchantPOIResponse.places.place[1].aggregateMerchantId"))
        self.customAssertValue("NON-AGGREGATED MEN'S AND BOY'S CLOTHING AND ACCESSORIES STOR 5611", response.get("MerchantPOIResponse.places.place[1].aggregateMerchantName"))
        self.customAssertValue("5611", response.get("MerchantPOIResponse.places.place[1].keyAggregateMerchantId"))
        self.customAssertValue("10001460", response.get("MerchantPOIResponse.places.place[1].parentAggregateMerchantId"))
        self.customAssertValue("NON-AGGREGATED", response.get("MerchantPOIResponse.places.place[1].parentAggregateMerchantName"))
        self.customAssertValue("6200", response.get("MerchantPOIResponse.places.place[1].msaCode"))
        self.customAssertValue("424320", response.get("MerchantPOIResponse.places.place[1].naicsCode"))
        self.customAssertValue("753", response.get("MerchantPOIResponse.places.place[1].dmaCode"))
        self.customAssertValue("55475954", response.get("MerchantPOIResponse.places.place[1].locationId"))
        self.customAssertValue("VAN HEUSEN #071", response.get("MerchantPOIResponse.places.place[2].merchantName"))
        self.customAssertValue("VAN HEUSEN", response.get("MerchantPOIResponse.places.place[2].cleansedMerchantName"))
        self.customAssertValue("COOGAN BLVD", response.get("MerchantPOIResponse.places.place[2].streetAddr"))
        self.customAssertValue("1 COOGAN BLVD", response.get("MerchantPOIResponse.places.place[2].cleansedStreetAddr"))
        self.customAssertValue("MYSTIC", response.get("MerchantPOIResponse.places.place[2].cityName"))
        self.customAssertValue("MYSTIC", response.get("MerchantPOIResponse.places.place[2].cleansedCityName"))
        self.customAssertValue("CT", response.get("MerchantPOIResponse.places.place[2].stateProvidenceCode"))
        self.customAssertValue("CT", response.get("MerchantPOIResponse.places.place[2].cleansedStateProvidenceCode"))
        self.customAssertValue("06355", response.get("MerchantPOIResponse.places.place[2].postalCode"))
        self.customAssertValue("06355-1927", response.get("MerchantPOIResponse.places.place[2].cleansedPostalCode"))
        self.customAssertValue("USA", response.get("MerchantPOIResponse.places.place[2].countryCode"))
        self.customAssertValue("USA", response.get("MerchantPOIResponse.places.place[2].cleansedCountryCode"))
        self.customAssertValue("8605729972", response.get("MerchantPOIResponse.places.place[2].telephoneNumber"))
        self.customAssertValue("8605729972", response.get("MerchantPOIResponse.places.place[2].cleansedTelephoneNumber"))
        self.customAssertValue("5611", response.get("MerchantPOIResponse.places.place[2].mccCode"))
        self.customAssertValue("VAN HEUSEN RETAI", response.get("MerchantPOIResponse.places.place[2].legalCorporateName"))
        self.customAssertValue("VAN HEUSEN RETAI", response.get("MerchantPOIResponse.places.place[2].cleansedLegalCorporateName"))
        self.customAssertValue("AAF", response.get("MerchantPOIResponse.places.place[2].industry"))
        self.customAssertValue("AAP", response.get("MerchantPOIResponse.places.place[2].superIndustry"))
        self.customAssertValue("12/31/1997", response.get("MerchantPOIResponse.places.place[2].dateEstablished"))
        self.customAssertValue("FALSE", response.get("MerchantPOIResponse.places.place[2].newBusinessFlag"))
        self.customAssertValue("TRUE", response.get("MerchantPOIResponse.places.place[2].inBusiness7DayFlag"))
        self.customAssertValue("TRUE", response.get("MerchantPOIResponse.places.place[2].inBusiness30DayFlag"))
        self.customAssertValue("TRUE", response.get("MerchantPOIResponse.places.place[2].inBusiness60DayFlag"))
        self.customAssertValue("TRUE", response.get("MerchantPOIResponse.places.place[2].inBusiness90DayFlag"))
        self.customAssertValue("TRUE", response.get("MerchantPOIResponse.places.place[2].inBusiness180DayFlag"))
        self.customAssertValue("TRUE", response.get("MerchantPOIResponse.places.place[2].inBusiness360DayFlag"))
        self.customAssertValue("41.372157", response.get("MerchantPOIResponse.places.place[2].latitude"))
        self.customAssertValue("-71.955404", response.get("MerchantPOIResponse.places.place[2].longitude"))
        self.customAssertValue("STOREFRONT", response.get("MerchantPOIResponse.places.place[2].geocodeQualityIndicator"))
        self.customAssertValue("B", response.get("MerchantPOIResponse.places.place[2].primaryChannelOfDistribution"))
        self.customAssertValue("FALSE", response.get("MerchantPOIResponse.places.place[2].cashBack"))
        self.customAssertValue("FALSE", response.get("MerchantPOIResponse.places.place[2].payAtThePump"))
        self.customAssertValue("FALSE", response.get("MerchantPOIResponse.places.place[2].nfcFlag"))
        self.customAssertValue("11917", response.get("MerchantPOIResponse.places.place[2].aggregateMerchantId"))
        self.customAssertValue("VAN HEUSEN", response.get("MerchantPOIResponse.places.place[2].aggregateMerchantName"))
        self.customAssertValue("11917", response.get("MerchantPOIResponse.places.place[2].keyAggregateMerchantId"))
        self.customAssertValue("10000205", response.get("MerchantPOIResponse.places.place[2].parentAggregateMerchantId"))
        self.customAssertValue("PHILLIPS-VAN HEUSEN CORP", response.get("MerchantPOIResponse.places.place[2].parentAggregateMerchantName"))
        self.customAssertValue("448140", response.get("MerchantPOIResponse.places.place[2].naicsCode"))
        self.customAssertValue("533", response.get("MerchantPOIResponse.places.place[2].dmaCode"))
        self.customAssertValue("55475387", response.get("MerchantPOIResponse.places.place[2].locationId"))
        

        BaseTest.putResponse("example_merchantpoi", response);

    
        
        
        
        
        
        
    

if __name__ == '__main__':
    unittest.main()

