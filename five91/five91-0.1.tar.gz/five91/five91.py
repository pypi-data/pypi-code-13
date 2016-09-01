from bs4 import BeautifulSoup
from urllib.parse import urlencode
from urllib.parse import urljoin
from urllib.request import urlopen
import json
import re


def to_int(str):
    return int(re.sub('[^0-9]', '', str))


def to_float(str):
    return float(re.sub('[^0-9\.]', '', str))


class Rent591():

    def __init__(self):
        self.request_url = 'https://rent.591.com.tw/index.php'
        pass

    def search(self, region=1, kind=None, section=None, rentprice=0, pattern=None, first_row=0, total_rows=None):
        values = {'module': 'search',
                  'action': 'rslist',
                  'is_new_list': 1,
                  'type': 1,
                  'searchtype': 1,
                  'region': region,
                  'listview': 'txt',
                  'rentprice': rentprice,
                  'firstRow': first_row}
        if kind is not None:
            values['kind'] = ','.join(kind)
        if section is not None:
            values['secion'] = ','.join(section)
        if pattern is not None:
            values['pattern'] = pattern
        if total_rows is not None:
            values['totalRows'] = total_rows
        data = urlencode(values)
        full_url = self.request_url + '?' + data
        with urlopen(full_url) as response:
            # structure of response_result:
            # {
            #   "region": same as the search parameter
            #   "count": total count
            #   "recom": recommended objects
            #   "main": html of search results
            #   "page": html of pagination
            #   "left": html of left-side-filter-box
            #   "broker":
            #   "community":
            # }
            response_result = json.loads(response.read().decode('utf-8'))
            return self.__translate_result(response_result)

    def __translate_common_object(self, item):
        """
        Translate a html structure of common object to a rent info.

        <ul class="shTxInfo">
            <li class="rs"><strong><a class="txt-sh-region" href="javascript:;" data-bind="1">台北市</a>-<strong><a class="txt-sh-section" href="javascript:;" data-bind="12">文山區</a></strong></strong></li>
            <li class="address"><a href="rent-detail-xxxxxxx.html" target="_blank" title="某某路四段某某華廈!!吉祥入住!!來電成交!!">某某路四段某某華廈!!吉祥入住..</a>&nbsp;<span class="ImgStatus" title="內有房屋照片">附圖</span>&nbsp;&nbsp;(1)</li>
            <li class="area">32坪/整層</li>
            <li class="price"><strong class="fc-org">12,800元</strong></li>
            <li class="visited">543</li>
            <li class="update"><strong class="fc-red"><strong class="TodayTime">今日</strong></strong></li>
        </ul>
        """
        tag_a_section = item.find_all('a', {'class': 'txt-sh-section'})[0]
        section_txt = tag_a_section.get_text()
        tag_li_address = item.find_all('li', {'class': 'address'})[0]
        address = tag_li_address.find_all('a')[0]
        title = address.get('title')
        url = urljoin(self.request_url, address.get('href'))
        tag_li_area = item.find_all('li', {'class': 'area'})[0]
        area_txt, kind_txt = tag_li_area.get_text().split('/')
        area = to_float(area_txt)
        tag_li_price = item.find_all('li', {'class': 'price'})[0]
        price = to_int(tag_li_price.get_text())
        # <li class='visited'>
        # <li class='update'>
        return {'title': title,
                'url': url,
                'area': area,
                'section': section_txt,
                'kind': kind_txt,
                'price': price}

    def __translate_recommended_object(self, item):
        """
        Translate a html structure of recommended object to a rent info.

        <div class="content">
            <p><a href="rent-detail-xxxxxxx.html" target="_blank" title="天母某某居(飯店式管理)" google-data-stat="出售_精選推薦_精選推薦列表"><img src="https://cp2.591.c...x127.jpg" width="172" height="127" alt="天母某某居(飯店式管理)" /></a></p>
            <p class="name"><a href="rent-detail-xxxxxxx.html" target="_blank" title="天母某某居(飯店式管理)" google-data-stat="出售_精選推薦_精選推薦列表"><strong>天母某某居(飯店式管理...</strong></a></p>
            <p>士林區 - 整層住家<em class="area">12.34坪</em></p>
            <p class="fc-org"><strong>80,000元</strong></p>
        </div>
        """
        ps = item.find_all('p')
        title = ps[0].a.get('title')
        url = urljoin(self.request_url, ps[0].a.get('href'))
        section_txt, kind_txt = ps[2].find(
            text=True, recursive=False).split(' - ')
        area_txt = ps[2].em.get_text()
        area = to_float(area_txt)
        price = to_int(ps[3].get_text())
        return {'title': title,
                'url': url,
                'area': area,
                'section': section_txt,
                'kind': kind_txt,
                'price': price}

    def __translate_result(self, origin_result):
        result = {}
        result['region'] = to_int(origin_result['region'])
        result['count'] = to_int(origin_result['count'])

        result['main'] = []
        soup = BeautifulSoup(origin_result['main'], 'html.parser')
        for tag_ul in soup.find_all('ul'):
            common_object = self.__translate_common_object(tag_ul)
            result['main'].append(common_object)
        soup.decompose()

        result['recom'] = []
        soup = BeautifulSoup(origin_result['recom'], 'html.parser')
        for tag_div in soup.find_all('div', {'class': 'content'}):
            recom_object = self.__translate_recommended_object(tag_div)
            result['recom'].append(recom_object)
        soup.decompose()

        return result


class Sale591():
    pass
