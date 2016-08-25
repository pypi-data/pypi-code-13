'''
Created on Aug 23, 2016
API to access Azure ML portal to 
predict the annual building energy consumption in kbtu
@author: t_songr
'''
import json
import urllib2
from gbXMLParser import gbXMLparser

class predictor:
    def __init__(self, endpoint_URL, access_key):
        self.url = endpoint_URL
        self.key = access_key
     
    def _predict(self, body, url, api_key):
        '''
        predict
        '''
        headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}
        
        req = urllib2.Request(url, body, headers) 
        
        try:
            response = urllib2.urlopen(req)
            result = response.read()
            results = json.loads(result)

            real_value = results["Results"]["output1"]["value"]["Values"][0][0]
            predicted_value = results["Results"]["output1"]["value"]["Values"][0][1]
            print "Simulated Annual Building Energy Consumption (kBTU):", real_value
            print "Predicted Annual Building Energy Consumption (kBTU):", round(float(predicted_value), 4)
            
        except urllib2.HTTPError, error:
            print("The request failed with status code: " + str(error.code))
        
            # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
            print(error.info())
        
            print(json.loads(error.read())) 

       
    def load_dataframe(self,df):
        '''
        load panda dataframe and submit to the model
        do prediction
        print out the results
        '''
        data_keys = df.index.values.tolist()
        data_values = map(str,df.values.tolist())

        data =  {
        
                "Inputs": {
                        "input1":
                        {
                            "ColumnNames": data_keys,
                            "Values": [ data_values ]
                        },        },
                    "GlobalParameters": {
        }
            }

        body = str.encode(json.dumps(data))
        
        self._predict(body, self.url, self.key)
        
    def load_gbXML(self,xml_path):
        '''
        load the gbXML file
        parse it here
        '''
        thisParser = gbXMLparser(xml_path, convert_climate=True)
        this_results = thisParser.results_dict
        this_results['Project ID'] = 0 # single parser doesn't have project ID, add a fake one
  
        data =  {
        
                "Inputs": {
                        "input1":
                        {
                            "ColumnNames": this_results.keys(),
                            "Values": [ this_results.values() ]
                        },        },
                    "GlobalParameters": {
        }
            }
    
        body = str.encode(json.dumps(data))
        self._predict(body, self.url, self.key)
    
if __name__ == '__main__':
    pass
    
        
        
