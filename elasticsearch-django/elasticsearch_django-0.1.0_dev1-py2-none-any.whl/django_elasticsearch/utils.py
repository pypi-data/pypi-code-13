# -*- coding: utf-8 -*-
"""Temporary file used for sharing search concepts."""

from elasticsearch_dsl import Search, SF, Q

from django.utils.timezone import now as tz_now

from elasticsearch_django.settings import get_client


def day_rate_func(origin, weight=1):
    """Create the day rate scoring function."""
    return SF(
        'gauss',
        rate__day={
            "origin": origin,
            "scale": 50,
            "decay": 0.8
        },
        weight=weight
    )


def last_activity_func(origin, weight=1):
    """Create the last activity scoring function."""
    return SF(
        'exp',
        last_activity_timestamp={
            "origin": origin,
            "scale": 604800,
            "decay": 0.5
        },
        weight=weight
    )


def work_history_func(origin, weight=1):
    """Create the work history count scoring function."""
    return SF(
        'gauss',
        work_history__count={
            "origin": origin,
            "scale": 2,
            "decay": 0.7
        },
        weight=weight
    )

# 1. create a blank match_all query
# search = Search().using(get_client())


# 2. Add the function scoring.
def add_function_score(search, day_rate, work_history=5, timestamp=tz_now()):
    """Add function_score to the search."""
    return search.query(
        'function_score',
        functions=[
            day_rate_func(day_rate, 0),
            last_activity_func(timestamp, 0),
            work_history_func(work_history, 0)
        ],
        score_mode="multiply",
        boost_mode="multiply",
    )


# 3. Add the search terms (if supplied)
def add_search_query(search, search_term):
    """Add the search terms."""
    return search.query(
        'bool',
        should=[
            Q('match', full_name={'query': search_term, 'operator': 'or', 'boost': 100}),
            Q('match', job_title={'query': search_term, 'boost': 10, 'fuzziness': 'auto'}),
            Q('match', core_skills={'query': search_term, 'boost': 5, 'fuzziness': 'auto'}),
            Q('match', summary={'query': search_term, 'boost': 1, 'fuzziness': 'auto'}),
            Q('match', work_history__employers={'query': search_term, 'boost': 1, 'fuzziness': '0'}),  # noqa
            Q('match', work_history__roles={'query': search_term, 'boost': 1, 'fuzziness': '0'}),
        ],
        minimum_should_match=1,
    )


# 4. add the fixed filters: NB this must come last, else the
# minimum_should_match gets wiped - no explanation.
def add_filters(search, discipline_id, min_rate, max_rate, available_from):
    """Add the fixed filters. Must go last."""
    return (
        search
        .filter('terms', discipline__id=[discipline_id])
        .filter('range', rate__day={'gte': min_rate, 'lte': max_rate})
        .filter('match', approval_state='approved')
        .filter('range', available_from={'lte': available_from.isoformat()})
    )


def build_search(discipline_id, rate_range, available_from, search_term=None):
    """Build up the Search object from inputs."""
    mid_range = min(rate_range) + (max(rate_range) - min(rate_range)) / 2
    search = Search(using=get_client())
    if search_term:
        search = add_function_score(search, mid_range)
    search = add_search_query(search, search_term)
    search = add_filters(search, discipline_id, min(rate_range), max(rate_range), available_from)
    return search

# Putting it all together
#
# search_term = "Angular"
# rate_range = (300, 400)
# discipline_id = 1
# available_from = datetime.date(2016, 8, 30)

# search = build_search(discipline_id, rate_range, available_from, search_term=search_term)
# SearchQuery.execute(search, reference=ref)
# json.dumps(search.to_dict())
