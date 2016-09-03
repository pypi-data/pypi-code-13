# -*- coding: utf-8 -*-
"""Search3 search-related functions."""
from elasticsearch_django.models import QueryLog


def do_search(search, user=None, reference=None):
    """Execute search and log response.

    This function is a wrapper around Search.execute()
    and QueryLogManager.create_log.

    Returns the search response.

    """
    return QueryLog.objects.create_log(
        search=search,
        response=search.execute(),
        user=user,
        reference=reference
    )
