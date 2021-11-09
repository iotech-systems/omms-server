
import psycopg2

CONN_STRING_FILE = "config/dbconn.string"


class dbConfig(object):

   @staticmethod
   def getConnection() -> [object, None]:
      try:
         # ignore all lines with #
         with open(CONN_STRING_FILE, "r") as file:
            lines = file.readlines()
         lns = [x for x in lines if not x.startswith("#")]
         if lns[0] in (None, ""):
            raise Exception("BadDatabaseConnectionString")
         # - - - -
         connStr = lns[0].strip()
         conn = psycopg2.connect(connStr)
         if conn is None:
            raise Exception(f"UnableToConnect: {connStr}")
         return conn
      except Exception as e:
         print(e)
         return None
