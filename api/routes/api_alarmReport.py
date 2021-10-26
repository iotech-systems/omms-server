
import codecs
import flask_restful as fr
from sbmslib.shared.models.alarmReport import alarmReport
import core.data.databaseOps as dbOps
import core.services.emailBot as embot
import config.email as emConf


class api_alarmReport(fr.Resource):

   @staticmethod
   def put():
      try:
         # get request body; should be json string
         data = fr.request.data
         # json string
         jsonStr = codecs.decode(data, "UTF-8")
         print(f"\n >> {jsonStr}")
         report: alarmReport = alarmReport()
         report.fromJson(jsonStr)
         # send alarm email
         alarmStatus = api_alarmReport.trySendEmail(report)
         # save to database
         db = dbOps.databaseOps()
         val = db.save_Alarm(report, alarmStatus)
         # - - - - - - - - - - - - - - - - - -
         return {"val": val}
      except Exception as e:
         print(e)

   @staticmethod
   def trySendEmail(report: alarmReport) -> int:
      db = dbOps.databaseOps()
      yesOrNo: str = db.read_sendNewAlarmReport(report, emConf.emailConfig.emailIntervalMinutes)
      if yesOrNo.upper() == "NO":
         print("Not Sending Email Yet")
         return 1
      # - - - - - - - - - - - - - - - - - -
      bdy = f"\niotech - sbms - alarm\n\n{report.toJson()}"
      email = embot.emailBot("erik@iotech.systems", "office@iotech.systems",
         "SimpleBMS - Error Alarm", bdy)
      rval: int = 1
      if email.send():
         print("\tAlarm Email Sent")
         rval = 2
      # - - - - - - - - - - - - - -
      return rval
