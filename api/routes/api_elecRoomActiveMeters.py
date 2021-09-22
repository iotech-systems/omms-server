
import json
import logging
import flask
import flask_restful as fr
import core.data.databaseOps as dbOps
from routes.api_flask import api_flask


class api_elecRoomActiveMeters(fr.Resource):

   @staticmethod
   def get():
      try:
         jsonStr = ""
         tag = flask.request.args.get("entag")
         db: dbOps.databaseOps = dbOps.databaseOps()
         jObj = db.get_elecRoomActiveMeters(tag)
         if jObj is not None:
            jsonStr = json.dumps(jObj)
         return api_flask.jsonResp(jsonStr, 200)
      except Exception as e:
         logging.error(e)
