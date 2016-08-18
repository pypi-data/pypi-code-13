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
from mastercardlocations import *


class MerchantCategoriesTest(BaseTest):

    def setUp(self):
        keyFile = join(dirname(realpath(__file__)),"resources","mcapi_sandbox_key.p12")
        auth = OAuthAuthentication("L5BsiPgaF-O3qA36znUATgQXwJB6MRoMSdhjd7wt50c97279!50596e52466e3966546d434b7354584c4975693238513d3d",keyFile, "alias", "password")
        Config.setAuthentication(auth)
        Config.setDebug(True)

    
        
        
        
        
        
        
                
    def test_example_merchants_category(self):
        mapObj = RequestMap()
        

        

        response = MerchantCategories.query(mapObj)
        self.customAssertValue("1Apparel", response.get("Categories.Category[0]"))
        self.customAssertValue("2Automotive", response.get("Categories.Category[1]"))
        self.customAssertValue("3Beauty", response.get("Categories.Category[2]"))
        self.customAssertValue("4Book Stores", response.get("Categories.Category[3]"))
        self.customAssertValue("5Convenience Stores", response.get("Categories.Category[4]"))
        self.customAssertValue("7Dry Cleaners And Laundry Services", response.get("Categories.Category[5]"))
        self.customAssertValue("8Fast Food Restaurants", response.get("Categories.Category[6]"))
        self.customAssertValue("9Gift Shops, Hobbies, Jewelers", response.get("Categories.Category[7]"))
        self.customAssertValue("10Grocery Stores And Supermarkets", response.get("Categories.Category[8]"))
        self.customAssertValue("11Health", response.get("Categories.Category[9]"))
        

        BaseTest.putResponse("example_merchants_category", response);

    
        
    

if __name__ == '__main__':
    unittest.main()

