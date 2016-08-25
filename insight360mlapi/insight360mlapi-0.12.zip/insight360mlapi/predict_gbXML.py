from insight360ml_api.building_energy_api import predictor
import getopt, sys



if __name__ == '__main__':
    
    endpoint_url = "https://ussouthcentral.services.azureml.net/workspaces/e09cad2151c94dc895673dcdbf35efb8/services/cfefc92d4e60486c8c9794af4d4e0761/execute?api-version=2.0&details=true"
    api_key = "ddWkdaJk7wVuPSR6+TuFaUgtrTMruiSFxKHzh7fbC3K+R1oGU6qxX+BzbkJ2PNlfvWVcE3JQ/eiaLuiNFQ874Q=="
    opts, args = getopt.getopt(sys.argv[1:], "n")  
    xml_path = args[0]

    thisPredictor = predictor(endpoint_url, api_key)
    thisPredictor.load_gbXML(xml_path)
    
    raw_input()