
import json, logging, flask
import flask_restful as fr
import core.data.databaseOps as dbOps
from routes.api_flask import api_flask


class api_getMeters(fr.Resource):

   @staticmethod
   def get():
      try:
         jsonStr = ""
         flags: int = int(flask.request.args.get("flags"))
         db: dbOps.databaseOps = dbOps.databaseOps()
         resObj = db.get_allMeters(flags)
         # - - - -
         if resObj is not None:
            jsonStr = json.dumps(resObj)
         return api_flask.jsonResp(jsonStr, 200)
      except Exception as e:
         logging.error(e)
