
import codecs
import flask_restful as fr
from sbmslib.shared.models import kWhReport
import core.data.databaseOps as dbOps


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class api_kWhReport(fr.Resource):

   @staticmethod
   def put():
      try:
         # get request body; should be json string
         data = fr.request.data
         # json string
         jsonStr = codecs.decode(data, "UTF-8")
         # create model
         report: kWhReport.kWhReport = kWhReport.kWhReport()
         report.fromJson(jsonStr)
         # save to database
         db = dbOps.databaseOps()
         val = db.save_kWhRead(report)
         # - - - - - - - - - - - - - - - - - -
         return {"val": val}
      except Exception as e:
         return {f"exception: {str(e)}"}

   @staticmethod
   def help():
      return "help file:"
