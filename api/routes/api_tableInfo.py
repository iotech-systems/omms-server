
import json
import logging, flask
import flask_restful as fr
import core.data.databaseOps as dbOps
from routes.api_flask import api_flask


TBLS = {"0x00": "clients", "0x02": "circuits", "0x04": "meters", "0x06": "spaces"
        , "0x08": "client_circuits", "0x10": "client_spaces"}


class api_tableInfo(fr.Resource):

   @staticmethod
   def get():
      try:
         jsonStr = ""
         IDX: str = str(flask.request.args.get("tblidx"))
         tableName = TBLS[IDX]
         db: dbOps.databaseOps = dbOps.databaseOps()
         resObj = db.get_tableInfo(tableName)
         if resObj is not None:
            jsonStr = json.dumps(resObj)
         return api_flask.jsonResp(jsonStr, 200)
      except Exception as e:
         logging.error(e)
