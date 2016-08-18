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


class TokenCommentsTest(BaseTest):

    def setUp(self):
        keyFile = join(dirname(realpath(__file__)),"resources","mcapi_sandbox_key.p12")
        auth = OAuthAuthentication("L5BsiPgaF-O3qA36znUATgQXwJB6MRoMSdhjd7wt50c97279!50596e52466e3966546d434b7354584c4975693238513d3d",keyFile, "alias", "password")
        Config.setAuthentication(auth)
        Config.setDebug(True)

    
        
                
    def test_example_mdes_token_comments(self):
        mapObj = RequestMap()
        mapObj.set("TokenCommentsRequest.TokenUniqueReference", "DWSPMC00000000010906a349d9ca4eb1a4d53e3c90a11d9c")
        mapObj.set("TokenCommentsRequest.AuditInfo.UserId", "A1435477")
        mapObj.set("TokenCommentsRequest.AuditInfo.UserName", "John Smith")
        mapObj.set("TokenCommentsRequest.AuditInfo.Organization", "Any Bank")
        mapObj.set("TokenCommentsRequest.AuditInfo.Phone", "5555551234")
        

        

        response = TokenComments.create(mapObj)
        self.customAssertValue("1648", response.get("TokenCommentsResponse.Comments.Comment[0].CommentId"))
        self.customAssertValue("Cardholder lost phone. Suspending device.", response.get("TokenCommentsResponse.Comments.Comment[0].CommentText"))
        self.customAssertValue("2015-01-21T18:04:35-06:00", response.get("TokenCommentsResponse.Comments.Comment[0].CommentDateTime"))
        self.customAssertValue("A14354774", response.get("TokenCommentsResponse.Comments.Comment[0].AuditInfo.UserId"))
        self.customAssertValue("Jade Mark", response.get("TokenCommentsResponse.Comments.Comment[0].AuditInfo.UserName"))
        self.customAssertValue("Any Bank", response.get("TokenCommentsResponse.Comments.Comment[0].AuditInfo.Organization"))
        self.customAssertValue("5555558888", response.get("TokenCommentsResponse.Comments.Comment[0].AuditInfo.Phone"))
        self.customAssertValue("1647", response.get("TokenCommentsResponse.Comments.Comment[1].CommentId"))
        self.customAssertValue("Cardholder called to activate their digital card.", response.get("TokenCommentsResponse.Comments.Comment[1].CommentText"))
        self.customAssertValue("2015-01-19T11:02:25-06:00", response.get("TokenCommentsResponse.Comments.Comment[1].CommentDateTime"))
        self.customAssertValue("A14354773", response.get("TokenCommentsResponse.Comments.Comment[1].AuditInfo.UserId"))
        self.customAssertValue("Tom Smith", response.get("TokenCommentsResponse.Comments.Comment[1].AuditInfo.UserName"))
        self.customAssertValue("Any Bank", response.get("TokenCommentsResponse.Comments.Comment[1].AuditInfo.Organization"))
        self.customAssertValue("5555559999", response.get("TokenCommentsResponse.Comments.Comment[1].AuditInfo.Phone"))
        

        BaseTest.putResponse("example_mdes_token_comments", response);

    
        
        
        
        
        
        
    

if __name__ == '__main__':
    unittest.main()

