

class configSQL(object):

   @staticmethod
   def upsert(tblname, dataDict: dict) -> str:
      qry = ""
      if tblname == "meters":
         dbid = int(dataDict["meter_dbid"])
         ctag = dataDict["circuit_tag"]
         qry = f"update config.meters set circuit_tag = '{ctag}' where meter_dbid = {dbid};"
      if tblname == "clients":
         dbid = dataDict["client_dbid"]
         tag = dataDict["client_tag"]
         name = dataDict["client_name"]
         if "default" in dbid:
            qry = f"insert into reports.clients values(default, '{tag}', '{name}');"
         else:
            qry = f"update reports.client set client_tag = '{tag}', client_name = '{name}' " \
               f" where client_dbid = {dbid};"
      # -- return qry --
      return qry

   @staticmethod
   def delete(tblname, dataDict: dict):
      qry = ""
      if tblname == "meters":
         dbid = int(dataDict["meter_dbid"])
         qry = f"delete from config.meters where meter_dbid = {dbid};"
      if tblname == "clients":
         dbid = int(dataDict["client_dbid"])
         qry = f"delete from reports.clients where client_dbid = {dbid};"
      # -- return qry --
      return qry
