import json
from urllib.parse import urlencode

from tornado.httpclient import AsyncHTTPClient
from tornado.httpclient import HTTPError


async def get_user(user_id, *, base_url, service_name, service_secret):
    client = AsyncHTTPClient()

    credientials = {
        'service-name': service_name,
        'service-secret': service_secret}

    query = urlencode({'id': user_id})
    url   = '{base_url}/get_user'.format(base_url=base_url)

    try:
        response = await client.fetch(
            url,
            method='POST',
            headers=credientials,
            body=query)
    except HTTPError:
        raise
    else:
        return json.loads(response.body.decode('utf-8'))['result']
