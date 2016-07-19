import json

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from ..requests_util import RequestsUtil


class ZillowCrawler:

    def __init__(self):
        self._p_sleep = 0.999
        self._t_sleep = 10
        self._input_fp = ''
        self._output_fp = ''
        self._hspace = 1

        self.requests = RequestsUtil()

    def set_input(self, input, **params):
        pass

    def set_output(self, output, **params):
        pass

    def set_progress_bar(self, hspace=1):
        self._hspace = int(hspace)
        return self

    def crawl(self):
        pass


def GetBoundingbox(zipcode):
    #call bing map
    url = 'http://dev.virtualearth.net/REST/v1/Locations/' \
        + zipcode + '/?o=json&key=AgYfRZaVa5_OqtLHE3v3hcMRKk3AhqstGb2SWmU6uMI4XpONOxNlES1UkBwoCRPP'
    try:
        r = requests.request('GET', url)
        parsed_json = json.loads(r.text)
        sw_lat = parsed_json['resourceSets'][0]['resources'][0]['bbox'][0]
        sw_long = parsed_json['resourceSets'][0]['resources'][0]['bbox'][1]
        ne_lat = parsed_json['resourceSets'][0]['resources'][0]['bbox'][2]
        ne_long = parsed_json['resourceSets'][0]['resources'][0]['bbox'][3]

        return ne_lat,ne_long,sw_lat,sw_long
    except Exception, e:
        print e


def GetZpidLisWithinZipcode(zipcode):

    listofproperties = []

    ne_lat,ne_long,sw_lat,sw_long = GetBoundingbox(zipcode)

    parts = str(ne_long).split('.')
    str_ne_long = parts[0] + parts[1][0:6]
    parts = str(sw_long).split('.')
    str_sw_long = parts[0] + parts[1][0:6]

    str_ne_lat = str(ne_lat).replace('.','')[0:8]
    str_sw_lat = str(sw_lat).replace('.','')[0:8]

    boundingbox = str_sw_long+','+str_sw_lat+','+str_ne_long+','+str_ne_lat

    url = 'http://www.zillow.com/search/GetResults.htm?spt=homes&status=110011&lt=111101&ht=111111&pr=,&mp=,&bd=0%2C&ba=0%2C&sf=,&lot=,&yr=,&pho=0&pets=0&parking=0&laundry=0&pnd=0&red=0&zso=0&days=any&ds=all&pmf=1&pf=1&zoom=10&rect=' + boundingbox +'&p=1&sort=days&search=map&disp=1&rt=7&listright=true&isMapSearch=true&zoom=10' #map vs. maplist
    # print url
    # url = 'http://www.zillow.com/homes/' + zipcode + '_rb'

    try:
        r = requests.request('GET', url)
        parsed_json = json.loads(r.text)

        # totalResultCount = parsed_json['list']['binCounts']['totalResultCount']
        # forSaleCount = parsed_json['list']['binCounts']['forSaleCount']
        # makeMeMoveCount = parsed_json['list']['binCounts']['makeMeMoveCount']
        # recentlySoldCount = parsed_json['list']['binCounts']['recentlySoldCount']
        # forRentCount = parsed_json['list']['binCounts']['forRentCount']
        # fsbaCount = parsed_json['list']['binCounts']['fsbaCount']
        # fsboCount = parsed_json['list']['binCounts']['fsboCount']
        # foreclosuresCount = parsed_json['list']['binCounts']['foreclosuresCount']
        # bankOwnedCount = parsed_json['list']['binCounts']['bankOwnedCount']
        # foreclosedCount = parsed_json['list']['binCounts']['foreclosedCount']
        # preForeclosureCount = parsed_json['list']['binCounts']['preForeclosureCount']
        # newConstructionCount = parsed_json['list']['binCounts']['newConstructionCount']
        # openHousesCount = parsed_json['list']['binCounts']['openHousesCount']
        # singleFamilyCount = parsed_json['list']['binCounts']['singleFamilyCount']
        # condoCount = parsed_json['list']['binCounts']['condoCount']
        # multiFamilyCount = parsed_json['list']['binCounts']['multiFamilyCount']
        # manufacturedCount = parsed_json['list']['binCounts']['manufacturedCount']
        # landCount = parsed_json['list']['binCounts']['landCount']
        # unmappedCount = parsed_json['list']['binCounts']['unmappedCount']
        # comingSoonCount = parsed_json['list']['binCounts']['comingSoonCount']

        properties = parsed_json['map']['properties']
        for property in properties:
            zpid = property[0]
            listofproperties.append(zpid)

        # print listofproperties
        return listofproperties

    except Exception, e:
        print e


def GetChart(zid, chartURL, chartType):
    path = basepath + zid + '_' + chartType + '.txt'
    with open(path, 'a') as fout:
        r = requests.request('GET', chartURL)
        parsed_json = json.loads(r.text)

        for entries in parsed_json['paparazziData']:
            data = entries['data']
            name = entries['name']
            regionType = entries['regionType']

            dslist = []
            valuelist = []

            for datapoint in data:
                xvalue = datapoint['xValue'] #time
                unixtime = int(xvalue/1000)
                ds = datetime.utcfromtimestamp(unixtime)
                yvalue = datapoint['yValue'] #value

                dslist.append(ds.strftime('%Y/%m/%d'))
                valuelist.append(yvalue)

        #print
            fout.writelines('\n'+name + '\t' + regionType + '\n')
            for i in range(len(dslist)):
                fout.writelines(dslist[i] + '\t' + str(valuelist[i]) + '\n')


def GetPropertyInfo(zpid):
    url = 'http://www.zillow.com/homedetails/' + zpid + '_zpid/'
    r = requests.request('GET', url)
    html = r.text
    # print html
    html = html.encode('ascii', 'ignore')
    content = BeautifulSoup(html)
    scriptTags = content.findAll('a', attrs={'data-chart-img': True})

    for script in scriptTags:
        chartURL = script['data-chart-img'].replace('render.png', 'render.json')

        if 'm=1' in chartURL:
            GetChart(zpid, chartURL,'zestimate')
        elif 'm=3' in chartURL:
            GetChart(zpid, chartURL,'listing_price')
        elif 'm=9' in chartURL:
            GetChart(zpid, chartURL,'rent_zestimate')
        elif 'm=2' in chartURL:
            GetChart(zpid, chartURL,'zestimate_chage')
        elif 'm=5' in chartURL:
            GetChart(zpid, chartURL,'tax_assessment')
        elif 'm=6' in chartURL:
            GetChart(zpid, chartURL,'tax_paid')
        elif 'm=4' in chartURL:
            GetChart(zpid, chartURL,'page_view')

#2098319300
basepath = '/Volumes/cchen224/'
GetPropertyInfo('2098319300')