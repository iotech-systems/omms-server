
import psycopg2

CONN_STRING_FILE = "config/dbconn.string"


class dbConfig(object):

   @staticmethod
   def getConnection():
      try:
         # ignore all lines with #
         with open(CONN_STRING_FILE, "r") as file:
            lines = file.readlines()
         lns = [x for x in lines if not x.startswith("#")]
         if lns[0] in (None, ""):
            raise Exception("BadDatabaseConnectionString")
         # - - - -
         return psycopg2.connect(lns[0])
      except Exception as e:
         print(e)
