
import flask, json
from datetime import datetime
import flask_restful as fr
from ommslib.shared.misc import dtsFormats
from core.data.dbConfig import dbConfig
import psycopg2.extensions


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class api_dbinfo(fr.Resource):

   @staticmethod
   def get():
      jsonBuff = ""; buff = {}; dts = None; connStr = ""
      dbStatus = "closed"
      try:
         dts = datetime.utcnow().strftime(dtsFormats.std)
         connStr = open("config/dbconn.string", "r").read().strip()
         # - - - -
         conn: psycopg2.extensions.connection = dbConfig.getConnection()
         if conn is None:
            dbStatus = "connIsNone"
         if (conn is not None) and (conn.status == psycopg2.extensions.STATUS_READY):
            dbStatus = "ready"
            conn.close()
         # - - - -
      except Exception as e:
         buff["exception"] = str(e)
      finally:
         buff = {"SbmsRestApiServer": dts
            , "dbConnString": connStr
            , "dbStatus": dbStatus}
         jsonBuff = json.dumps(buff)
         return flask.Response(jsonBuff, content_type="application/json")
