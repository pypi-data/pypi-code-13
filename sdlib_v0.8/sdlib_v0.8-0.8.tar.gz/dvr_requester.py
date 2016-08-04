import json

import requests

from dvr_logger import lager 


class DvrRequester(object):
  HOST = "https://api.buildingos.com/"

  def __init__(self, username, password, client_id, client_secret):
    self.bos_token= ""
    self.params = {
      "username": username,
      "password": password,
      "grant_type": "password",
      "client_secret": client_secret,
      "client_id": client_id
    }


  def _requester(self, url, headers=None, params=None, cookies=None):
    response = requests.get(url, params=params, headers=headers, cookies=cookies)

    try:
      response.raise_for_status()
    except requests.exceptions.HTTPError as e:
      lager.error("{} / on call {}".format(e, url))
      raise Exception("{} / Error making call on {}.".format(e, url))
 
    lager.warning("Recieved resoonse {} on call {}.".format(url, response))
    return response


  def post(self, url, params=None, data=None, headers=None):
    try:
      data = json.dumps(data)
    except ValueError:
      lager.info("No data arg passed.")
      
    response = requests.post(url, params=params, data=data, headers=headers)

    try:
      response.raise_for_status()
    except requests.exceptions.HTTPError as e:
      lager.error("{} / on call {}".format(e, url))
      raise Exception("{} / Error making call on {}.".format(e, url))

    return response
 

  def get_bos_token(self):
    response = self.post(self.HOST + "o/token/", params=self.params)

    try:
      content = response.json()
    except ValueError:
      return None

    self.bos_token = content["access_token"]
    lager.warning("Retrieved BOS token: {}.".format(self.bos_token))
    return self.bos_token


  def get(self, url):
    headers = {"Authorization" : "Bearer " + self.bos_token}
    lager.error("Here is the header {}.".format(headers))

    try:
      response = self._requester(url, headers=headers, params=None, cookies=None)
      return response
    except Exception as e:
      lager.error("{} / Accessing bos API.".format(e))
      self.get_bos_token()
      return self.get(url) 

