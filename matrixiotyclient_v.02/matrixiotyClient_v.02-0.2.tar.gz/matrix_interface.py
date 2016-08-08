import logging 
import json
import logging
import requests
from urllib import quote 


class MatrixClient(object):

  LOGIN_TYPE = "m.login.password"
  MATRIX_API_PATH = "/_matrix/client/api/v1"
  MESSAGE_TYPE = "m.text" 
  MESSAGE_EVENT = "m.room.message"

  def __init__(self, host, username, password):
    self.host = host
    self.username = username 
    self.password = password
    self.listener = []
    self.headers = {}
    self.token = None
    self.current_room = None
    self.params = {"access_token": None} 
    self.rooms = {
            # room_id: Room
        }
    self.verify_cert = True
    self.limit = 1
    self.message_id = 0  


  def _matrix_requester(self, method, url, content=None):
    response = requests.request(
      method, 
      url,
      data=json.dumps(content),
      params = self.params,
      headers=self.headers,
      verify=self.verify_cert
    ) 

    try:
      response.raise_for_status()
    except requests.exceptions.HTTPError as e:
      raise Exception("Invalid response recieved from Matrix server{}.".format(e))
    
    return response.json() 


  def _sync_to_server(self, limit=1):
    '''Sync occurs after user has logged in. 
       Rooms, room ids, state, and messages are synced.'''
    method = "GET"
    sync_url = self.host + self.MATRIX_API_PATH + "/initialSync"
    self.limit = limit 
    self.params["access_token"] = self.token
    self.params["limit"] = self.limit
    response_payload = self._matrix_requester(method, sync_url)
    return response_payload


  def login(self):
    content = {
      "type": self.LOGIN_TYPE,
      "user": self.username,
      "password": self.password
    }
    login_url = self.host + self.MATRIX_API_PATH + "/login"
    self.headers["Content-Type"] = "application/json"
    response_payload = self._matrix_requester("POST", login_url, content)  
    self.token = response_payload["access_token"]
    synced_data = self._sync_to_server()
    return response_payload


  def join_room(self, room_name_and_host): 
    if room_name_and_host:
      join_room_path = "/join/%s" % quote(room_name_and_host)
      join_room_url = self.host + self.MATRIX_API_PATH + join_room_path
      response_payload = self._matrix_requester("POST", join_room_url)     
      return response_payload
    else:
      raise Exception("Please proved a room id.")

  def send_message(self, message, message_id=None, room=None):
    if not room and not self.current_room:
      raise Exception ("Please enter a room to join.")

    elif room:
      self.current_room = room

    method = "PUT"
    join_room_payload = self.join_room(self.current_room)
    room_id = join_room_payload["room_id"]
    message = {
      "msgtype": self.MESSAGE_TYPE,
      "body": message
    }

    if not message_id:
      self.message_id += 1
    else: 
      self.message_id = message_id 
 
    path = "/rooms/%s/send/%s/%s" % (
        quote(room_id),
        quote(self.MESSAGE_EVENT), 
        quote(str(self.message_id)))
    
    message_url = self.host + self.MATRIX_API_PATH + path 
    response_payload = self._matrix_requester(method, message_url, message)
    return response_payload
