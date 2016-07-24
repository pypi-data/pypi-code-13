import json
from urllib.parse import urlencode, quote_plus

from bs4 import BeautifulSoup
from requests.sessions import Session

from .cache import cache_search_result, check_cache_and_return_result

__author__ = 'PyBeaner'

headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'www.meipai.com',
    'Referer': 'http://www.meipai.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36'
}


class Topic:
    def __init__(self, name):
        self.name = name
        self._id = None

    def __getattr__(self, item):
        if item == 'topic_id':
            if self._id:
                return self._id
            self._id = self._get_id()
            return self._id
        return getattr(super, item)

    def _get_id(self):
        session = Session()
        resp = session.request('GET', 'http://www.meipai.com/topic/' + quote_plus(self.name),
                               headers=headers)
        html = BeautifulSoup(resp.content, 'html.parser')
        return html.find(class_='topic-txt').attrs['data-id']

    def __str__(self):
        return self.name


class MeiPai:
    def __init__(self):
        self.session = Session()
        self.session.headers = headers

    def search(self, query, search_type='mv', page=1):
        query = query.strip()
        # topic
        if query.startswith('#'):
            topic = query.strip('#')
            return self.get_videos_by_topic(topic)
        cache_exists, result = check_cache_and_return_result(query=query, search_type=search_type, page=page)
        if cache_exists:
            return result
        url = 'http://www.meipai.com/search/{search_type}?'.format(search_type=search_type) + \
              urlencode({'q': query, 'page': page})
        resp = self.session.request('GET', url)
        html = BeautifulSoup(resp.content, 'html.parser')
        if search_type == 'mv':
            video_links = [div.attrs['data-video'].strip() for div in html.find_all(class_='content-l-video')]

            # associated_words = self.word_association(query)
            # print("你是否还想搜索：" + ",".join(associated_words))
            result = video_links
        elif search_type == 'topic':
            result = [div.text.strip().strip('#') for div in html.find_all(class_='tcard-name')]
        else:
            result = []

        cache_search_result(query, search_type, page, result)
        return result

    def get_videos_by_topic(self, topic_name):
        """
        get top videos by topic
        :param topic_name:
        :return:
        """
        topic = Topic(topic_name)
        topic_id = topic.topic_id
        url = "http://www.meipai.com/topics/hot_timeline?page=1&count=24&tid={topic_id}".format(topic_id=topic_id)
        resp = self.session.request('GET', url)
        result = json.loads(resp.text)
        return [media['video'] for media in result['medias']]

    # get associated words
    def word_association(self, word):
        url = 'http://www.meipai.com/search/word_assoc?' + urlencode({'q': word})
        resp = self.session.request('GET', url)
        return json.loads(resp.text)


if __name__ == '__main__':
    api = MeiPai()
    print(api.search('性感'))
    # topic_names = api.search('萌宠', 'topic')
    # print(topic_names)
    # topic = Topic(random.choice(topic_names))
    # print(topic.name, topic.topic_id)
