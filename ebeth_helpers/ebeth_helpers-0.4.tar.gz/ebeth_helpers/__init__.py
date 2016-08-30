'''
helpers:
order/order status (wimca?) (order_and_wait_10) (order_update)
'''

from gbdxtools import Interface
gbdx = Interface()
import pprint
pp = pprint.PrettyPrinter(indent=4)
import requests
import json

# will probably need an init function to initiate gbdx


def gbdx_go():
    gbdx = Interface()
    return gbdx


def wimwa(workflow_id):
    workflow = gbdx.Workflow([])
    workflow.id = workflow_id
    return workflow.status


def the_full_wimwa(results):
    new_results = []
    for i in range(len(results)):
        workflow_info = results[i]
        workflow = gbdx.Workflow([])
        workflow.id = results[i]['workflow_id']
        workflow_info['status'] = workflow.status['event']
        new_results.append(workflow_info)
    return new_results


def get_cat(catalog_id):
    token = "Bearer %s" % gbdx.gbdx_connection.access_token
    url = 'https://geobigdata.io/catalog/v1/record/' + str(catalog_id) + '?includeRelationships=false'
    headers = {'Content-Type': 'application/json',"Authorization": token}
    catID_result = requests.get(url, headers=headers, data=json.dumps(catalog_id))
    metadata = catID_result.json()['properties']
    return metadata

