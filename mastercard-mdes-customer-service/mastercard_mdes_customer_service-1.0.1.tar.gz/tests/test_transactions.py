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


class TransactionsTest(BaseTest):

    def setUp(self):
        keyFile = join(dirname(realpath(__file__)),"resources","mcapi_sandbox_key.p12")
        auth = OAuthAuthentication("L5BsiPgaF-O3qA36znUATgQXwJB6MRoMSdhjd7wt50c97279!50596e52466e3966546d434b7354584c4975693238513d3d",keyFile, "alias", "password")
        Config.setAuthentication(auth)
        Config.setDebug(True)

    
        
                
    def test_example_mdes_transactions(self):
        mapObj = RequestMap()
        mapObj.set("TransactionsRequest.TokenUniqueReference", "DWSPMC00000000010906a349d9ca4eb1a4d53e3c90a11d9c")
        mapObj.set("TransactionsRequest.AuditInfo.UserId", "A1435477")
        mapObj.set("TransactionsRequest.AuditInfo.UserName", "John Smith")
        mapObj.set("TransactionsRequest.AuditInfo.Organization", "Any Bank")
        mapObj.set("TransactionsRequest.AuditInfo.Phone", "5555551234")
        

        

        response = Transactions.create(mapObj)
        self.customAssertValue("USD", response.get("TransactionsResponse.Transactions.Transaction[0].CurrencyCode"))
        self.customAssertValue("123.45", response.get("TransactionsResponse.Transactions.Transaction[0].TransactionAmount"))
        self.customAssertValue("PURCH", response.get("TransactionsResponse.Transactions.Transaction[0].TransactionTypeCode"))
        self.customAssertValue("Purchase", response.get("TransactionsResponse.Transactions.Transaction[0].TransactionTypeDescription"))
        self.customAssertValue("AUTH", response.get("TransactionsResponse.Transactions.Transaction[0].TransactionStatusCode"))
        self.customAssertValue("FOODMART", response.get("TransactionsResponse.Transactions.Transaction[0].MerchantName"))
        self.customAssertValue("1234", response.get("TransactionsResponse.Transactions.Transaction[0].MerchantCategoryCode"))
        self.customAssertValue("GROCERY STORES, SUPERMARKETS", response.get("TransactionsResponse.Transactions.Transaction[0].MerchantCategoryDescription"))
        self.customAssertValue("90", response.get("TransactionsResponse.Transactions.Transaction[0].POSEntryMode"))
        self.customAssertValue("USD", response.get("TransactionsResponse.Transactions.Transaction[1].CurrencyCode"))
        self.customAssertValue("29.47", response.get("TransactionsResponse.Transactions.Transaction[1].TransactionAmount"))
        self.customAssertValue("PURCB", response.get("TransactionsResponse.Transactions.Transaction[1].TransactionTypeCode"))
        self.customAssertValue("Purchase with Cashback", response.get("TransactionsResponse.Transactions.Transaction[1].TransactionTypeDescription"))
        self.customAssertValue("COMP", response.get("TransactionsResponse.Transactions.Transaction[1].TransactionStatusCode"))
        self.customAssertValue("RXMART", response.get("TransactionsResponse.Transactions.Transaction[1].MerchantName"))
        self.customAssertValue("5678", response.get("TransactionsResponse.Transactions.Transaction[1].MerchantCategoryCode"))
        self.customAssertValue("DRUG STORES, PHARMACIES", response.get("TransactionsResponse.Transactions.Transaction[1].MerchantCategoryDescription"))
        self.customAssertValue("91", response.get("TransactionsResponse.Transactions.Transaction[1].POSEntryMode"))
        self.customAssertValue("USD", response.get("TransactionsResponse.Transactions.Transaction[2].CurrencyCode"))
        self.customAssertValue("-16.30", response.get("TransactionsResponse.Transactions.Transaction[2].TransactionAmount"))
        self.customAssertValue("REFND", response.get("TransactionsResponse.Transactions.Transaction[2].TransactionTypeCode"))
        self.customAssertValue("Refund", response.get("TransactionsResponse.Transactions.Transaction[2].TransactionTypeDescription"))
        self.customAssertValue("COMP", response.get("TransactionsResponse.Transactions.Transaction[2].TransactionStatusCode"))
        self.customAssertValue("AUTOMART", response.get("TransactionsResponse.Transactions.Transaction[2].MerchantName"))
        self.customAssertValue("9012", response.get("TransactionsResponse.Transactions.Transaction[2].MerchantCategoryCode"))
        self.customAssertValue("AUTOMOTIVE PARTS, ACCESSORIES STORES", response.get("TransactionsResponse.Transactions.Transaction[2].MerchantCategoryDescription"))
        self.customAssertValue("07", response.get("TransactionsResponse.Transactions.Transaction[2].POSEntryMode"))
        self.customAssertValue("USD", response.get("TransactionsResponse.Transactions.Transaction[3].CurrencyCode"))
        self.customAssertValue("41.89", response.get("TransactionsResponse.Transactions.Transaction[3].TransactionAmount"))
        self.customAssertValue("AFD", response.get("TransactionsResponse.Transactions.Transaction[3].TransactionTypeCode"))
        self.customAssertValue("Purchase Pre-Auth AFD", response.get("TransactionsResponse.Transactions.Transaction[3].TransactionTypeDescription"))
        self.customAssertValue("PAUTC", response.get("TransactionsResponse.Transactions.Transaction[3].TransactionStatusCode"))
        self.customAssertValue("GASMART", response.get("TransactionsResponse.Transactions.Transaction[3].MerchantName"))
        self.customAssertValue("3456", response.get("TransactionsResponse.Transactions.Transaction[3].MerchantCategoryCode"))
        self.customAssertValue("FUEL DISPENSER, AUTOMATED", response.get("TransactionsResponse.Transactions.Transaction[3].MerchantCategoryDescription"))
        self.customAssertValue("90", response.get("TransactionsResponse.Transactions.Transaction[3].POSEntryMode"))
        

        BaseTest.putResponse("example_mdes_transactions", response);

    
        
        
        
        
        
        
    

if __name__ == '__main__':
    unittest.main()

