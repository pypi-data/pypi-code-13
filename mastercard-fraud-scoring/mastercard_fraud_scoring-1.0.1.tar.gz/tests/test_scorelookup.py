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
from mastercardfraudscoring import *


class ScoreLookupTest(BaseTest):

    def setUp(self):
        keyFile = join(dirname(realpath(__file__)),"resources","mcapi_sandbox_key.p12")
        auth = OAuthAuthentication("L5BsiPgaF-O3qA36znUATgQXwJB6MRoMSdhjd7wt50c97279!50596e52466e3966546d434b7354584c4975693238513d3d",keyFile, "alias", "password")
        Config.setAuthentication(auth)
        Config.setDebug(True)

    
        
        
                
    def test_example_score(self):
        mapObj = RequestMap()
        mapObj.set("ScoreLookupRequest.TransactionDetail.CustomerIdentifier", "1996")
        mapObj.set("ScoreLookupRequest.TransactionDetail.MerchantIdentifier", "12345")
        mapObj.set("ScoreLookupRequest.TransactionDetail.AccountNumber", "5555555555555555")
        mapObj.set("ScoreLookupRequest.TransactionDetail.AccountPrefix", "555555")
        mapObj.set("ScoreLookupRequest.TransactionDetail.AccountSuffix", "5555")
        mapObj.set("ScoreLookupRequest.TransactionDetail.TransactionAmount", "12500")
        mapObj.set("ScoreLookupRequest.TransactionDetail.TransactionDate", "1231")
        mapObj.set("ScoreLookupRequest.TransactionDetail.TransactionTime", "035931")
        mapObj.set("ScoreLookupRequest.TransactionDetail.BankNetReferenceNumber", "abc123hij")
        mapObj.set("ScoreLookupRequest.TransactionDetail.Stan", "123456")
        

        

        request = ScoreLookup(mapObj)
        response = request.update()
        self.customAssertValue("L5BsiPgaF-O3qA36znUATgQXwJB6MRoMSdhjd7wt50c97279", response.get("ScoreLookup.CustomerIdentifier"))
        self.customAssertValue("1996", response.get("ScoreLookup.TransactionDetail.CustomerIdentifier"))
        self.customAssertValue("12345", response.get("ScoreLookup.TransactionDetail.MerchantIdentifier"))
        self.customAssertValue("5555555555555555", response.get("ScoreLookup.TransactionDetail.AccountNumber"))
        self.customAssertValue("555555", response.get("ScoreLookup.TransactionDetail.AccountPrefix"))
        self.customAssertValue("5555", response.get("ScoreLookup.TransactionDetail.AccountSuffix"))
        self.customAssertValue("12500", response.get("ScoreLookup.TransactionDetail.TransactionAmount"))
        self.customAssertValue("1231", response.get("ScoreLookup.TransactionDetail.TransactionDate"))
        self.customAssertValue("035931", response.get("ScoreLookup.TransactionDetail.TransactionTime"))
        self.customAssertValue("abc123hij", response.get("ScoreLookup.TransactionDetail.BankNetReferenceNumber"))
        self.customAssertValue("123456", response.get("ScoreLookup.TransactionDetail.Stan"))
        self.customAssertValue("2", response.get("ScoreLookup.ScoreResponse.MatchIndicator"))
        self.customAssertValue("681", response.get("ScoreLookup.ScoreResponse.FraudScore"))
        self.customAssertValue("A5", response.get("ScoreLookup.ScoreResponse.ReasonCode"))
        self.customAssertValue("701", response.get("ScoreLookup.ScoreResponse.RulesAdjustedScore"))
        self.customAssertValue("19", response.get("ScoreLookup.ScoreResponse.RulesAdjustedReasonCode"))
        self.customAssertValue("A9", response.get("ScoreLookup.ScoreResponse.RulesAdjustedReasonCodeSecondary"))
        

        BaseTest.putResponse("example_score", response);

    
        
        
        
        
        
    

if __name__ == '__main__':
    unittest.main()

