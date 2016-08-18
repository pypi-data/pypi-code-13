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


class TokenStatusHistoryTest(BaseTest):

    def setUp(self):
        keyFile = join(dirname(realpath(__file__)),"resources","mcapi_sandbox_key.p12")
        auth = OAuthAuthentication("L5BsiPgaF-O3qA36znUATgQXwJB6MRoMSdhjd7wt50c97279!50596e52466e3966546d434b7354584c4975693238513d3d",keyFile, "alias", "password")
        Config.setAuthentication(auth)
        Config.setDebug(True)

    
        
                
    def test_example_mdes_token_status_history(self):
        mapObj = RequestMap()
        mapObj.set("TokenStatusHistoryRequest.TokenUniqueReference", "DWSPMC00000000010906a349d9ca4eb1a4d53e3c90a11d9c")
        mapObj.set("TokenStatusHistoryRequest.AuditInfo.UserId", "A1435477")
        mapObj.set("TokenStatusHistoryRequest.AuditInfo.UserName", "John Smith")
        mapObj.set("TokenStatusHistoryRequest.AuditInfo.Organization", "Any Bank")
        mapObj.set("TokenStatusHistoryRequest.AuditInfo.Phone", "5555551234")
        

        

        response = TokenStatusHistory.create(mapObj)
        self.customAssertValue("D", response.get("TokenStatusHistoryResponse.Statuses.Status[0].StatusCode"))
        self.customAssertValue("Deleted", response.get("TokenStatusHistoryResponse.Statuses.Status[0].StatusDescription"))
        self.customAssertValue("2014-12-16T13:04:35-06:00", response.get("TokenStatusHistoryResponse.Statuses.Status[0].StatusDateTime"))
        self.customAssertValue("C", response.get("TokenStatusHistoryResponse.Statuses.Status[0].Initiator"))
        self.customAssertValue("L", response.get("TokenStatusHistoryResponse.Statuses.Status[0].ReasonCode"))
        self.customAssertValue("A", response.get("TokenStatusHistoryResponse.Statuses.Status[1].StatusCode"))
        self.customAssertValue("Active", response.get("TokenStatusHistoryResponse.Statuses.Status[1].StatusDescription"))
        self.customAssertValue("2014-12-15T11:05:35-06:00", response.get("TokenStatusHistoryResponse.Statuses.Status[1].StatusDateTime"))
        self.customAssertValue("I", response.get("TokenStatusHistoryResponse.Statuses.Status[1].Initiator"))
        self.customAssertValue("A", response.get("TokenStatusHistoryResponse.Statuses.Status[1].ReasonCode"))
        self.customAssertValue("AI145530", response.get("TokenStatusHistoryResponse.Statuses.Status[1].AuditInfo.UserId"))
        self.customAssertValue("John Smith", response.get("TokenStatusHistoryResponse.Statuses.Status[1].AuditInfo.UserName"))
        self.customAssertValue("Any Bank", response.get("TokenStatusHistoryResponse.Statuses.Status[1].AuditInfo.Organization"))
        self.customAssertValue("6362205555", response.get("TokenStatusHistoryResponse.Statuses.Status[1].AuditInfo.Phone"))
        self.customAssertValue("S", response.get("TokenStatusHistoryResponse.Statuses.Status[2].StatusCode"))
        self.customAssertValue("Suspended", response.get("TokenStatusHistoryResponse.Statuses.Status[2].StatusDescription"))
        self.customAssertValue("2014-12-14T12:04:35-06:00", response.get("TokenStatusHistoryResponse.Statuses.Status[2].StatusDateTime"))
        self.customAssertValue("I", response.get("TokenStatusHistoryResponse.Statuses.Status[2].Initiator"))
        self.customAssertValue("L", response.get("TokenStatusHistoryResponse.Statuses.Status[2].ReasonCode"))
        self.customAssertValue("AI145530", response.get("TokenStatusHistoryResponse.Statuses.Status[2].AuditInfo.UserId"))
        self.customAssertValue("John Smith", response.get("TokenStatusHistoryResponse.Statuses.Status[2].AuditInfo.UserName"))
        self.customAssertValue("Any Bank", response.get("TokenStatusHistoryResponse.Statuses.Status[2].AuditInfo.Organization"))
        self.customAssertValue("6362205555", response.get("TokenStatusHistoryResponse.Statuses.Status[2].AuditInfo.Phone"))
        self.customAssertValue("A", response.get("TokenStatusHistoryResponse.Statuses.Status[3].StatusCode"))
        self.customAssertValue("Active", response.get("TokenStatusHistoryResponse.Statuses.Status[3].StatusDescription"))
        self.customAssertValue("2014-12-13T11:05:35-06:00", response.get("TokenStatusHistoryResponse.Statuses.Status[3].StatusDateTime"))
        self.customAssertValue("I", response.get("TokenStatusHistoryResponse.Statuses.Status[3].Initiator"))
        self.customAssertValue("A", response.get("TokenStatusHistoryResponse.Statuses.Status[3].ReasonCode"))
        self.customAssertValue("AI145530", response.get("TokenStatusHistoryResponse.Statuses.Status[3].AuditInfo.UserId"))
        self.customAssertValue("John Smith", response.get("TokenStatusHistoryResponse.Statuses.Status[3].AuditInfo.UserName"))
        self.customAssertValue("Any Bank", response.get("TokenStatusHistoryResponse.Statuses.Status[3].AuditInfo.Organization"))
        self.customAssertValue("6362205555", response.get("TokenStatusHistoryResponse.Statuses.Status[3].AuditInfo.Phone"))
        self.customAssertValue("U", response.get("TokenStatusHistoryResponse.Statuses.Status[4].StatusCode"))
        self.customAssertValue("Unmapped", response.get("TokenStatusHistoryResponse.Statuses.Status[4].StatusDescription"))
        self.customAssertValue("2014-12-12T10:04:35-06:00", response.get("TokenStatusHistoryResponse.Statuses.Status[4].StatusDateTime"))
        self.customAssertValue("Z", response.get("TokenStatusHistoryResponse.Statuses.Status[4].ReasonCode"))
        

        BaseTest.putResponse("example_mdes_token_status_history", response);

    
        
        
        
        
        
        
    

if __name__ == '__main__':
    unittest.main()

