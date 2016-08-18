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
from mastercardassuranceiq import *


class ECommerceMessageTest(BaseTest):

    def setUp(self):
        keyFile = join(dirname(realpath(__file__)),"resources","mcapi_sandbox_key.p12")
        auth = OAuthAuthentication("L5BsiPgaF-O3qA36znUATgQXwJB6MRoMSdhjd7wt50c97279!50596e52466e3966546d434b7354584c4975693238513d3d",keyFile, "alias", "password")
        Config.setAuthentication(auth)
        Config.setDebug(True)

    
        
        
                
    def test_example_notify_event(self):
        mapObj = RequestMap()
        mapObj.set("ECommerceMessage.ServiceRequest.EventType", "Purchase")
        mapObj.set("ECommerceMessage.ServiceRequest.SenderMsgRef", "123356af")
        mapObj.set("ECommerceMessage.ServiceRequest.ServiceMethod", "Notification")
        mapObj.set("ECommerceMessage.ServiceRequest.NotificationOutcome", "Success")
        mapObj.set("ECommerceMessage.ServiceRequest.UserAccountId", "siHZ27CDp/M0KNfCo8MZiuklYU1wIQ4ocWzKp81N23k=")
        mapObj.set("ECommerceMessage.ServiceRequest.AppMsgType", "AppMsgType")
        mapObj.set("ECommerceMessage.ServiceRequest.PAN", "1234567890123456789")
        mapObj.set("ECommerceMessage.ServiceRequest.ExpirationDate", "1015")
        mapObj.set("ECommerceMessage.ServiceRequest.TransactionDateTime", "2012-01-02 23:59:59.123")
        mapObj.set("ECommerceMessage.ServiceRequest.IPAddress", "siHZ27CDp/M0KNfCo8MZiuklYU1wIQ4ocWzKp81N23k=")
        mapObj.set("ECommerceMessage.ServiceRequest.Email", "siHZ27CDp/M0KNfCo8MZiuklYU1wIQ4ocWzKp81N23k=")
        mapObj.set("ECommerceMessage.ServiceRequest.Telephone1", "siHZ27CDp/M0KNfCo8MZiuklYU1wIQ4ocWzKp81N23k=")
        mapObj.set("ECommerceMessage.ServiceRequest.Telephone2", "siHZ27CDp/M0KNfCo8MZiuklYU1wIQ4ocWzKp81N23k=")
        mapObj.set("ECommerceMessage.ServiceRequest.Telephone3", "siHZ27CDp/M0KNfCo8MZiuklYU1wIQ4ocWzKp81N23k=")
        mapObj.set("ECommerceMessage.ServiceRequest.ShippingAddress1", "siHZ27CDp/M0KNfCo8MZiuklYU1wIQ4ocWzKp81N23k=")
        mapObj.set("ECommerceMessage.ServiceRequest.ShippingAddress2", "ShippingAddress2")
        mapObj.set("ECommerceMessage.ServiceRequest.ShippingAddress3", "ShippingAddress3")
        mapObj.set("ECommerceMessage.ServiceRequest.ShippingCity", "ShippingCity")
        mapObj.set("ECommerceMessage.ServiceRequest.ShippingState", "ShippingState")
        mapObj.set("ECommerceMessage.ServiceRequest.ShippingCountry", "ShippingCountry")
        mapObj.set("ECommerceMessage.ServiceRequest.ShippingPostalCode", "siHZ27CDp/M0KNfCo8MZiuklYU1wIQ4ocWzKp81N23k=")
        mapObj.set("ECommerceMessage.ServiceRequest.BillingAddress1", "siHZ27CDp/M0KNfCo8MZiuklYU1wIQ4ocWzKp81N23k=")
        mapObj.set("ECommerceMessage.ServiceRequest.BillingAddress2", "BillingAddress2")
        mapObj.set("ECommerceMessage.ServiceRequest.BillingAddress3", "BillingAddress3")
        mapObj.set("ECommerceMessage.ServiceRequest.BillingCity", "BillingCity")
        mapObj.set("ECommerceMessage.ServiceRequest.BillingState", "BillingState")
        mapObj.set("ECommerceMessage.ServiceRequest.BillingCountry", "BillingCountry")
        mapObj.set("ECommerceMessage.ServiceRequest.BillingPostalCode", "siHZ27CDp/M0KNfCo8MZiuklYU1wIQ4ocWzKp81N23k=")
        mapObj.set("ECommerceMessage.ServiceRequest.DeviceCollection", "status_success")
        mapObj.set("ECommerceMessage.ServiceRequest.HttpHeaders", "{'content-type': 'application/x-www-form-urlencoded', 'connection': 'keep-alive','content-length': '1618','accept-encoding': 'gzip,deflate,sdch'}")
        mapObj.set("ECommerceMessage.ServiceRequest.TelephoneCountryCode", "1")
        mapObj.set("ECommerceMessage.ServiceRequest.TelephoneAreaCode", "555")
        mapObj.set("ECommerceMessage.ServiceRequest.IPPrefix", "10.100")
        mapObj.set("ECommerceMessage.ServiceRequest.PostalCodePrefix", "620")
        mapObj.set("ECommerceMessage.ServiceRequest.SenderConfidence", "ZiuklYU1wIQ4oc")
        mapObj.set("ECommerceMessage.ServiceRequest.LoginAuthenticationMethod", "0101")
        mapObj.set("ECommerceMessage.ServiceRequest.CardVerificationStatus", "23")
        mapObj.set("ECommerceMessage.ServiceRequest.WalletDistributorIsIssuer", "Y")
        mapObj.set("ECommerceMessage.ServiceRequest.TxnAmount", "15000")
        mapObj.set("ECommerceMessage.ServiceRequest.TxnCurrCode", "123")
        mapObj.set("ECommerceMessage.ServiceRequest.MerchantName", "MerchantName")
        mapObj.set("ECommerceMessage.ServiceRequest.AcquirerId", "123545")
        mapObj.set("ECommerceMessage.ServiceRequest.MerchantId", "123456555")
        mapObj.set("ECommerceMessage.ServiceRequest.MCC", "1234")
        

        

        request = ECommerceMessage(mapObj)
        response = request.update()
        self.customAssertValue("123356af", response.get("EventNotificationResponse.ServiceRequest.SenderMsgRef"))
        self.customAssertValue("Success", response.get("EventNotificationResponse.ServiceResponse.Status"))
        

        BaseTest.putResponse("example_notify_event", response);

    
        
        
        
        
        
    

if __name__ == '__main__':
    unittest.main()

