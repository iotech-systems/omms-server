import json
import logging
import flask
import flask_restful as fr
import core.data.databaseOps as dbOps


class api_getMeters(fr.Resource):

   @staticmethod
   def get():
      try:
         cType = "application/json; charset=utf8"
         db: dbOps.databaseOps = dbOps.databaseOps()
         rowObj = db.get_allMeters()
         jsonStr = json.dumps(rowObj)
         return flask.Response(jsonStr, content_type=cType)
      except Exception as e:
         logging.error(e)
