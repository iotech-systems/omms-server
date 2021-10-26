
import logging
import codecs, flask, json
import flask_restful as fr
import core.data.databaseOps as dbOps
import core.data.sysReports as sysReps
from routes.api_flask import api_flask


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
            # /report?repName=client-kwhrs&cltTag=nip0011&sDate=2021-08-01&eDate=2021-08-30
            cltTag: str = str(flask.request.args.get("cltTag"))
            sdate: str = str(flask.request.args.get("sDate"))
            edate: str = str(flask.request.args.get("eDate"))
            db: dbOps.databaseOps = dbOps.databaseOps()
            rpt = db.run_report_client_kWhrs(cltTag, sdate, edate)
            jsonStr = json.dumps(rpt)
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
         return api_flask.jsonResp(jsonStr, status)
