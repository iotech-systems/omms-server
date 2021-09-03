
import psycopg2
import core.data.dbConfig as dbConfig


class dbCore(object):

   def __init__(self):
      self.conn = dbConfig.dbConfig.getConnection()

   def run_query(self, query: str):
      pass

   def run_insert(self, ins: str):
      try:
         print(ins)
         with self.conn.cursor() as cur:
            cur.execute(ins)
            rowCnt = cur.rowcount
            self.conn.commit()
         print(rowCnt)
         return rowCnt
      except Exception as e:
         print(e)

   def run_exec(self, qry: str):
      try:
         with self.conn.cursor() as cur:
            cur.execute(qry)
            rowCnt = cur.rowcount
            self.conn.commit()
         return rowCnt
      except Exception as e:
         print(e)

   def run_query_fetch1(self, sel: str):
      try:
         with self.conn.cursor() as cur:
            cur.execute(sel)
            row = cur.fetchone()
         # - - - -
         return row
      except Exception as e:
         print(e)
