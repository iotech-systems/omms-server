
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
         jsonBuff = db.get_allMeters()
         return flask.Response(jsonBuff, content_type=cType)
      except Exception as e:
         logging.error(e)
