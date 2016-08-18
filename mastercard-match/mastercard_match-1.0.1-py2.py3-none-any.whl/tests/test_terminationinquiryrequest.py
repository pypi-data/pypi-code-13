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


class TerminationInquiryRequestTest(BaseTest):

    def setUp(self):
        keyFile = join(dirname(realpath(__file__)),"resources","mcapi_sandbox_key.p12")
        auth = OAuthAuthentication("L5BsiPgaF-O3qA36znUATgQXwJB6MRoMSdhjd7wt50c97279!50596e52466e3966546d434b7354584c4975693238513d3d",keyFile, "alias", "password")
        Config.setAuthentication(auth)
        Config.setDebug(True)

    
        
                
    def test_example_termination_inquiry(self):
        mapObj = RequestMap()
        mapObj.set("PageOffset", "0")
        mapObj.set("PageLength", "10")
        mapObj.set("TerminationInquiryRequest.AcquirerId", "1996")
        mapObj.set("TerminationInquiryRequest.Merchant.Name", "XYZTEST  XYZTECHMERCHANT")
        mapObj.set("TerminationInquiryRequest.Merchant.DoingBusinessAsName", "XYZTEST  XYZTECHMERCHANT")
        mapObj.set("TerminationInquiryRequest.Merchant.AltPhoneNumber", "3098876333")
        mapObj.set("TerminationInquiryRequest.Merchant.Address.Line1", "88 Nounce World")
        mapObj.set("TerminationInquiryRequest.Merchant.Address.Line2", "APT 9009")
        mapObj.set("TerminationInquiryRequest.Merchant.Address.City", "MICKENVINCE")
        mapObj.set("TerminationInquiryRequest.Merchant.Address.CountrySubdivision", "MO")
        mapObj.set("TerminationInquiryRequest.Merchant.Address.PostalCode", "66559")
        mapObj.set("TerminationInquiryRequest.Merchant.Address.Country", "USA")
        mapObj.set("TerminationInquiryRequest.Merchant.ServiceProvLegal", "JJC WORKSHIRE")
        mapObj.set("TerminationInquiryRequest.Merchant.Principal.FirstName", "PRINCE")
        mapObj.set("TerminationInquiryRequest.Merchant.Principal.LastName", "HENREY")
        mapObj.set("TerminationInquiryRequest.Merchant.Principal.PhoneNumber", "9983339923")
        mapObj.set("TerminationInquiryRequest.Merchant.Principal.AltPhoneNumber", "6365689336")
        mapObj.set("TerminationInquiryRequest.Merchant.Principal.Address.CountrySubdivision", "IL")
        mapObj.set("TerminationInquiryRequest.Merchant.Principal.Address.PostalCode", "66579")
        mapObj.set("TerminationInquiryRequest.Merchant.Principal.Address.Country", "USA")
        mapObj.set("TerminationInquiryRequest.Merchant.SearchCriteria.SearchAll", "Y")
        mapObj.set("TerminationInquiryRequest.Merchant.SearchCriteria.MinPossibleMatchCount", "1")
        

        

        response = TerminationInquiryRequest.create(mapObj)
        self.customAssertValue("0", response.get("TerminationInquiry.PageOffset"))
        self.customAssertValue("14", response.get("TerminationInquiry.PossibleMerchantMatches[0].TotalLength"))
        self.customAssertValue("XYZTEST  XYZTECHMERCHANT", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[0].Merchant.Name"))
        self.customAssertValue("XYZTEST  XYZTECHMERCHANT", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[0].Merchant.DoingBusinessAsName"))
        self.customAssertValue("1996", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[0].Merchant.AddedByAcquirerID"))
        self.customAssertValue("10/13/2015", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[0].Merchant.AddedOnDate"))
        self.customAssertValue("5675543210", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[0].Merchant.PhoneNumber"))
        self.customAssertValue("5672655441", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[0].Merchant.AltPhoneNumber"))
        self.customAssertValue("6700 BEN NEVIS", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[0].Merchant.Address.Line1"))
        self.customAssertValue("GLASGOW", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[0].Merchant.Address.City"))
        self.customAssertValue("MA", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[0].Merchant.Address.CountrySubdivision"))
        self.customAssertValue("93137", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[0].Merchant.Address.PostalCode"))
        self.customAssertValue("USA", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[0].Merchant.Address.Country"))
        self.customAssertValue("*****", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[0].Merchant.CountrySubdivisionTaxId"))
        self.customAssertValue("*****", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[0].Merchant.NationalTaxId"))
        self.customAssertValue("TESTXYZ SVC PRVDER", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[0].Merchant.ServiceProvLegal"))
        self.customAssertValue("JNL ASSOC", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[0].Merchant.ServiceProvDBA"))
        self.customAssertValue("PAUL", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[0].Merchant.Principal[0].FirstName"))
        self.customAssertValue("HEMINGHOFF", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[0].Merchant.Principal[0].LastName"))
        self.customAssertValue("*****", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[0].Merchant.Principal[0].NationalId"))
        self.customAssertValue("3906541234", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[0].Merchant.Principal[0].PhoneNumber"))
        self.customAssertValue("4567390234", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[0].Merchant.Principal[0].AltPhoneNumber"))
        self.customAssertValue("2200 SHEPLEY DRIVE", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[0].Merchant.Principal[0].Address.Line1"))
        self.customAssertValue("SUITE 789", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[0].Merchant.Principal[0].Address.Line2"))
        self.customAssertValue("BROWNSVILLE", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[0].Merchant.Principal[0].Address.City"))
        self.customAssertValue("MO", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[0].Merchant.Principal[0].Address.CountrySubdivision"))
        self.customAssertValue("89022", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[0].Merchant.Principal[0].Address.PostalCode"))
        self.customAssertValue("USA", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[0].Merchant.Principal[0].Address.Country"))
        self.customAssertValue("*****", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[0].Merchant.Principal[0].DriversLicense.Number"))
        self.customAssertValue("MS", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[0].Merchant.Principal[0].DriversLicense.CountrySubdivision"))
        self.customAssertValue("USA", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[0].Merchant.Principal[0].DriversLicense.Country"))
        self.customAssertValue("WWW.TESTJJ.COM", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[0].Merchant.UrlGroup[0].NoMatchUrls.Url[0]"))
        self.customAssertValue("WWW.JNLTESTJJ.COM", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[0].Merchant.UrlGroup[0].NoMatchUrls.Url[1]"))
        self.customAssertValue("04", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[0].Merchant.TerminationReasonCode"))
        self.customAssertValue("M01", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[0].MerchantMatch.Name"))
        self.customAssertValue("M02", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[0].MerchantMatch.DoingBusinessAsName"))
        self.customAssertValue("M00", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[0].MerchantMatch.Address"))
        self.customAssertValue("M00", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[0].MerchantMatch.PhoneNumber"))
        self.customAssertValue("M00", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[0].MerchantMatch.AltPhoneNumber"))
        self.customAssertValue("M00", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[0].MerchantMatch.CountrySubdivisionTaxId"))
        self.customAssertValue("M00", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[0].MerchantMatch.NationalTaxId"))
        self.customAssertValue("M00", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[0].MerchantMatch.ServiceProvLegal"))
        self.customAssertValue("M00", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[0].MerchantMatch.ServiceProvDBA"))
        self.customAssertValue("M00", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[0].MerchantMatch.PrincipalMatch[0].Name"))
        self.customAssertValue("M00", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[0].MerchantMatch.PrincipalMatch[0].Address"))
        self.customAssertValue("M00", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[0].MerchantMatch.PrincipalMatch[0].PhoneNumber"))
        self.customAssertValue("M00", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[0].MerchantMatch.PrincipalMatch[0].AltPhoneNumber"))
        self.customAssertValue("M00", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[0].MerchantMatch.PrincipalMatch[0].NationalId"))
        self.customAssertValue("M00", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[0].MerchantMatch.PrincipalMatch[0].DriversLicense"))
        self.customAssertValue("XYZTEST  XYZTECHMERCHANT", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[1].Merchant.Name"))
        self.customAssertValue("XYZTEST  XYZTECHMERCHANT", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[1].Merchant.DoingBusinessAsName"))
        self.customAssertValue("1996", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[1].Merchant.AddedByAcquirerID"))
        self.customAssertValue("01/20/2016", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[1].Merchant.AddedOnDate"))
        self.customAssertValue("5675543210", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[1].Merchant.PhoneNumber"))
        self.customAssertValue("5672655441", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[1].Merchant.AltPhoneNumber"))
        self.customAssertValue("6700 BEN NEVIS", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[1].Merchant.Address.Line1"))
        self.customAssertValue("GLASGOW", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[1].Merchant.Address.City"))
        self.customAssertValue("MA", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[1].Merchant.Address.CountrySubdivision"))
        self.customAssertValue("93137", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[1].Merchant.Address.PostalCode"))
        self.customAssertValue("USA", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[1].Merchant.Address.Country"))
        self.customAssertValue("*****", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[1].Merchant.CountrySubdivisionTaxId"))
        self.customAssertValue("*****", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[1].Merchant.NationalTaxId"))
        self.customAssertValue("TESTXYZ SVC PRVDER", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[1].Merchant.ServiceProvLegal"))
        self.customAssertValue("JNL ASSOC", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[1].Merchant.ServiceProvDBA"))
        self.customAssertValue("PAUL", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[1].Merchant.Principal[0].FirstName"))
        self.customAssertValue("HEMINGHOFF", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[1].Merchant.Principal[0].LastName"))
        self.customAssertValue("*****", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[1].Merchant.Principal[0].NationalId"))
        self.customAssertValue("3906541234", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[1].Merchant.Principal[0].PhoneNumber"))
        self.customAssertValue("4567390234", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[1].Merchant.Principal[0].AltPhoneNumber"))
        self.customAssertValue("2200 SHEPLEY DRIVE", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[1].Merchant.Principal[0].Address.Line1"))
        self.customAssertValue("SUITE 789", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[1].Merchant.Principal[0].Address.Line2"))
        self.customAssertValue("BROWNSVILLE", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[1].Merchant.Principal[0].Address.City"))
        self.customAssertValue("MO", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[1].Merchant.Principal[0].Address.CountrySubdivision"))
        self.customAssertValue("89022", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[1].Merchant.Principal[0].Address.PostalCode"))
        self.customAssertValue("USA", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[1].Merchant.Principal[0].Address.Country"))
        self.customAssertValue("*****", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[1].Merchant.Principal[0].DriversLicense.Number"))
        self.customAssertValue("MS", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[1].Merchant.Principal[0].DriversLicense.CountrySubdivision"))
        self.customAssertValue("USA", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[1].Merchant.Principal[0].DriversLicense.Country"))
        self.customAssertValue("WWW.TESTJJ.COM", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[1].Merchant.UrlGroup[0].NoMatchUrls.Url[0]"))
        self.customAssertValue("WWW.JNLTESTJJ.COM", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[1].Merchant.UrlGroup[0].NoMatchUrls.Url[1]"))
        self.customAssertValue("04", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[1].Merchant.TerminationReasonCode"))
        self.customAssertValue("M01", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[1].MerchantMatch.Name"))
        self.customAssertValue("M02", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[1].MerchantMatch.DoingBusinessAsName"))
        self.customAssertValue("M00", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[1].MerchantMatch.Address"))
        self.customAssertValue("M00", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[1].MerchantMatch.PhoneNumber"))
        self.customAssertValue("M00", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[1].MerchantMatch.AltPhoneNumber"))
        self.customAssertValue("M00", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[1].MerchantMatch.CountrySubdivisionTaxId"))
        self.customAssertValue("M00", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[1].MerchantMatch.NationalTaxId"))
        self.customAssertValue("M00", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[1].MerchantMatch.ServiceProvLegal"))
        self.customAssertValue("M00", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[1].MerchantMatch.ServiceProvDBA"))
        self.customAssertValue("M00", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[1].MerchantMatch.PrincipalMatch[0].Name"))
        self.customAssertValue("M00", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[1].MerchantMatch.PrincipalMatch[0].Address"))
        self.customAssertValue("M00", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[1].MerchantMatch.PrincipalMatch[0].PhoneNumber"))
        self.customAssertValue("M00", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[1].MerchantMatch.PrincipalMatch[0].AltPhoneNumber"))
        self.customAssertValue("M00", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[1].MerchantMatch.PrincipalMatch[0].NationalId"))
        self.customAssertValue("M00", response.get("TerminationInquiry.PossibleMerchantMatches[0].TerminatedMerchant[1].MerchantMatch.PrincipalMatch[0].DriversLicense"))
        

        BaseTest.putResponse("example_termination_inquiry", response);

    
        
        
        
        
        
        
    

if __name__ == '__main__':
    unittest.main()

