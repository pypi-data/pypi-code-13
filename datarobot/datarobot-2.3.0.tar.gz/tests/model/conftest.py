import json

from datarobot import enums

import pytest
import responses


@pytest.fixture
def job_id():
    return '13'


@pytest.fixture
def job_url(project_id, job_id):
    return 'https://host_name.com/projects/{}/jobs/{}/'.format(project_id, job_id)


@pytest.fixture
def feature_impact_url(project_id, model_id):
    return 'https://host_name.com/projects/{}/models/{}/featureImpact/'.format(project_id, model_id)


@pytest.fixture
def feature_impact_job_creation_response(feature_impact_url, job_url):
    responses.add(
        responses.POST,
        feature_impact_url,
        body='',
        status=202,
        adding_headers={'Location': job_url})


@pytest.fixture
def feature_impact_server_data():
    return {u'count': 2,
            u'featureImpacts': [
                {u'featureName': u'dates',
                 u'impactNormalized': 1.0,
                 u'impactUnnormalized': 2.0},
                {u'featureName': u'item_ids',
                 u'impact': 0.93,
                 u'impactUnnormalized': 1.87}],
            u'next': None,
            u'previous': None}


@pytest.fixture
def feature_impact_response(feature_impact_server_data, feature_impact_url):
    body = json.dumps(feature_impact_server_data)
    responses.add(
        responses.GET,
        feature_impact_url,
        status=200,
        content_type='application/json',
        body=body
    )


@pytest.fixture
def job_running_server_data(job_id, project_id, job_url):
    return {
        'status': enums.QUEUE_STATUS.INPROGRESS,
        'url': job_url,
        'id': job_id,
        'jobType': 'featureImpact',
        'projectId': project_id
    }


@pytest.fixture
def job_finished_server_data(job_id, project_id, job_url):
    return {
        'status': enums.QUEUE_STATUS.COMPLETED,
        'url': job_url,
        'id': job_id,
        'jobType': 'featureImpact',
        'projectId': project_id
    }


@pytest.fixture
def feature_impact_completed_response(job_finished_server_data, job_url, feature_impact_url):
    """
    Loads a response that the given job is a featureImpact job, and is in completed
    """
    responses.add(responses.GET,
                  job_url,
                  body=json.dumps(job_finished_server_data),
                  status=303,
                  adding_headers={'Location': feature_impact_url},
                  content_type='application/json')


@pytest.fixture
def feature_impact_running_response(job_running_server_data, job_url):
    """
    Loads a response that the given job is a featureImpact job, and is running
    """
    responses.add(responses.GET,
                  job_url,
                  body=json.dumps(job_running_server_data),
                  status=200,
                  content_type='application/json')
