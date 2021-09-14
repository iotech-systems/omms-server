
import psycopg2
import core.data.dbConfig as dbConfig


class dbCore(object):

   def __init__(self):
      self.conn = dbConfig.dbConfig.getConnection()

   def run_query(self, query: str):
      try:
         with self.conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
         return rows
      except Exception as e:
         print(e)

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

   def run_qry_fetch_scalar(self, sel: str) -> [object, None]:
      try:
         with self.conn.cursor() as cur:
            cur.execute(sel)
            """ Fetch the next row of a query result set, returning a single tuple, 
               or None when no more data is available: """
            row = cur.fetchone()
         # - - - -
         if len(row) > 0:
            return row[0]
         else:
            return None
      except Exception as e:
         print(e)
