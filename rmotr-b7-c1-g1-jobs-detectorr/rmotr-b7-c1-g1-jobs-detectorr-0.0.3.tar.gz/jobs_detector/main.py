import click
import requests
from bs4 import BeautifulSoup

from settings import BASE_URL


DEFAULT_KEYWORDS = [
    'Remote',
    'Postgres',
    'Python',
    'Javascript',
    'React',
    'Pandas'
]


@click.group()
def jobs_detector():
    pass


def request_page(post_id):
    url = BASE_URL.format(post_id)
    return requests.get(url)
    
    
def keywords_count_and_stats(keywords, comments, total_job_post_count):
    keyword_counts = {}
    keywords = keywords.split(',')
    
    for keyword in keywords: #initializing keyword_counts dict with 0 for each keyword, and 0 for stats 
                            #therefore, the datastruct looks like keyword_counts[keyword] = [count, stat]
        keyword = keyword.lower()
        keyword_counts[keyword] = [0, 0]
    
        
    for comment in comments:
        comment = str(comment).lower()
        for keyword in keyword_counts.keys():
            if str(keyword) in comment:
                keyword_counts[keyword][0] += 1
    
    for keyword in keyword_counts.keys():
        stat = keyword_counts[keyword][0]/float(total_job_post_count) * 100
        keyword_counts[keyword][1] = int(stat)
    # #==========================
    # for keyword in keyword_counts: #iterate through keys
    #     keyword_counts[keyword][0] = only_text.count(keyword)
        
    #     temp = keyword_counts[keyword][0] / float(total_job_post_count) * 100
    #     keyword_counts[keyword][1] = int(temp)
    
            
    keyword_output =  "Keywords:"
    for keyword in keyword_counts:
        keyword_output = keyword_output + \
        "{}: {} ({}%)\n ".format(keyword.capitalize(), keyword_counts[keyword][0], keyword_counts[keyword][1])
    
    return keyword_output

def combination_count_and_stats(combinations, comments, total_job_post_count):
    combination_dict = {}
    for combination in combinations: #initializing combination_dict with 0 for each keyword, and 0 for stats 
                                    #therefore, the datastruct looks like combination_dict[combination] = [count, stat]
        combination = combination.lower()
        keyword_list = combination.split('-')
        keyword_list_tuple = tuple(keyword_list)
        combination_dict[keyword_list_tuple] = [0,0] 
    #25 for python-remote, 6 for django
    for comment in comments:
        comment = str(comment).lower()
        #(u'django', u'remote') 
        #import ipdb; ipdb.set_trace()
        for combination_keywords in combination_dict.keys(): #iterate through dictionary
            # flag = True
            for keyword in combination_keywords:
                if str(keyword) not in comment:
                    break
            else:
                combination_dict[combination_keywords][0] += 1

    for key in combination_dict:
        temp = combination_dict[key][0] / float(total_job_post_count) * 100
        combination_dict[key][1] = int(temp)

    combination_output = "Combinations:\n" #happy birthday Adrian!!!
    for key_tuple in (combination_dict):
        
        formatted_string = '-'.join(key_tuple).title()
        
        combination_output = combination_output + \
        "{}: {} ({}%)\n".format(formatted_string, combination_dict[key_tuple][0], combination_dict[key_tuple][1])
        
    return combination_output

@jobs_detector.command()
@click.option('-i', '--post-id', type=str, required=True)
@click.option('-k', '--keywords', type=str, default=','.join(DEFAULT_KEYWORDS))
@click.option('-c', '--combinations', type=str,
              callback=lambda _, x: x.split(',') if x else x)
def hacker_news(post_id, keywords=DEFAULT_KEYWORDS, combinations=None):
    """
    This subcommand aims to get jobs statistics by parsing "who is hiring?"
    HackerNews posts based on given set of keywords.
    """

    page = request_page(post_id)
    soup = BeautifulSoup(page.content, "html.parser")

    comments = soup.find_all('span', class_='c00')
    total_job_post_count = len(comments)
    total_job_post_count_output =  "\n Total job posts: {} \n".format(total_job_post_count)
    click.echo(total_job_post_count_output)
    
    only_text = soup.get_text()
    only_text = only_text.lower()
    
    keyword_output = keywords_count_and_stats(keywords, comments, total_job_post_count)
    click.echo(keyword_output)
    click.echo('\n')
    
    if combinations != None:
        combination_output = combination_count_and_stats(combinations, comments, total_job_post_count)
        click.echo(combination_output)
    
    
if __name__ == '__main__':
    jobs_detector()    
    