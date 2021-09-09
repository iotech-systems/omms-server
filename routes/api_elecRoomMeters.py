
import json
import logging
import flask
import flask_restful as fr
import core.data.databaseOps as dbOps


class api_getElecRoomMeters(fr.Resource):

   @staticmethod
   def get():
      try:
         tag = flask.request.args.get("entityTag")
         jsonStr = ""
         cType = "application/json; charset=utf8"
         db: dbOps.databaseOps = dbOps.databaseOps()
         resObj = db.get_elecRoomMeters(tag)
         if resObj is not None:
            jsonStr = json.dumps(resObj)
         return flask.Response(jsonStr, content_type=cType)
      except Exception as e:
         logging.error(e)
