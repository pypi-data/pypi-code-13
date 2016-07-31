# -*- coding: utf-8 -*-
from __future__ import print_function
import click
import requests
from bs4 import BeautifulSoup
import re

from .settings import BASE_URL, BASE_DIR
from .exceptions import InvalidURLException

import pdb

DEFAULT_KEYWORDS = ['Remote', 'Postgres', 'Python', 'Javascript','React','Pandas']

@click.group()
def jobs_detector():
    pass

@jobs_detector.command()
@click.option('-i', '--post-id', type=str, required=True, help='[required]')
@click.option('-k', '--keywords', type=str, default=','.join(DEFAULT_KEYWORDS))
@click.option('-c', '--combinations', type=str,
              callback=lambda _, x: x.split(',') if x else x)

def hacker_news(post_id, keywords, combinations=None):
    keywords = [word for word in keywords.split(',')]
    # Combine BASE_URL from setting.py with post_id (replace {} with id)
    # Make a HTTP request from URLat(post_id))

    r = requests.get(BASE_URL.format(post_id))
    if r.status_code != 200:
        raise InvalidURLException
    
    # BeautifulSoup above request
    soup = BeautifulSoup(r.text, 'html.parser')
    
    # Get all the things (beginning of thread and comments)
    comment_tree = soup.find_all("tr", ["athing", "athing comtr "]) #list of bs4.element.Tag objects; use .text to get plain-text
     
    # Get image tag's width to determine margin
    job_posts = []
    for comment in comment_tree:
        if comment.select('img'):
            comment_width = int(comment.select('img')[0].get('width'))
            if comment_width == 0:
                job_posts.append(comment)

    """
    This subcommand aims to get jobs statistics by parsing "who is hiring?"
    HackerNews posts based on given set of keywords.
    """
    
    # Finds if keyword is in job post, count++ if it is
    count_dict = {key:0 for key in keywords}
    job_posts_found = 0
    for comment in job_posts:
        for word in keywords:
            if word.lower() in comment.text.lower():
                count_dict[word] += 1
                job_posts_found += 1
   
    '''IMPORTANT: Check if all the combinations variables are plural; caused too much debug time already'''
    if combinations:
        # combinations = [keyword-keyword-etc,keyword-keyword-etc]
        combination_check_list = [item.split('-') for item in combinations] # [[keyword,keyword,etc],[keyword,keyword,etc]]
        # click.echo(combination_check_list)
        combination_dict = {key:0 for key in combinations} # {}
#       combined_kw_list = dict(zip(combinations, combination_check_list))

        for comment in job_posts:
            for index, combo in enumerate(combination_check_list):
                # Basically all() without extra def, then record a hit if matches
                if [word for word in combo if word.lower() in comment.text.lower()] == combo:
                    combination_dict[combinations[index]] += 1
                else:
                    break
        
        # for comment in job_posts:
        #     for combination in combinations:
        #         break_flag = 0
        #         for pairs in combination_check_list:
        #             for word in pairs:
        #                 if word.lower() not in comment.lower():
        #                     break_flag = 1
        #                     break
        #         if break_flag == 1:
        #             break
        #     else:
        #         combination_dict[combination] += 1
#                       
    
    # Building expected output
    expected_list = ['Total job posts: {0}'.format(len(job_posts)), 'Keywords:']
                    # 'Total job hits: {0}'.format(job_posts_found)
    for key, val in count_dict.items():
        expected_list.append('{0}: {1} ({2}%)'.format(key, val, int(val/float(len(job_posts))*100)))
    
    if combinations:
        expected_list.append('Combinations:')
        for key, val in combination_dict.items():
            expected_list.append('{0}: {1} ({2}%)'.format(key, val, int(val/float(len(job_posts))*100)))
    
    # click.echo(expected_list) 
    print(expected_list)


if __name__ == '__main__':
    jobs_detector()
