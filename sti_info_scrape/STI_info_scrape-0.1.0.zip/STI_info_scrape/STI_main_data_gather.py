"""    
    STI data collect from SGX.
    Daily collection of main data. (Index, volumen and gain/loss ratio)

    Requires:
        pattern, pandas and selenium (Chrome)
        
    May need to add the index



    Updates:
        Jul 24 2016: Enable saving to raw data.
                     Change to get_SGX_main_data instead of SGX_main_data (property)
        Jul 23 2016: resolve bug in retrieve_page_source, chromedriver not defined.




"""

import os, re, time, sys
from pattern.web import DOM, URL, plaintext
import pandas as pd
from selenium import webdriver

class STIMainData(object):
    """ Class that retreive main results from sgx.oom

    """
    SGX_main_website = 'http://sgx.com' 

    @property
    def chromedriver_location(self):
        """ Path of the chromedriver_location."""
        return self._cd_path
    
    @chromedriver_location.setter
    def chromedriver_location(self, path):
        """ Set the chromedriver_location.
            Args:
                path: path of chromedriver location.
        """
        if not path:
            print "please enter valid path."
            print "Please download from https://sites.google.com/a/chromium.org/chromedriver/downloads"
            raise
        self._cd_path = path

    @property
    def store_location(self):
        """ Saved file of all the raw data."""
        return self._storelocation

    @store_location.setter
    def store_location(self, path):
        """ Specifiy the stored location of data.
            Args:
                path: path of save data location.
        """
        self._storelocation = path
                
    def retrieve_page_source(self, url):
        """ Retrieve main page source from target url using selenium chrome.`
            Args:
                url (str): url str of target
            Returns:
                (str): html page source.

        """
        source = ''

        try:    
            os.environ["webdriver.chrome.driver"] = self.chromedriver_location
            driver = webdriver.Chrome(self.chromedriver_location)
            driver.get(url)
            source = driver.page_source
            driver.quit()
        except:
            print 'Error'
            raise

        return source

    def get_SGX_main_data(self):
        
        """ Retrieve main informaton from SGX main website.
            Would need to get the date as well

        """
        html_source =  self.retrieve_page_source(self.SGX_main_website)
        self.source = html_source #for debug purpose
        self.STI_data_df = self.get_data_fr_htmlsrc(html_source)
        return self.STI_data_df

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

    def save_to_file(self ,mode = 'a', header=False):
        """ Save data to file.
            If file not exist, create the file.
            Kwargs:
                mode : 'a' or 'w' mode
                header (bool): default False when append
        """
        if not os.path.isfile(self.store_location):
            mode = 'w' #force to write if file do not exisit
            header = True
                    
        self.STI_data_df.to_csv(self.store_location, index =False, mode = mode, header=header)

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
    w.chromedriver_location = r"D:\download (software)\chromedriver.exe"
    w.store_location = r'C:\data\temp\STImaindata.csv'
    kk = w.get_SGX_main_data()
    print kk.head()
    w.save_to_file()

    sys.exit()











