
import logging
import flask, json
import flask_restful as fr
import core.data.databaseOps as dbOps
from routes.api_flask import api_flask


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class api_org(fr.Resource):

   @staticmethod
   def get():
      status = 400
      jsonStr = "{\"Error\": \"Unexpected\"}"
      try:
         db: dbOps.databaseOps = dbOps.databaseOps()
         status = 200
      except Exception as e:
         logging.error(e)
      finally:
         api_flask.jsonResp(jsonStr, status)
