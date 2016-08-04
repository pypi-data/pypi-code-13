import uuid

from pymongo import MongoClient
from pymongo import errors


import dvr_logger

class DvrMache(object):

  HOST = "mongo"
  PORT = 27017
  DATABASE = "sd_cache"
  COLLECTION = "data"


  def connect(self):
    dvr_logger.lager.info("Attempting to connect to {} on {}.".format(self.HOST, self.PORT))
    try:
      client = MongoClient(host=self.HOST, port=self.PORT)
    except errors.ConnectionFailure as me:
      raise Exception("Error connecting to Dache.")

    db = client["sd_cache"]
    return db


  def _change_record(self, cmd, data, key, Id):
    db = self.connect()
    col = db["data"]

    try:
      result = col.update_one({"_id": Id},{cmd: {key: data}}, upsert=True)
    except Exception as pe:
      raise Exception("{} / {} {} - ID: {}/LOC: {}.".format(pe, cmd, data, Id, key))

    dvr_logger.lager.info("Updated {} - ID: {}/LOC: {}.".format(data, Id, key))
    return Id


  def add(self, data, key, Id):
    Id = self._change_record("$push", data, key, Id)
    return Id



  def put(self, data, key):
    Id = str(uuid.uuid4())
    Id = self._change_record("$set", data, key, Id)
    return Id


  def get(self, Id):
    db = self.connect()
    try:
      result = db["data"].find_one({"_id": Id})
    except errors.PyMongoError as pe:  
      raise Exception("{} / Finding {}".format(pe, Id))

    dvr_logger.lager.info("Retrieved data with Id = {}".format(Id))
    return result 


  def delete(self):
    db = self.connect()
    dvr_logger.lager.info("Deleting collection.")
    db["data"].drop()
    return True

