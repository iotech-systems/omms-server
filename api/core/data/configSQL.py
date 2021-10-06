

class configSQL(object):

   @staticmethod
   def upsert(tblname, dataDict: dict) -> str:
      qry = ""
      if tblname == "meters":
         dbid = int(dataDict["meter_dbid"])
         ctag = dataDict["circuit_tag"]
         qry = f"update config.meters set circuit_tag = '{ctag}' where meter_dbid = {dbid};"
      # -- return qry --
      return qry
