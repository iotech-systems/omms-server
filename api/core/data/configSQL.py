

class configSQL(object):

   @staticmethod
   def upsert(tblname, dataDict: dict) -> [str, None]:
      if tblname == "meters":
         return configSQL.__meters__(dataDict)
      elif tblname == "clients":
         return configSQL.__clients__(dataDict)
      elif tblname == "circuits":
         return configSQL.__circuits__(dataDict)
      elif tblname == "client_space_circuits":
         return configSQL.__client_space_circuits__(dataDict)
      elif tblname == "spaces":
         return configSQL.__spaces__(dataDict)
      else:
         return None

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
         cir_tag: str = dataDict["circuit_tag"]
         clt_tag = dataDict["client_tag"]
         entag = dataDict["entag"]
         qry = f"delete from reports.client_circuits where circuit_tag = '{cir_tag}' and" \
            f" client_tag = '{clt_tag}' and entag = '{entag}';"
      if tblname == "spaces":
         dbid = dataDict["space_dbid"]
         qry = f"delete from reports.spaces where space_dbid = {dbid};"
      # -- return qry --
      return qry

   @staticmethod
   def activeElectricMeters(elcRoomTag: str):
      # return f"select distinct(bps.fk_meter_dbid) from streams.\"__basic_pwr_stats\" bps " \
      #    f" join streams.\"__kwhrs\" k on bps.fk_meter_dbid = k.fk_meter_dbid " \
      #    f" join config.meters m on m.meter_dbid = bps.fk_meter_dbid " \
      #    f" where m.elcrm_entag = '{elcRoomTag}'"
      return f"select distinct(am.fk_meter_dbid) from \"diagnostics\".active_meters am"\
         f" join config.meters m  on m.meter_dbid = am.fk_meter_dbid"\
         f" where m.elcrm_entag  = '{elcRoomTag}';"

   @staticmethod
   def __meters__(dataDict: []):
      dbid = dataDict["meter_dbid"]
      ctag = dataDict["circuit_tag"]
      return f"update config.meters set circuit_tag = '{ctag}' where meter_dbid = {dbid};"

   @staticmethod
   def __clients__(dataDict: []):
      dbid = dataDict["client_dbid"]
      tag = dataDict["client_tag"]
      name = dataDict["client_name"]
      if "::default" in dbid:
         qry = f"insert into reports.clients values(default, '{tag}', '{name}');"
      else:
         qry = f"update reports.clients set (client_tag, client_name)" \
            f" = ('{tag}', '{name}') where client_dbid = {dbid};"
      # -- return --
      return qry

   @staticmethod
   def __circuits__(dataDict: []):
      dbid = dataDict["circuit_dbid"]
      tag = dataDict["circuit_tag"]
      entag = dataDict["entag"]
      amps = dataDict["max_amps"]
      volts = dataDict["voltage"]
      if "::default" in dbid:
         qry = f"insert into config.circuits " \
               f" values(default, '{tag}', '{entag}', {amps}, {volts});"
      else:
         qry = f"update config.circuits set (circuit_tag, entag, max_amps, voltage)" \
               f" = ('{tag}', '{entag}', {amps}, {volts}) where circuit_dbid = {dbid};"
      # -- return --
      return qry

   @staticmethod
   def __client_space_circuits__(dataDict: []):
      NotSet = 999
      dbid: str = dataDict["csc_dbid"]
      clt_tag: str = dataDict["client_tag"]
      entag: str = dataDict["entag"]
      spa_tag: str = dataDict["space_tag"]
      cir_tag: str = dataDict["circuit_tag"]
      tmp = dataDict["bitflag"]
      if tmp == "":
         tmp = NotSet
      bitflag: int = int(tmp)
      if "::default" in dbid:
         qry = f"insert into reports.client_space_circuits" \
            f" (client_tag, entag, space_tag, circuit_tag, bitflag)" \
            f" values('{clt_tag}', '{entag}', '{spa_tag}', '{cir_tag}', {bitflag});"
      else:
         qry = f"update reports.client_space_circuits" \
            f" set (client_tag, entag, space_tag, circuit_tag, bitflag)" \
            f" = ('{clt_tag}', '{entag}', '{spa_tag}', '{cir_tag}', {bitflag})" \
            f" where csc_dbid = {dbid};"
      # -- return --
      return qry

   @staticmethod
   def __spaces__(dataDict: []):
      dbid: str = dataDict["space_dbid"]
      bld_tag: str = dataDict["building_entag"]
      spc_tag: str = dataDict["space_tag"]
      # -- space area --
      tmp: str = dataDict["area_m2"]
      if tmp in [None, ""]:
         area_m2 = None
      else:
         area_m2 = float(dataDict["area_m2"])
      # -- floor --
      tmp = dataDict["floor"]
      if "::" in tmp:
         floor = int(tmp.split("::")[0].strip())
      else:
         floor = int(tmp)
      # -- build qry --
      if "::default" in dbid:
         qry = f"insert into reports.spaces (building_entag, space_tag, area_m2, floor)" \
               f" values('{bld_tag}', '{spc_tag}', {area_m2}, {floor});"
      else:
         qry = f"update reports.spaces set (building_entag, space_tag, area_m2, floor) =" \
               f" ('{bld_tag}', '{spc_tag}', {area_m2}, {floor}) where space_dbid = {dbid};"
      # -- return --
      return qry


"""
   dbid = dataDict["meter_dbid"]
         ctag = dataDict["circuit_tag"]
         qry = f"update config.meters set circuit_tag = '{ctag}' where meter_dbid = {dbid};"
         
"""