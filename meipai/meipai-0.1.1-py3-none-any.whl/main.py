import argparse

from src.api import MeiPai
from .cache import get_last_page
from .player import Player

__author__ = 'PyBeaner'


def play(query, videos=None):
    videos = videos if videos else MeiPai().search(query)
    all_played = True
    for video in videos:
        if not Player.played(video):
            Player.play(video)
            all_played = False
            break
    if all_played:
        print('正在加载视频数据')
        videos = MeiPai().search(query, page=get_last_page(query, 'mv') + 1)
        if not videos:
            print("没有更多关于" + query + "的视频了")
            return
        return play(query, videos)


def start():
    parser = argparse.ArgumentParser()
    parser.add_argument('query')
    parser.add_argument('--topic', action='store_true', help='搜索话题')
    args = parser.parse_args()
    query = args.query
    if args.topic:
        query = '#' + query + '#'

    play(query)


if __name__ == '__main__':
    start()

    # topic_names = api.search('萌宠', 'topic')
    # print(topic_names)
    # topic = Topic(random.choice(topic_names))
    # print(topic.name, topic.topic_id)
