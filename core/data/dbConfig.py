
import psycopg2


CONN_STRING = "host=192.168.40.106 dbname=sbms_db user=sbms_admin password=abcd1234@@"


class dbConfig(object):

   @staticmethod
   def getConnection():
      try:
         return psycopg2.connect(CONN_STRING)
      except Exception as e:
         print(e)
