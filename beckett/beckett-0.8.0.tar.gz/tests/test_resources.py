#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_resources
----------------------------------

Tests for `beckett.resources` module.
"""

from beckett.resources import BaseResource


import responses

from tests.fixtures import (
    AuthorSubResource, HypermediaAuthorsResource,
    HypermediaBlogsResource, PeopleResource, SubResourcePeopleResource
)


def test_base_resource_attributes():
    """
    Base class tests
    """

    model = BaseResource(id='1')
    assert model.__str__() == '<Resource | 1>'


def test_custom_resource():
    """
    Test our own custom resource - MyTestResource
    """
    data = {
        'name': 'Wort wort',
        'slug': 'sluggy',
        'not_valid': 'nooo'
    }
    instance = PeopleResource(**data)
    # We should have this attribute
    assert hasattr(instance, 'name')
    # But this one is missing
    assert not hasattr(instance, 'another_thing')
    # and this one is not valid
    assert not hasattr(instance, 'not_valid')
    assert instance.__str__() == '<People | Wort wort>'
    # It should also have parent Meta attributes
    assert hasattr(instance.Meta, 'valid_status_codes')


def test_hypermedia_custom_resource():
    """
    Test our custom Hypermedia resource loads correctly
    """
    data = {
        'name': 'Wort wort',
        'slug': 'sluggy',
        'not_valid': 'nooo',
        'author': 'http://dev/api/authors/1'
    }
    instance = HypermediaBlogsResource(**data)
    assert hasattr(instance, 'get_authors')


def test_hypermedia_custom_resource_non_registered_urls():
    """
    Test our custom Hypermedia resource handles
    URls that aren't registered.
    """
    data = {
        'name': 'Wort wort',
        'slug': 'sluggy',
        'not_valid': 'nooo',
        # This should not appear!
        'author': 'http://dev/api/foobar/1'
    }
    instance = HypermediaBlogsResource(**data)
    assert not hasattr(instance, 'get_authors')


@responses.activate
def test_hypermedia_custom_resource_calling():
    """
    Test our custom Hypermedia resource make HTTP calls correctly
    """
    responses.add(responses.GET, 'http://dev/api/authors/1',
                  body='''
                    {"id": "1", "title": "blog title",
                     "slug": "blog-title",
                     "content": "This is some content"}''',
                  status=200,
                  content_type='application/json')
    data = {
        'name': 'Wort wort',
        'slug': 'sluggy',
        'not_valid': 'nooo',
        'author': 'http://dev/api/authors/1'
    }
    instance = HypermediaBlogsResource(**data)
    response = instance.get_authors()
    assert isinstance(response[0], HypermediaAuthorsResource)
    assert responses.calls[0].request.url == 'http://dev/api/authors/1'
    assert responses.calls[0].request.method == 'GET'


@responses.activate
def test_hypermedia_custom_resource_calling_list_of_resources():
    """
    Test our custom Hypermedia resource make HTTP calls correctly
    when the related results are a list of urls
    """
    responses.add(responses.GET, 'http://dev/api/authors/1',
                  body='''
                    {"id": "1", "title": "blog title",
                     "slug": "blog-title",
                     "content": "This is some content"}''',
                  status=200,
                  content_type='application/json')
    responses.add(responses.GET, 'http://dev/api/authors/2',
                  body='''
                    {"id": "2", "title": "second title",
                     "slug": "blog-title",
                     "content": "This is some content"}''',
                  status=200,
                  content_type='application/json')
    data = {
        'name': 'Wort wort',
        'slug': 'sluggy',
        'not_valid': 'nooo',
        'author': ['http://dev/api/authors/1', 'http://dev/api/authors/2']
    }
    instance = HypermediaBlogsResource(**data)
    response = instance.get_authors()
    assert isinstance(response[0], HypermediaAuthorsResource)
    assert response[0].title == 'blog title'
    assert response[1].title == 'second title'
    assert responses.calls[0].request.url == 'http://dev/api/authors/1'
    assert responses.calls[0].request.method == 'GET'
    assert responses.calls[1].request.url == 'http://dev/api/authors/2'
    assert responses.calls[1].request.method == 'GET'


@responses.activate
def test_hypermedia_custom_resource_calling_list_of_resources_many_items():
    """
    Test our custom Hypermedia resource make HTTP calls correctly
    when the related results are a list of urls and the
    results are a list themselves
    """
    responses.add(responses.GET, 'http://dev/api/authors/1',
                  body='''
                    [{"id": "1", "title": "blog title",
                     "slug": "blog-title",
                     "content": "This is some content"},
                     {"id": "1", "title": "blog title",
                      "slug": "blog-title",
                      "content": "This is some content"}]''',
                  status=200,
                  content_type='application/json')
    responses.add(responses.GET, 'http://dev/api/authors/2',
                  body='''
                    {"id": "2", "title": "second title",
                     "slug": "blog-title",
                     "content": "This is some content"}''',
                  status=200,
                  content_type='application/json')
    data = {
        'name': 'Wort wort',
        'slug': 'sluggy',
        'not_valid': 'nooo',
        'author': ['http://dev/api/authors/1', 'http://dev/api/authors/2']
    }
    instance = HypermediaBlogsResource(**data)
    response = instance.get_authors()
    # The first item is a list of responses
    assert isinstance(response[0], list)
    # But the first is just a single item
    assert isinstance(response[1], HypermediaAuthorsResource)
    assert response[1].title == 'second title'
    assert responses.calls[0].request.url == 'http://dev/api/authors/1'
    assert responses.calls[0].request.method == 'GET'
    assert responses.calls[1].request.url == 'http://dev/api/authors/2'
    assert responses.calls[1].request.method == 'GET'


def test_parse_url_and_validate_single_instance():
    """
    Test the _parse_url_and_validate class method
    """
    result = HypermediaBlogsResource._parse_url_and_validate(
        'http://valid.com')
    assert result


def test_sub_resource_generates_okay():
    """
    Test that we generate subresources as expected
    """
    data = {
        "author": {
            "name": "This is the subresource"
        },
        "slug": "this-is-the-resource",
        "another_thing": "this-is-also-the-resource"
    }

    instance = SubResourcePeopleResource(**data)
    assert isinstance(instance.author, AuthorSubResource)
    assert instance.author.name == 'This is the subresource'
    assert instance.author.__str__() == '<Author | This is the subresource>'
    assert instance.slug == 'this-is-the-resource'


def test_a_list_of_sub_resource_generates_okay():
    """
    Test that we generate subresources as expected when they are a list
    """
    data = {
        "author": [
            {
                "name": "This is the subresource"
            },
            {
                "name": "This is another subresource"
            }
        ],
        "slug": "this-is-the-resource",
        "another_thing": "this-is-also-the-resource"
    }

    instance = SubResourcePeopleResource(**data)
    assert isinstance(instance.author, list)
    assert instance.author[0].name == 'This is the subresource'
    assert instance.author[1].name == 'This is another subresource'
    assert instance.slug == 'this-is-the-resource'
