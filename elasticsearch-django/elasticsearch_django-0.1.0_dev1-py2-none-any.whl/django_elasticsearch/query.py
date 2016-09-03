# -*- coding: utf-8 -*-
"""Search3 query-related functions."""
from calendar import timegm

from elasticsearch_dsl import Search, SF, Q

from elasticsearch_django.models import SearchQuery
from elasticsearch_django.settings import get_client

# global boost values - put here to make it easier to edit
BOOST_FULL_NAME = 100
BOOST_JOB_TITLE = 10
BOOST_CORE_SKILLS = 5
BOOST_SUMMARY = 1
BOOST_EMPLOYERS = 1
BOOST_ROLES = 1

FUNCTION_SCORE_MODE = "multiply"
FUNCTION_BOOST_MODE = "multiply"
FUNCTION_BOOST = 1

# origin value for the work history function
WORK_HISTORY_COUNT = 5


def day_rate_func(origin_day_rate, weight=1):
    """
    Create the day rate scoring function.

    Args:
        origin_day_rate: decimal, the midpoint day rate used as
            the origin in the function.

    Kwargs:
        weight: int, the weighting of the function relative to
            the other functions in the function_socre.

    Returns:
        an SF function object that can be used in a search query.

    """
    return SF(
        'gauss',
        rate__day={
            "origin": origin_day_rate,
            "scale": 50,
            "decay": 0.8
        },
        weight=weight
    )


def last_activity_func(origin_timestamp, weight=1):
    """
    Create the last activity scoring function.

    Args:
        origin_timestamp: datetime, the timestamp used as the
            origin in the function.

    Kwargs:
        weight: int, the weighting of the function relative to
            the other functions in the function_socre.

    Returns:
        an SF function object that can be used in a search query.

    """
    return SF(
        'exp',
        last_activity_timestamp={
            "origin": timegm(origin_timestamp.timetuple()),
            "scale": 604800,
            "decay": 0.5
        },
        weight=weight
    )


def work_history_func(origin_count, weight=1):
    """
    Create the work history count scoring function.

    Args:
        origin_count: int, the numbner of work history items used as
            the origin in the function.

    Kwargs:
        weight: int, the weighting of the function relative to
            the other functions in the function_socre.

    Returns:
        an SF function object that can be used in a search query.

    """
    return SF(
        'gauss',
        work_history__count={
            "origin": origin_count,
            "scale": 2,
            "decay": 0.7
        },
        weight=weight
    )


def match_queries(search_term):
    """Return list of Q objects used for the free text matching.

    Args:
        search_term: string, a free text search term.

    Returns:
        a list of Q objects used as the 'should' value of the bool query.

    """
    return [
        Q('match', full_name={'query': search_term, 'operator': 'or', 'boost': BOOST_FULL_NAME}),  # noqa
        Q('match', job_title={'query': search_term, 'boost': BOOST_JOB_TITLE, 'fuzziness': 'auto'}),  # noqa
        Q('match', core_skills={'query': search_term, 'boost': BOOST_CORE_SKILLS, 'fuzziness': 'auto'}),  # noqa
        Q('match', summary={'query': search_term, 'boost': BOOST_SUMMARY, 'fuzziness': 'auto'}),  # noqa
        Q('match', work_history__employers={'query': search_term, 'boost': BOOST_EMPLOYERS, 'fuzziness': '0'}),  # noqa
        Q('match', work_history__roles={'query': search_term, 'boost': BOOST_ROLES, 'fuzziness': '0'}),  # noqa
    ]


def filter_queries(discipline_id, rate_range, available_from):
    """
    Return the list of filter matches used to restrict the document set.

    Args:
        discipline_id: int, the id of the discipline to filter on.
        rate_range: 2-tuple of int containing the min/max ranges to filter on.
        available_from: datetime, the availability filter.

    Returns:
        A list of Q objects, one per field match, used as the 'filters' value of the bool query.

    """
    return [
        Q('terms', discipline__id=[discipline_id]),
        Q('range', rate__day={'gte': min(rate_range), 'lte': max(rate_range)}),
        Q('match', approval_state='approved'),
        Q('range', available_from={'lte': available_from.isoformat()}),
    ]


