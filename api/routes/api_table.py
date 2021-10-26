
import json
import logging, flask
import flask_restful as fr
import core.data.databaseOps as dbOps
from routes.api_flask import api_flask


class api_table(fr.Resource):

   @staticmethod
   def get():
      try:
         jsonStr = ""
         tbl: str = str(flask.request.args.get("tbl"))
         db: dbOps.databaseOps = dbOps.databaseOps()
         resObj = db.read_table(tbl)
         if resObj is not None:
            jsonStr = json.dumps(resObj)
         return api_flask.jsonResp(jsonStr, 200)
      except Exception as e:
         logging.error(e)
