import time

import requests

from eridu.logger import logger
from eridu.config import ACCESS_KEY, SITE
from eridu.config import POST_IDS_URL, POST_IDS_FILTER, POST_IDS_NUMBER, POST_IDS_SORT, POST_IDS_ORDER
from eridu.config import QUESTIONS_URL, QUESTIONS_FILTER, QUESTIONS_SORT, QUESTIONS_ORDER
from eridu.config import ANSWERS_URL, ANSWERS_FILTER, ANSWERS_SORT, ANSWERS_ORDER



def get_questions(question_ids, url=QUESTIONS_URL, filter=QUESTIONS_FILTER, access_key=ACCESS_KEY, site=SITE, sort=QUESTIONS_SORT, order=QUESTIONS_ORDER):
    url = url.format(';'.join([str(i) for i in question_ids]))

    payload = {
        "pagesize": 100,
        "key": access_key,
        "site": site,
        "sort": sort,
        "order": order,
        "filter": filter,
    }

    logger.info('Getting questions with payload: {}'.format(payload))

    r = requests.get(url, params=payload)

    data = r.json()

    if data.get('backoff') is not None:
        time.sleep(int(data.get('backoff')))

    return data

def get_answers(answer_ids, url=ANSWERS_URL, filter=ANSWERS_FILTER, access_key=ACCESS_KEY, site=SITE, sort=ANSWERS_SORT, order=ANSWERS_ORDER):
    url = url.format(';'.join([str(i) for i in answer_ids]))

    payload = {
        "pagesize": 100,
        "key": access_key,
        "site": site,
        "sort": sort,
        "order": order,
        "filter": filter,
    }

    logger.info('Getting answers with payload: {}'.format(payload))

    r = requests.get(url, params=payload)

    data = r.json()

    question_ids = [answer['question_id'] for answer in data['items']]

    questions = get_questions(question_ids)

    tags = {question['question_id']: question['tags'] for question in questions['items']}

    for answer in data['items']:
        answer['tags'] = tags[answer['question_id']]

    if data.get('backoff') is not None:
        time.sleep(int(data.get('backoff')))

    return data


def get_post_ids(page, url=POST_IDS_URL, filter=POST_IDS_FILTER, n_posts=POST_IDS_NUMBER, access_key=ACCESS_KEY, site=SITE, sort=POST_IDS_SORT, order=POST_IDS_ORDER):
    payload = {
        "pagesize": n_posts,
        "page": page,
        "key": access_key,
        "site": site,
        "sort": sort,
        "order": order,
        "filter": filter,
    }
    logger.info('Getting post ids with payload: {}'.format(payload))

    r = requests.get(url, params=payload)

    data = r.json()

    if data.get('backoff') is not None:
        time.sleep(int(data.get('backoff')))

    return data


def split_post_ids(post_ids):
    logger.info('Splitting post ids into question and answer ids')

    question_ids, answer_ids = [], []

    for item in post_ids:
        if item['post_type'] == "question":
            question_ids.append(item['post_id'])
        elif item['post_type'] == 'answer':
            answer_ids.append(item['post_id'])

    return {
        "question_ids": question_ids,
        "answer_ids": answer_ids
    }

def filter_posts_by_tag(posts, tags):
    tags = set(tags)
    return [post for post in posts if set(post['tags']) & tags]
