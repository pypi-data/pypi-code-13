"""    
    STI data collect from SGX.
    Daily collection of main data. (Index, volumen and gain/loss ratio)

    Requires:
        pattern, pandas and selenium (Chrome)
        
    Need a project name
    STI_info_scrape


"""

import os, re, time, sys
from pattern.web import DOM, URL, plaintext
import pandas as pd
from selenium import webdriver

class STIMainData(object):
    """ Class that retreive main results from sgx.oom

    """
    chromedriver_location = r"D:\download (software)\chromedriver.exe"
    SGX_main_website = 'http://sgx.com' 

    def retrieve_page_source(self, url):
        """ Retrieve main page source from target url using selenium chrome.`
            Args:
                url (str): url str of target
            Returns:
                (str): html page source.

        """
        try:    
            os.environ["webdriver.chrome.driver"] = self.chromedriver_location
            driver = webdriver.Chrome(chromedriver)
            driver.get(url)
            source = driver.page_source
            driver.quit()
        except:
            print 'Error'

        return source

    @property
    def SGX_main_data(self):
        
        """ Retrieve main informaton from SGX main website.
            Would need to get the date as well

        """
        html_source =  self.retrieve_page_source(self.SGX_main_website)
        self.source = html_source #for debug purpose
        return self.get_data_fr_htmlsrc(html_source)

    def get_data_fr_htmlsrc(self, page_source):
        """ Retrieve the raw data based on DOM object.
            Include both raw data and the date
            Args:
                page_source (str): html str.
            Returns:
                (dataframe): 

        """
        dom_object = DOM(page_source)
        # get date
        date_data = self.get_date_fr_src(dom_object)
        
        data_df = pd.read_html(dom_object('div#tots')[0].content, index_col =0)[0]
        data_df = self.modify_sgx_main_data_df(data_df)

        data_df['Date'] = date_data
        data_df['Date'] = pd.to_datetime(data_df['Date'])

        return data_df

    @staticmethod
    def get_date_fr_src(dom_object):
        """ Retrieved the date from small print in SGX main page.

        """
        date_str = plaintext(dom_object('div.sgx_portlet_timestamp_label')[0].content)
        return re.search('As at (.*)\s\d', date_str).group(1)

    @staticmethod
    def modify_sgx_main_data_df(data_df):
        """ Modify the data df to a format that is suitable
            Args:
                data_df (Dataframe obj): raw input of target data
            Returns:
                (Dataframe): modified data_df

        """
        data_df.index = data_df.index.str.replace(':','')
        data_df  = data_df.T
        data_df['Volume'] = data_df['Volume'].str.replace('M', '')
        data_df['Volume'] = data_df['Volume'].str.replace(',', '')
        for n in ', M $'.split(' '):
            data_df['Value'] = data_df['Value'].str.replace(n, '')

        data_df['Volume'] = data_df['Volume'].astype(float)
        data_df['Value'] = data_df['Value'].astype(float)

        data_df['Gainers'] = data_df['Gainers/Losers'].str.extract('(.*)/').astype(int)
        data_df['Losers'] = data_df['Gainers/Losers'].str.extract('/(.*)').astype(int)
        data_df['Gain_Loss_ratio'] = data_df['Gainers']/data_df['Losers']

        return data_df
        
if __name__ == "__main__":
    print "testing function"

    w = STIMainData()
    kk = w.SGX_main_data
    print kk.head()

    sys.exit()











