'''
Created on Jul 9, 2016

@author: tavis
'''

import urllib2, cStringIO
from BeautifulSoup import BeautifulSoup

def getLatestReading():
    """Fetches the latest Beijing US Embassy pollution reading into a duple of (AQI, reading time)"""
    url = "http://www.stateair.net/web/rss/1/1.xml"
    soup = BeautifulSoup(urllib2.urlopen(url).read())
    first_item = soup.find("item")
    aqi_reading = first_item.find("aqi").contents[0]
    reading_time = first_item.find("readingdatetime").contents[0]
    return ( aqi_reading , reading_time )



def fetchDataToArray():
    """
    Fetches pollution data from 2008-July 2016 into one long array of observations.
    
    Each observation is a dictionary of its values.  This function may need to be updated
    to reflect the filenames of current pollution datasets. Check the website at 
    http://www.stateair.net/web/historical/1/1.html for more information.
    """
    
    data_array= []
    
    data_urls = ["http://www.stateair.net/web/assets/historical/1/Beijing_2008_HourlyPM2.5_created20140325.csv",
                 "http://www.stateair.net/web/assets/historical/1/Beijing_2009_HourlyPM25_created20140709.csv",
                 "http://www.stateair.net/web/assets/historical/1/Beijing_2010_HourlyPM25_created20140709.csv",
                 "http://www.stateair.net/web/assets/historical/1/Beijing_2011_HourlyPM25_created20140709.csv",
                 "http://www.stateair.net/web/assets/historical/1/Beijing_2012_HourlyPM2.5_created20140325.csv",
                 "http://www.stateair.net/web/assets/historical/1/Beijing_2013_HourlyPM2.5_created20140325.csv",
                 "http://www.stateair.net/web/assets/historical/1/Beijing_2014_HourlyPM25_created20150203.csv",
                 "http://www.stateair.net/web/assets/historical/1/Beijing_2015_HourlyPM25_created20160201.csv",
                 "http://www.stateair.net/web/assets/historical/1/Beijing_2016_HourlyPM25_created20160707.csv"
                 ]
    
    for this_url in data_urls:
        pseudo_file = cStringIO.StringIO(urllib2.urlopen(this_url).read())

        #Three lines of file headers, followed by one line of column headers
        for i in range(1,5):
            pseudo_file.readline()

        next_line = pseudo_file.readline()
        while ( next_line ):
            this_line_split = next_line.split(",")
            date = str(this_line_split[3] + "-" + ("0" if (int(this_line_split[4]) < 10) else  "" ) + \
                       str(this_line_split[4])) + "-" + ("0" if (int(this_line_split[5]) < 10) else  "" ) + \
                       str(this_line_split[5])
            #Note -999 is missing, and we haven't recoded it here
            this_line_dictionary = {
                                    "site":         this_line_split[0],
                                    "parameter" :   this_line_split[1],
                                    "datetime" :        this_line_split[2],
                                    "year" :        this_line_split[3],
                                    "month" :       this_line_split[4],
                                    "day"   :       this_line_split[5],
                                    "hour" :        this_line_split[6],
                                    "value" :       this_line_split[7],
                                    "unit" :        this_line_split[8],
                                    "duration" :    this_line_split[9],
                                    "qc_name" :     this_line_split[10],
                                    "date" :        date 
                                        }
            data_array.append(this_line_dictionary)
            next_line = pseudo_file.readline()
            

    return data_array

def takeDailyAverage(data_array):
    """The raw US embassy pollution data are hourly; this takes a daily average of non-missing values and indexes it by SQL date"""
    input_dictionary = {}
    output_dictionary = {} 
    
    for this_element in data_array:
        this_date_array = input_dictionary.get(this_element["date"])
        if this_date_array is None:
            this_date_array = [ this_element]
        else:
            this_date_array.append(this_element)
        input_dictionary[this_element["date"]] = this_date_array

    for this_date in input_dictionary:
        total = 0.0
        obs = 0.0
        for this_hour in input_dictionary[this_date]:
            this_obs = float(this_hour["value"])
            if ( this_obs is not None and this_obs > 0):
                total += this_obs 
                obs += 1.0
            if ( obs > 0 ):
                daily_average = total/obs
                output_dictionary[this_date] = daily_average

    return output_dictionary

def fetchDailyAverage():
    """This routine just fetches the hourly pollution data array and fetches the indexed daily average in one step."""
    full_array = fetchDataToArray()
    daily_average = takeDailyAverage(full_array)
    return daily_average

if __name__ == '__main__':
    
    latest_reading = getLatestReading()
    print(latest_reading[0] + ", " + latest_reading[1])
    
    