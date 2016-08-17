from suds.client import Client
from suds.sax.element import Element

def z_query(username,password,wsdl_path,query):
    user = username
    pw = password
    url='file:\\\%s' % wsdl_path
    client = Client(url)
    headers = client.service.login(user,pw)
    ssnns = ('ns1','http://api.zuora.com/')
    ssn = Element('SessionHeader', ns=ssnns).append(Element('session',ns=ssnns).setText(headers['Session']))
    client.set_options(soapheaders=ssn) 
    output = client.service.query(query)
    
    return output
    
def z_query_more(username,password,wsdl_path,query_locator):
    user = username
    pw = password
    url='file:\\\%s' % wsdl_path
    client = Client(url)
    headers = client.service.login(user,pw)
    ssnns = ('ns1','http://api.zuora.com/')
    ssn = Element('SessionHeader', ns=ssnns).append(Element('session',ns=ssnns).setText(headers['Session']))
    client.set_options(soapheaders=ssn) 
    
    output = client.service.queryMore(query_locator)
    
    return output