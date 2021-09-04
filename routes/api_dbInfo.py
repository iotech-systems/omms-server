
import flask, json
from datetime import datetime
import flask_restful as fr
from sbmslib.shared.misc import dtsFormats
from core.data.dbConfig import dbConfig
import psycopg2.extensions


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class api_dbinfo(fr.Resource):

   @staticmethod
   def get():
      jsonBuff = ""; buff = {}
      try:
         dts = datetime.utcnow().strftime(dtsFormats.std)
         dbStatus = "closed"
         connStr = open("config/dbconn.string", "r").read().strip()
         # - - - -
         conn: psycopg2.extensions.connection = dbConfig.getConnection()
         if conn.status == psycopg2.extensions.STATUS_READY:
            dbStatus = "ready"
            conn.close()
         # - - - -
         buff = {"SbmsRestApiServer": dts
            , "dbConnString": connStr
            , "dbStatus": dbStatus}
         # - - - -
      except Exception as e:
         buff["exception"] = str(e)
      finally:
         jsonBuff = json.dumps(buff)
         return flask.Response(jsonBuff, content_type="text/json")
