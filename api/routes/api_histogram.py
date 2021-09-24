
import logging
import flask, json
import flask_restful as fr
import core.data.databaseOps as dbOps
from routes.api_flask import api_flask


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class api_histogram(fr.Resource):

   @staticmethod
   def get():
      status = 400
      jsonStr = "{\"Error\": \"Unexpected\"}"
      try:
         meterDBID = flask.request.args.get("mid")
         db: dbOps.databaseOps = dbOps.databaseOps()
         rows = db.get_histogramData(int(meterDBID))
         data = {"streamTbl": "__histogram", "rows": rows}
         jsonStr = json.dumps(data)
         status = 200
      except Exception as e:
         logging.error(e)
      finally:
         return api_flask.jsonResp(jsonStr, status)