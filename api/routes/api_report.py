
import logging
import codecs, flask, json
import flask_restful as fr
from sbmslib.shared.utils.jsonx import jsonx
import core.data.databaseOps as dbOps
import core.data.reportsSQL as repSQL
import core.data.sysReports as sysReps


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class api_report(fr.Resource):

   @staticmethod
   def get():
      status = 400
      jsonStr = "{\"Error\": \"MissingInput\"}"
      try:
         reportName: str = str(flask.request.args.get("repName"))
         # - - - - -
         if reportName == "meter-kwhrs":
            sr: sysReps.sysReports = sysReps.sysReports()
            jsonStr = sr.meter_kwhrs(flask.request)
         # - - - -
         elif reportName == "client-kwhrs":
            pass
         elif reportName == "place-holder":
            pass
         else:
            pass
         # - - - - -
         status = 200
      except Exception as e:
         logging.error(e)
         jsonStr = f'{"Error": "{e}"}'
      finally:
         return flask.Response(response=jsonStr, status=status
            , content_type="application/json")
