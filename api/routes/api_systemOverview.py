
import json, flask
import flask_restful as fr
import core.data.databaseOps as dbOps
from routes.api_flask import api_flask


class api_sysOverview(fr.Resource):

   @staticmethod
   def get():
      try:
         jsonStr = ""
         hn: str = str(flask.request.args.get("hostname"))
         db: dbOps.databaseOps = dbOps.databaseOps()
         resObj = db.get_edgeLastPing(hn)
         if resObj is not None:
            jsonStr = json.dumps(resObj)
         return api_flask.jsonResp(jsonStr, 200)
      except Exception as e:
         print(e)
