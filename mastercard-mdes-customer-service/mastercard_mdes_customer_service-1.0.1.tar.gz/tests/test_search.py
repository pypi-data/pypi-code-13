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
from mastercardmdescustomerservice import *


class SearchTest(BaseTest):

    def setUp(self):
        keyFile = join(dirname(realpath(__file__)),"resources","mcapi_sandbox_key.p12")
        auth = OAuthAuthentication("L5BsiPgaF-O3qA36znUATgQXwJB6MRoMSdhjd7wt50c97279!50596e52466e3966546d434b7354584c4975693238513d3d",keyFile, "alias", "password")
        Config.setAuthentication(auth)
        Config.setDebug(True)

    
        
                
    def test_example_mdes_search_token_unique_ref(self):
        mapObj = RequestMap()
        mapObj.set("SearchRequest.TokenUniqueReference", "DWSPMC00000000010906a349d9ca4eb1a4d53e3c90a11d9c")
        mapObj.set("SearchRequest.AuditInfo.UserId", "A1435477")
        mapObj.set("SearchRequest.AuditInfo.UserName", "John Smith")
        mapObj.set("SearchRequest.AuditInfo.Organization", "Any Bank")
        mapObj.set("SearchRequest.AuditInfo.Phone", "5555551234")
        

        

        response = Search.create(mapObj)
        self.customAssertValue("1234", response.get("SearchResponse.Accounts.Account.AccountPanSuffix"))
        self.customAssertValue("1215", response.get("SearchResponse.Accounts.Account.ExpirationDate"))
        self.customAssertValue("DWSPMC00000000010906a349d9ca4eb1a4d53e3c90a11d9c", response.get("SearchResponse.Accounts.Account.Tokens.Token.TokenUniqueReference"))
        self.customAssertValue("FWSPMC0000000004793dac803f190a4dca4bad33c90a11d31", response.get("SearchResponse.Accounts.Account.Tokens.Token.PrimaryAccountNumberUniqueReference"))
        self.customAssertValue("7639", response.get("SearchResponse.Accounts.Account.Tokens.Token.TokenSuffix"))
        self.customAssertValue("0216", response.get("SearchResponse.Accounts.Account.Tokens.Token.ExpirationDate"))
        self.customAssertValue("2015-01-20T18:04:35-06:00", response.get("SearchResponse.Accounts.Account.Tokens.Token.DigitizationRequestDateTime"))
        self.customAssertValue("2015-01-20T18:04:35-06:00", response.get("SearchResponse.Accounts.Account.Tokens.Token.TokenActivatedDateTime"))
        self.customAssertValue("A", response.get("SearchResponse.Accounts.Account.Tokens.Token.FinalTokenizationDecision"))
        self.customAssertValue("101234", response.get("SearchResponse.Accounts.Account.Tokens.Token.CorrelationId"))
        self.customAssertValue("A", response.get("SearchResponse.Accounts.Account.Tokens.Token.CurrentStatusCode"))
        self.customAssertValue("Active", response.get("SearchResponse.Accounts.Account.Tokens.Token.CurrentStatusDescription"))
        self.customAssertValue("S", response.get("SearchResponse.Accounts.Account.Tokens.Token.ProvisioningStatusCode"))
        self.customAssertValue("Provisioning successful", response.get("SearchResponse.Accounts.Account.Tokens.Token.ProvisioningStatusDescription"))
        self.customAssertValue("00212345678", response.get("SearchResponse.Accounts.Account.Tokens.Token.TokenRequestorId"))
        self.customAssertValue("103", response.get("SearchResponse.Accounts.Account.Tokens.Token.WalletId"))
        self.customAssertValue("92de9357a535b2c21a3566e446f43c532a46b54c46", response.get("SearchResponse.Accounts.Account.Tokens.Token.PaymentAppInstanceId"))
        self.customAssertValue("S", response.get("SearchResponse.Accounts.Account.Tokens.Token.TokenType"))
        self.customAssertValue("2376", response.get("SearchResponse.Accounts.Account.Tokens.Token.LastCommentId"))
        self.customAssertValue("3e5edf24a24ba98e27d43e345b532a245e4723d7a9c4f624e93452c92de9357a535b2c21a3566e446f43c532d34s6", response.get("SearchResponse.Accounts.Account.Tokens.Token.Device.DeviceId"))
        self.customAssertValue("John Phone", response.get("SearchResponse.Accounts.Account.Tokens.Token.Device.DeviceName"))
        self.customAssertValue("09", response.get("SearchResponse.Accounts.Account.Tokens.Token.Device.DeviceType"))
        self.customAssertValue("92de9357a535b2c21a3566e446f43c532a46b54c46", response.get("SearchResponse.Accounts.Account.Tokens.Token.Device.SecureElementId"))
        

        BaseTest.putResponse("example_mdes_search_token_unique_ref", response);

    
    def test_example_mdes_search_account_pan(self):
        mapObj = RequestMap()
        mapObj.set("SearchRequest.AccountPan", "5412345678901234")
        mapObj.set("SearchRequest.ExcludeDeletedIndicator", "false")
        mapObj.set("SearchRequest.AuditInfo.UserId", "A1435477")
        mapObj.set("SearchRequest.AuditInfo.UserName", "John Smith")
        mapObj.set("SearchRequest.AuditInfo.Organization", "Any Bank")
        mapObj.set("SearchRequest.AuditInfo.Phone", "5555551234")
        

        

        response = Search.create(mapObj)
        

        BaseTest.putResponse("example_mdes_search_account_pan", response);

    
    def test_example_mdes_search_token(self):
        mapObj = RequestMap()
        mapObj.set("SearchRequest.Token", "5598765432109876")
        mapObj.set("SearchRequest.AuditInfo.UserId", "A14354773")
        mapObj.set("SearchRequest.AuditInfo.UserName", "John Smith")
        mapObj.set("SearchRequest.AuditInfo.Organization", "Any Bank")
        mapObj.set("SearchRequest.AuditInfo.Phone", "5551234658")
        

        

        response = Search.create(mapObj)
        

        BaseTest.putResponse("example_mdes_search_token", response);

    
    def test_example_mdes_search_comment_id(self):
        mapObj = RequestMap()
        mapObj.set("SearchRequest.CommentId", "123456")
        mapObj.set("SearchRequest.AuditInfo.UserId", "A1435477")
        mapObj.set("SearchRequest.AuditInfo.UserName", "John Smith")
        mapObj.set("SearchRequest.AuditInfo.Organization", "Any Bank")
        mapObj.set("SearchRequest.AuditInfo.PhoneNumber", "5555551234")
        

        

        response = Search.create(mapObj)
        

        BaseTest.putResponse("example_mdes_search_comment_id", response);

    
    def test_example_mdes_search_payment_app_id(self):
        mapObj = RequestMap()
        mapObj.set("SearchRequest.PaymentAppInstanceId", "645b532a245e4723d7a9c4f62b24f24a24ba98e27d43e34e")
        mapObj.set("SearchRequest.AuditInfo.UserId", "A14354773")
        mapObj.set("SearchRequest.AuditInfo.UserName", "John Smith")
        mapObj.set("SearchRequest.AuditInfo.Organization", "Any Bank")
        mapObj.set("SearchRequest.AuditInfo.Phone", "5551234658")
        

        

        response = Search.create(mapObj)
        

        BaseTest.putResponse("example_mdes_search_payment_app_id", response);

    
        
        
        
        
        
        
    

if __name__ == '__main__':
    unittest.main()

