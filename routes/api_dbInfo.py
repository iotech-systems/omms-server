
import flask, json
from datetime import datetime
import flask_restful as fr
from sbmslib.shared.misc import dtsFormats


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class api_dbinfo(fr.Resource):

   @staticmethod
   def get():
      try:
         dts = datetime.utcnow().strftime(dtsFormats.std)
         connStr = open("config/dbconn.string", "r").read().strip()
         buff = {"SbmsRestApiServer": dts,
               "dbConnString": connStr}
         # - - - -
         jsonBuff = json.dumps(buff)
         return flask.Response(jsonBuff, content_type="text/json")
      except Exception as e:
         return {f"exception: {str(e)}"}
