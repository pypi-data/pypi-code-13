import os
import urllib
import click
from bs4 import BeautifulSoup
from . import exceptions
from . import settings

DEFAULT_KEYWORDS = ['remote', 'postgres',
                    'python', 'javascript', 'react', 'pandas']


@click.group()
def jobs_detector():
    pass


@jobs_detector.command()
@click.option('-i', '--post_id', type=str, required=True, help='Post id from Hackernews.')
@click.option('-k', '--keywords', type=str, default=','.join(DEFAULT_KEYWORDS),
              help='Keywords for counting')
@click.option('-c', '--combinations', type=str, default=None,
              callback=lambda ctx, _, x: x.split(',') if x else x, help='Keywords with combo')
def hacker_news(post_id, keywords, combinations):
    '''
    This subcommand aims to get jobs statistics by parsing "who is hiring?"
    HackerNews posts based on given set of keywords.
    '''
    posts = get_posts(get_html(post_id))
    word_list = keywords.split(',')
    kw_dict = get_stats_for_kw(posts, word_list)
    combo_dict = get_stats_for_cm(posts, combinations)
    display_to_terminal(len(posts), kw_dict, combo_dict)


def get_stats_for_kw(posts, keywords):
    '''
    This will return a dict with count of each KEYWORD in the list of posts
    '''
    kw_dict = {}
    # The lambda function will return count of a KEYWORD in a post
    word_count = lambda post, word: post.lower().count(word.lower())

    for word in keywords:
        count = 0
        for post in posts:
            count += 1 if word_count(post, word) else 0
        if count > 0:
            word_pct = round((count * 100) / len(posts))
            kw_dict[word.title()] = (count, int(word_pct))

    return kw_dict


def get_stats_for_cm(posts, combinations):
    '''
    This will return a dict with count of each COMBINATION in the list of posts
    '''
    if not combinations:
        return None

    combo_dict = {}

    for combo in combinations:
        combo_list = combo.split('-')
        combo = '-'.join([x.title() for x in combo_list])
        count = 0
        for post in posts:
            val = get_stats_for_kw([post], combo_list).values()
            if len(val) == len(combo_list):
                count += 1
        if count > 0:
            combo_pct = round((count * 100) / len(posts))
            combo_dict[combo] = (count, int(combo_pct))

    return combo_dict


def display_to_terminal(post_count, kw_dict, combo_dict):
    """Output statistics to terminal"""
    print("Total job posts: {}".format(post_count))

    print("\nKeywords:")
    for word, count in kw_dict.items():
        print("{}: {} ({}%)".format(word, count[0], count[1]))

    if combo_dict:
        print "\nCombinations:"
        for combo, count in combo_dict.items():
            print("{}: {} ({}%)".format(combo, count[0], count[1]))


def get_posts(html_data):
    '''Parse html file and return a list of job posts'''
    post_list = []

    def parse_file():
        with open(html_data) as html_file:
            parser = BeautifulSoup(html_file, 'html.parser')
            title = parser.select_one(".storylink")
            if not title or (title and not 'Ask HN: Who is hiring?' in title.text):
                return None
            cmnt_rows = parser.find_all("tr", class_="athing comtr ")
            for item in cmnt_rows:
                if item.select('img[width=0]') and item.select_one(".c00"):
                    post_list.append(item.select_one(".c00").text)
        return True
    parse_status = parse_file()
    os.remove(html_data)
    if not parse_status:
        raise exceptions.ValueError('Invalid Post id')
    return post_list


def get_html(post_id):
    '''Connect to hacker news using post_id and save return data as an html file.
       Returns a path to the html file.
    '''
    url_to_fetch = settings.BASE_URL.replace('{}', post_id)
    path_to_save = os.path.join(settings.BASE_DIR, post_id + ".html")

    webpage_in_file = urllib.URLopener()
    webpage_in_file.retrieve(url_to_fetch, path_to_save)
    return path_to_save


if __name__ == '__main__':
    jobs_detector()
