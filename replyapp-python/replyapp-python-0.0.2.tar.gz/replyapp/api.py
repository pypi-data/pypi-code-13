import requests
import re
import json

class ReplyAppError(Exception):
    def __init__(self, response):
        self.response = response

class ReplyApp():
    '''
    ReplyApp
    A python 3 wrapper for v1 of the ReplyApp api
    This wrapper uses getattr to build complete urls.
    Example:
        from replyapp import ReplyApp
        ra = ReplyApp('Api_Key')

        #ACTIONS:
        #Mark person as replied
        ra.actions.markasreplied(method='POST', data={'email': 'name@company.com'})
        ra.actions.markasreplied(method='POST', data={'domain': 'company.com'})

        #Push person to the campaign
        ra.actions.pushtocampaign(method='POST', data={'campaignId': 121, 'email': 'name@company.com'})

        #Add person and push to campaign
        data = {
            "campaignId": 121,
            "email": "name@company.com",
             "firstName": "James",
             "lastName": "Smith",
             "company": "Global Tech",
             "city": "San Francisco",
             "state": "CA",
             "country": "US",
             "title": "VP off Marketing"
         }
        ra.actions.addandpushtocampaign(method='POST', data=data)

        #Remove person from campaign by Id
        ra.actions.removepersonfromcampaignbyid(method='POST', data={'campaignId': 121, 'email': 'name@company.com'})

        #Remove person from all campaigns
        ra.actions.removepersonfromallcampaigns(method='POST', data={'email': 'name@company.com'})


        #People
        #Listing people
        ra.people()

        #Getting people from id
        ra.people.{{ID}}()
        #Getting people from email
        ra.people(data={'email': 'name@company.com'})

        #Saving people
        ra.people(method='POST', data={'id': 2232, 'email': james@globaltech.com', 'firstName': 'James', 'lastName': 'Smith', 'company': 'Global Tech', 'title': 'VP of Marketing'})

        #Deleting peiple
        ra.people(method='DELETE', data={'email': 'name@company.com'})
        ra.people.{{ID}}(method='DELETE')
    '''
    def __init__(self, api_key, *args, **kwargs):
        self.api_key = api_key
        self.api_version = 'v1'
        self.base_url = 'https://run.replyapp.io/api/' + self.api_version + '/'
        self._attr_path = []
        self._request_method = {
            'POST': requests.post,
            'GET': requests.get,
            'PUT': requests.put,
            'DELETE': requests.delete
        }

    def __call__(self, *args, **kwargs):
        url = self.base_url + '/'.join(self._attr_path)
        for variable_name, variable_sub in kwargs.get('variable', {}).items():
            url = re.sub(variable_name, variable_sub, url)
        self._attr_path = []
        return self._request(url,
                            kwargs.get('data', {}),
                            kwargs.get('method', 'GET'),
                            kwargs.get('params', {}))

    def __getattr__(self, attr, *args, **kwargs):
        self._attr_path.append(attr)
        return self

    def _request(self, endpoint, data, method='GET', params = None):
        headers = {'Content-Type': 'application/json'}
        params['apiKey'] = self.api_key
        if type(data) == dict:
            data = json.dumps(data)
        try:
            request = self._request_method[method]
        except KeyError as e:
            raise ReplyAppError(e.value)
        response = request(endpoint,
                           data=data,
                           params=params,
                           headers=headers)
        if response.status_code < 400:
            return response.json()
        else:
            response.raise_for_status()
