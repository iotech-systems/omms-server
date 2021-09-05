
import logging
import flask_restful as fr
from flask import Response
from datetime import datetime
from sbmslib.shared.misc import dtsFormats
import core.data.databaseOps as dbOps


class api_getMeters(fr.Resource):

   @staticmethod
   def get():
      try:
         db: dbOps.databaseOps = dbOps.databaseOps()
         jsonBuff = db.get_allMeters()
         return Response(jsonBuff, content_type="application/json")
      except Exception as e:
         logging.error(e)
