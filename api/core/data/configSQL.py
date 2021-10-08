

class configSQL(object):

   @staticmethod
   def upsert(tblname, dataDict: dict) -> str:
      qry = ""
      # -- meters --
      if tblname == "meters":
         dbid = int(dataDict["meter_dbid"])
         ctag = dataDict["circuit_tag"]
         qry = f"update config.meters set circuit_tag = '{ctag}' where meter_dbid = {dbid};"
      # -- clients --
      if tblname == "clients":
         dbid = dataDict["client_dbid"]
         tag = dataDict["client_tag"]
         name = dataDict["client_name"]
         if "default" in dbid:
            qry = f"insert into reports.clients values(default, '{tag}', '{name}');"
         else:
            qry = f"update reports.client set client_tag = '{tag}', client_name = '{name}' " \
               f" where client_dbid = {dbid};"
      # -- circuits --
      if tblname == "circuits":
         dbid = dataDict["circuit_dbid"]
         tag = dataDict["circuit_tag"]
         entag = dataDict["entag"]
         amps = dataDict["max_amps"]
         volts = dataDict["voltage"]
         if "default" in dbid:
            qry = f"insert into config.circuits " \
               f" values(default, '{tag}', '{entag}', {amps}, {volts});"
         else:
            qry = f"update config.circuits set (circuit_tag, entag, max_amps, voltage)" \
               f" = ('{tag}', '{entag}', {amps}, {volts}) where circuit_dbid = {dbid};"
      # -- client_circuits --
      if tblname == "client_circuits":
         cir_tag: str = dataDict["circuit_tag"]
         clt_tag: str = dataDict["client_tag"]
         entag: str = dataDict["entag"]
         status: int = int(dataDict["status"])
         qry = f"insert into reports.client_circuits" \
            f" values('{clt_tag}', '{entag}', '{cir_tag}', {status}, now());"
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
      if tblname == "circuits":
         dbid = int(dataDict["circuit_dbid"])
         qry = f"delete from config.circuits where circuit_dbid = {dbid};"
      if tblname == "circuits":
         dbid = int(dataDict["circuit_dbid"])
         qry = f"delete from config.circuits where circuit_dbid = {dbid};"
      if tblname == "client_circuits":
         cir_tag = dataDict["circuit_tag"]
         clt_tag = dataDict["client_tag"]
         entag = dataDict["entag"]
         qry = f"delete from reports.client_circuits where circuit_tag = '{cir_tag}' and" \
            f" client_tag = '{clt_tag}' and entag = '{entag}';"
      # -- return qry --
      return qry
