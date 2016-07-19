__author__ = 'hyheng'
from bs4 import BeautifulSoup
# from bs4 import BeautifulSoup
from urllib2 import urlopen
import json
import requests
import re
import csv
from datetime import datetime
from time import gmtime, strftime
from pyparsing import Literal, quotedString, removeQuotes, delimitedList
import json


def ConvertUnixTime(unixtime):
    ds = datetime.fromtimestamp(unixtime)
    return ds

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
                ds = ConvertUnixTime(unixtime)
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
        chartURL = script['data-chart-img'].replace('render.png','render.json')

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





# GetPropertyInfo('19619228')

# GetZpidLisWithinZipcode('60687')

basepath = '/Users/hyheng/Dropbox/zillow-project/nyc msa/'

filein = '/Users/hyheng/Dropbox/zillow-project/nyc msa[property sample2].txt'
lines = [line.strip() for line in open(filein, 'r')]
index = 0
for i in range(index, len(lines)):
    parts = lines[i].split(',')
    print parts[0]
    try:
        for j in range(1, len(parts)):
            if len(parts[j]) > 1:
                GetPropertyInfo(parts[j])
    except Exception, e:
        print e


# filein = '/Users/hyheng/Dropbox/zillow-project/nyc msa.txt'
#
# lines = [line.strip() for line in open(filein, 'r')]
#
# filepath2 = '/Users/hyheng/Dropbox/zillow-project/nyc msa[property].txt'
#
# index = 0
#
# with open(filepath2, 'a') as fout:
#     for i in range(index, len(lines)):
#         zip = lines[i].split('\t')[0]
#         print zip
#         fout.write(zip+',')
#
#         try:
#             listofproperties = GetZpidLisWithinZipcode(zip)
#
#
#             for item in listofproperties:
#                 fout.write(str(item)+',')
#
#             fout.write('\n')
#
#         except Exception, e:
#             print e