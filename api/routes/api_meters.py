
import json, logging, flask
import flask_restful as fr
import core.data.databaseOps as dbOps
from routes.api_flask import api_flask


class api_meters(fr.Resource):

   @staticmethod
   def get():
      try:
         jsonStr = "{\"Error\": \"MissingInput\"}"
         flags: object = flask.request.args.get("flags")
         if flags is None:
            return api_flask.jsonResp(jsonStr, 200)
         db: dbOps.databaseOps = dbOps.databaseOps()
         resObj = db.get_allMeters(int(str(flags)))
         # - - - -
         if resObj is not None:
            jsonStr = json.dumps(resObj)
         return api_flask.jsonResp(jsonStr, 200)
      except Exception as e:
         logging.error(e)