def bool_query(discipline_id, rate_range, available_from, search_term=None, boost=1.0):
    """
    Create the 'bool' query to be added to the function_score query.

    This returns a 'bool' query that includes a 'should' block if there
    are any search terms passed in, else it is just a list of filters. The
    form of the JSON is:

    {
        "bool" : {
            "filter": [],
            "should" : [],
            "minimum_should_match" : 1,
            "boost" : 1.0
        }
    }

    See https://www.elastic.co/guide/en/elasticsearch/reference/2.3/query-dsl-bool-query.html

    Args:
        discipline_id: int, the id of the discipline to filter on.
        rate_range: 2-tuple of int containing the min/max ranges to filter on.
        available_from: datetime, the availability filter.

    Kwargs:
        search_term: string, the free text search on which to search.
        boost: decimal, the value by which to boost this entire query

    Returns:
        A single Q object that can encapsulates the query.

    """
    if search_term:
        return Q(
            'bool',
            filter=filter_queries(discipline_id, rate_range, available_from),
            should=match_queries(search_term),
            minimum_should_match=1,
            boost=boost
        )
    else:
        return Q(
            'bool',
            filter=filter_queries(discipline_id, rate_range, available_from),
            boost=boost
        )


def build_search(discipline_id, rate_range, available_from, search_term=None):
    """
    Build up the Search object from inputs.

    The structure of the query is important. We are generating a 'function_score'
    query that internally contains a query and a list of functions:

    {
        "query": {
            "function_score": {
                "query": {},
                "boost": "",
                "functions": [],
                "max_boost": "number",
                "score_mode": "(multiply|max|...)",
                "boost_mode": "(multiply|replace|...)",
                "min_score" : "number"
            }
        }
    }

    Args:
        discipline_id: int, the id of the discipline to filter on.
        rate_range: 2-tuple of int containing the min/max ranges to filter on.
        available_from: datetime, the availability filter.

    Kwargs:
        search_term: string, the free text search on which to search.

    Returns:
        A Search object that can be used to execute the search itself.

    """
    assert len(rate_range) == 2, "rate_range must be specified as a 2-tuple (min, max)."
    return Search(using=get_client()).query(
        'function_score',
        functions=[
            day_rate_func(sum(rate_range) / 2),
            last_activity_func(available_from),
            work_history_func(WORK_HISTORY_COUNT)
        ],
        query=bool_query(
            discipline_id,
            rate_range,
            available_from,
            search_term=search_term
        ),
        score_mode=FUNCTION_SCORE_MODE,
        boost_mode=FUNCTION_BOOST_MODE,
        boost=FUNCTION_BOOST,
    )


def execute(discipline_id, rate_range, available_from, search_term=None, page=1, size=10):
    """
    Create and execute the search against ES, and log as a SearchQuery.

    This function does it all-in-one - creates the Search object, runs
    the SearchQuery.execute method, logs the query and returns the
    SeaerchQuery object.

    Args:
        discipline_id: int, the id of the discipline to filter on.
        rate_range: 2-tuple of int containing the min/max ranges to filter on.
        available_from: datetime, the availability filter.

    Kwargs:
        search_term: string, the free text search on which to search.
        page: int, the page number, defaults to 1 (first page)
        size: int, the number of items per page, using in conjunction with page.

    Returns:
        A SearchQuery object that contains the search results, and that can
        be be used to fetch the Django objects:

            sq = query.execute(
                discipline_id=1,
                rate_range=(300, 400),
                available_from=datetime.date(2016, 08, 30),
                search_term="Angular"
            )
            objs = FreelancerProfile.objects.from_search_query(sq)

    Paging implemented using the python slice pattern - see
    http://elasticsearch-dsl.readthedocs.io/en/latest/search_dsl.html#pagination

    """
    search = build_search(discipline_id, rate_range, available_from, search_term=search_term)
    first, last = page_slice(page, size)
    return SearchQuery.execute(search[first:last])


def page_slice(page_number, page_size):
    """Convert page number / size into from:to slice indices."""
    first = (page_number - 1) * page_size
    last = first + (page_size - 1)
    return (first, last)
