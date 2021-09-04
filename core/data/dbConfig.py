
import psycopg2


# CONN_STRING = "host=192.168.40.106 dbname=sbms_db user=sbms_admin password=abcd1234@@"
CONN_STRING_FILE = "config/dbconn.string"


class dbConfig(object):

   @staticmethod
   def getConnection():
      try:
         with open(CONN_STRING_FILE, "r") as file:
            CONN_STRING = file.read().strip()
         if CONN_STRING is (None, ""):
            raise Exception("BadDatabaseConnectionString")
         # - - - -
         return psycopg2.connect(CONN_STRING)
      except Exception as e:
         print(e)
