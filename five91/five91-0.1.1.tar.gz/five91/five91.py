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

    def search(self, region=1, section=None, kind=None, shType=None,
               listview='txt', rentprice=None, pattern=None, area=None, shape=None,
               role=None, min_floor=None, max_floor=None, sex=None, other=None, option=None, keywords=None,
               order=None, orderType=None, first_row=None, total_rows=None):
        """ Search by region and section.

        (under construction)

        Args:
            region: A number, the number represented region is list in
                <Region value-txt table>.
            section: Optional variable, number, the number represented section
                is list in <Section value-txt table>; a number list is also 
                valid, and only first five element is applied.
            kind: Optional variable, number, the number represented kind is list
                in <Kind value-txt table>.
            shType: Optional variable, string, should be 'hurryRent' or 'host'
            listview: string, should be 'txt' or 'img'. 'img' is more info but
                slow.
            rentprice: Optional variable, could be a number or a list/tuple of
                two numbers. If it's only a number, the price is defined in
                <rentprice value-txt table>; if it's a list, the list means the
                range of price.
            pattern: Optional variable, number, the number represented pattern
                is list in <Pattern value-txt table>.
            area: Optional variable, could be a number or a list/tuple of two
                numbers. If it's only a number, the area is defined in
                <area value-txt table>; if it's a list, the list means the range
                of area.
            shape: Optional variable, number or a list of number. The meaning of
                number is defined in <Shape value-txt table>.
            role: Optional variable, number or a list of number. The meaning of
                number is defined in <Role value-txt table>.
            floor: Optional variable, should be a list/tuple of two elements,
                each element could be number or `None`.
            sex: Optional variable, number, `1` for male and `2` for female.
            other: Optional variable, should be a list containing other-value
                string. Available other-value strings is list in
                <Other value-txt table>.
            option: Optional variable, should be a list containing option-value
                string. Available option-value strings is list in
                <Option value-txt table>.
            keywords: Arbitrary string as search keyword.
            order: Optional variable, string, which data to order by, may be one
                of ['area', 'money', 'visitor', 'posttime', 'nearby'].
            orderType: Optional variable, 'asc' or 'desc'.

        Returns:
        """
        # searchtype: {1: 'rgsc', 2: 'busness', 3: 'school', 4: 'mrg'}
        #                             ^^^^^^^ no typo
        values = {'module': 'search',
                  'action': 'rslist',
                  'is_new_list': 1,
                  'type': 1,
                  'searchtype': 1,
                  'listview': listview,
                  'region': region}
        # section
        if section is not None:
            if type(section) is list or type(section) is tuple:
                values['section'] = ','.join([str(x) for x in section[:5]])
            else:
                values['section'] = section
        # kind
        if kind is not None:
            if type(kind) is list or type(kind) is tuple:
                values['kind'] = ','.join(kind)
            else:
                values['kind'] = kind
        # shType
        if shType is not None and shType in ['hurryRent', 'host']:
            values['shType'] = shType
        # rentprice
        if rentprice is not None:
            if type(rentprice) is list or type(rentprice) is tuple:
                values['rentprice'] = ','.join(rentprice[:2])
            else:
                values['rentprice'] = rentprice
        # pattern
        if pattern is not None:
            values['pattern'] = pattern
        # area
        if area is not None:
            if type(area) is list or type(area) is tuple:
                values['area'] = ','.join(area[:2])
            else:
                values['area'] = area
        # shape
        if shape is not None:
            if type(shape) is list or type(shape) is tuple:
                values['shape'] = ','.join(shape)
            else:
                values['shape'] = shape
        # role
        if role is not None:
            if type(role) is list or type(role) is tuple:
                values['role'] = ','.join(role)
            else:
                values['role'] = role
        # floor
        if min_floor is not None or max_floor is not None:
            floor = []
            floor.append('' if min_floor is None else min_floor)
            fllor.append('' if max_floor is None else max_floor)
            values['floor'] = ','.join(floor)
        # sex
        if sex is not None and sex in [1, 2]:
            values['sex'] = sex
        # other
        if other is not None:
            if type(other) is list or type(other) is tuple:
                values['other'] = ','.join(other)
            else:
                values['other'] = other
        # option
        if option is not None:
            if type(option) is list or type(option) is tuple:
                values['option'] = ','.join(option)
            else:
                values['option'] = option
        # keywords
        if keywords is not None:
            if type(keywords) is list or type(keywords) is tuple:
                values['keywords'] = ','.join(keywords)
            else:
                values['keywords'] = keywords
        # order, orderType
        if order is not None and order in ['area', 'money', 'visitor', 'posttime', 'nearby']:
            values['order'] = order
            values['orderType'] = 'asc'
            if orderType is not None and orderType in ['asc', 'desc'] and order is not 'nearby':
                values['orderType'] = orderType
        # first_row
        if first_row is not None:
            values['firstRow'] = first_row
        # total_rows
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

    def __translate_img_object(self, item):
        """Translate a html structure of common object in img view to a rent info.
        """
        # <ul class="shInfo"   >
        #     <li class="info">
        #         <div class="left" data-bind="xxxxxxx" data-img-length="14">
        #             <a href="rent-detail-xxxxxxx.html" class="imgbd" target="_blank" title="專屬露臺可看101"   ><img src="https://cp1.591.com.tw/house/active/2016/05/10/146288090393453000_128x92.jpg" width="128" height="92" alt="專屬露臺可看101" /></a>
        #             <div class="imgMore"><a href="rent-detail-xxxxxxx.html" target="_blank">14張照片</a></div>
        #         </div>
        #         <div class="right">
        #             <p class="title"><a href="rent-detail-xxxxxxx.html" target="_blank" class="house_url" title="專屬露臺可看101"><strong>專屬露臺可看101</strong></a><em class="recomTag">黃金曝光</em></p>
        #             <p>敦南雅緻　台北市-信義區 和平東路三段xxx巷x弄xx-x號</p>
        #             <p>整層住家，<span class="layout">1房1廳1衛</span>，</span>樓層：5/6</p>
        #             <p class="fc-gry">59分鐘內更新  屋主 x小姐    </p>
        #             <p class="options opacity"><a href="javascript:;" class="map" data-bind="xxxxxxx"  onclick="ga('send', 'event','列表頁','物件列表','地圖',1);">地圖</a>
        #                                        <a href="javascript:;" class="fav" data-bind="xxxxxxx"  onclick="ga('send', 'event','列表頁','物件列表','收藏',1);">收藏</a>
        #                                        <a href="rent-detail-xxxxxxx.html#faq" class="qs"  onclick="ga('send', 'event','列表頁','物件列表','問答',1);">問答(1)</a></p>
        #         </div>
        #     </li>
        #     <li class="area rentByArea">
        #         18坪
        #     </li>
        #     <li class="price fc-org">
        #         <p><span class="oldprice"><strong></strong></span></p>
        #         <strong class="">28,000元</strong>
        #         <p></p>
        #     </li>
        #     <li class="pattern">165人</li>
        # </ul>

        pass

    def __translate_common_object(self, item):
        """Translate a html structure of common object in txt view to a rent info.
        """

        # <ul class="shTxInfo">
        #     <li class="rs"><strong><a class="txt-sh-region" href="javascript:;" data-bind="1">台北市</a>-<strong><a class="txt-sh-section" href="javascript:;" data-bind="12">文山區</a></strong></strong></li>
        #     <li class="address"><a href="rent-detail-xxxxxxx.html" target="_blank" title="某某路四段某某華廈!!吉祥入住!!來電成交!!">某某路四段某某華廈!!吉祥入住..</a>&nbsp;<span class="ImgStatus" title="內有房屋照片">附圖</span>&nbsp;&nbsp;(1)</li>
        #     <li class="area">32坪/整層</li>
        #     <li class="price"><strong class="fc-org">12,800元</strong></li>
        #     <li class="visited">543</li>
        #     <li class="update"><strong class="fc-red"><strong class="TodayTime">今日</strong></strong></li>
        # </ul>

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
        """Translate a html structure of recommended object to a rent info.
        """

        # <div class="content">
        #     <p><a href="rent-detail-xxxxxxx.html" target="_blank" title="天母某某居(飯店式管理)" google-data-stat="出售_精選推薦_精選推薦列表"><img src="https://cp2.591.c...x127.jpg" width="172" height="127" alt="天母某某居(飯店式管理)" /></a></p>
        #     <p class="name"><a href="rent-detail-xxxxxxx.html" target="_blank" title="天母某某居(飯店式管理)" google-data-stat="出售_精選推薦_精選推薦列表"><strong>天母某某居(飯店式管理...</strong></a></p>
        #     <p>士林區 - 整層住家<em class="area">12.34坪</em></p>
        #     <p class="fc-org"><strong>80,000元</strong></p>
        # </div>

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
        if origin_result['region'] is '':
            result['region'] = 0
        else:
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
