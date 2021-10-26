
import json
import logging, flask
import flask_restful as fr
import core.data.databaseOps as dbOps
from routes.api_flask import api_flask


class api_getSpaces(fr.Resource):

   @staticmethod
   def get():
      try:
         jsonStr = ""
         buildingTag: str = str(flask.request.args.get("buildingTag"))
         db: dbOps.databaseOps = dbOps.databaseOps()
         resObj = db.get_allSpaces(buildingTag)
         if resObj is not None:
            jsonStr = json.dumps(resObj)
         return api_flask.jsonResp(jsonStr, 200)
      except Exception as e:
         logging.error(e)
