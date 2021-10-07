
import logging
from typing import List
import core.data.dbCore as dbCore
from sbmslib.shared.app_error_codes import appErrorCodes
from sbmslib.shared.core.registerNames import registerNames as rn
from sbmslib.shared.utils.sysutils import sysutils
from sbmslib.shared.models import alarmReport, kWhReport,\
   jsonPackageHead, kWhReading
from core.data.reportsSQL import reportsSQL as repSQL
from core.data.configSQL import configSQL as confSQL


logfile = "logs/dbops.log"
level = logging.WARNING


class databaseOps(object):

   def __init__(self):
      self.dbCore = dbCore.dbCore()
      logging.basicConfig(filename=logfile, level=level)
      self.meterNotFound = (appErrorCodes.METER_NOT_FOUND, appErrorCodes.METER_NOT_FOUND.name)

   def save_kWhRead(self, d: kWhReport.kWhReport):
      # - - - - - - - -
      ins = f"insert into streams.kwhrs " \
         f"values({d.meterDBID}, cast('{d.dtsUTC}' as timestamp), {d.total}, {d.l1}" \
         f", {d.l2}, {d.l3}, default);"
      # - - - - - - - -
      db: dbCore.dbCore = dbCore.dbCore()
      val = db.run_insert(ins)
      return val

   """
      insert into streams.alarms values(default, 1004, 'error', default
         , 'DeadPing', 'msg string', default);
   """
   def save_Alarm(self, d: alarmReport.alarmReport, status: int = 0):
      ins = f"insert into streams.alarms" \
         f" values(default, {d.meterDBID}, cast('{d.dtsUTC}' as timestamp)," \
         f" '{d.level}', {status}, '{d.alarm_tag}'," \
         f" '{d.alarm_msg}', default);"
      db: dbCore.dbCore = dbCore.dbCore()
      val = db.run_insert(ins)
      return val

   def read_sendNewAlarmReport(self, r: alarmReport.alarmReport, emailInternal: int = 20):
      emit = f"00:{emailInternal}:00"
      sel = f"select case when age(timezone('utc', now()), t.row_ins_dts) > cast('{emit}' as time) then 'yes'" \
         f" else 'no' end as SendNewEmail from streams.alarms t where t.fk_meter_dbid = {r.meterDBID}" \
         f" and t.\"level\" = '{r.level}' and t.alarm_tag = '{r.alarm_tag}' and status=2" \
         f" order by t.row_ins_dts desc limit 1;"
      db: dbCore.dbCore = dbCore.dbCore()
      scalar = db.run_qry_fetch_scalar(sel)
      if scalar is None:
         return "YES"
      return str(scalar).upper()

   def save_ping(self, ip: str, hostName: str):
      ins = f"insert into diagnostics.edge_pings values ('{ip}', '{hostName}', default);"
      val = self.dbCore.run_insert(ins)
      qry = f"delete from diagnostics.edge_pings where ip = '{ip}' and" \
         f" age(timezone('utc', now()), dts_utc) > cast('06:00:00' as time);"
      self.dbCore.run_exec(qry)
      return val

   def save_streamerPUT(self, jObj: dict) -> (appErrorCodes, str):
      try:
         streamName: str = ""
         if "streamName" in jObj:
            streamName = jObj["streamName"]
         if streamName == "basicPwrStats":
            res = self.__save_basicPwrStats__(jObj)
         elif streamName == "kWhrs":
            res = self.__save_kwhrs__(jObj)
         else:
            return 100, streamName
         # - - - - - -
         return res
      except Exception as e:
         print(e)

   def configTablePUT(self, tblname, dataDict: dict) -> int:
      qry = confSQL.upsert(tblname, dataDict)
      return self.dbCore.run_exec(qry)

   def configTableDELETE(self, tblname, dataDict: dict) -> int:
      qry = confSQL.delete(tblname, dataDict)
      return self.dbCore.run_exec(qry)

   def datalist(self, dl):
      qry = ""
      if dl == "elcrm-tags":
         qry = "select o.entity_dbid, o.entag, o.entity_desc" \
            " from config.org o where o.entity_type = 'electricalroom'"
      elif dl == "client-tags":
         qry = "select * from reports.clients"
      elif dl == "circuit-tags":
         qry = "select circuit_dbid, circuit_tag, entag from config.circuits"
      elif dl == "building-tags":
         qry = "select o.entity_dbid, o.entag , o.entity_desc desc" \
            " from config.org o where o.entity_type = 'building'"
      qry = self.__json_rows__(qry)
      # -- return jobj --
      return self.dbCore.run_qry_fetch_scalar(qry)

   """
      getters
   """

   def get_allSpaces(self, bTag=None) -> [object, False]:
      qry = f"select * from reports.spaces"
      if bTag not in (None, "None", ""):
         qry = f"select * from reports.spaces t where t.building_tag = '{bTag}'"
      qry = self.__json_rows__(qry)
      return self.dbCore.run_qry_fetch_scalar(qry)

   def get_allMeters(self, flags=0) -> [object, False]:
      if flags == 0:
         qry = "select array_to_json(array_agg(row_to_json(t))) from" \
            " (select m.meter_dbid, m.edge_name, m.bus_type, m.bus_address," \
            " m.meter_type, m.circuit_tag from config.meters m) t;"
      elif flags == 2:
         qry = "select array_to_json(array_agg(row_to_json(t))) from " \
            "(select m.* from config.meters m) t;"
      else:
         return ""
      # -- run query -> should be a db json type --
      return self.dbCore.run_qry_fetch_scalar(qry)

   def get_elecRoomMeters(self, tag: str) -> [object, False]:
      qry = f"select array_to_json(array_agg(row_to_json(t))) from" \
         f" (select m.meter_dbid, m.edge_name, m.bus_type, m.bus_address," \
         f" m.meter_type, m.circuit_tag, m.meter_maker, m.meter_model, c.max_amps," \
         f" c.voltage from config.meters m join config.circuits c on m.circuit_tag = c.circuit_tag" \
         f" where m.elcrm_entag = '{tag}') t;"
      # -- run query -> should be a db json type --
      return self.dbCore.run_qry_fetch_scalar(qry)

   def get_elecRoomActiveMeters(self, tag: str) -> [object, False]:
      qry = f"select distinct(bps.fk_meter_dbid) from streams.\"__basic_pwr_stats\" bps " \
         f" join streams.\"__kwhrs\" k on bps.fk_meter_dbid = k.fk_meter_dbid " \
         f" join config.meters m on m.meter_dbid = bps.fk_meter_dbid " \
         f" where m.elcrm_entag = '{tag}'"
      qry = self.__json_rows__(qry)
      # -- run query -> should be a db json type --
      return self.dbCore.run_qry_fetch_scalar(qry)

   def read_lastFromStreamTbl(self, streamTbl, meterDBID) -> [object, False]:
      qry = f"select row_to_json(t) from"\
         f" (select * from streams.{streamTbl} k where fk_meter_dbid = {meterDBID}" \
         f" order by reading_dts_utc desc limit 1) t;"
      # -- run query -> should be a db json type --
      return self.dbCore.run_qry_fetch_scalar(qry)

   def get_org(self):
      qry = "select array_to_json(array_agg(row_to_json(t)))" \
         " from (select o.* from config.org o) t;"
      # -- run query -> should be a db json type --
      return self.dbCore.run_qry_fetch_scalar(qry)

   def run_meter_kWhrsReport(self, qry) -> [object, None]:
      return self.dbCore.run_qry_fetch_scalar(qry)

   def run_report_client_kWhrs(self, cltTag: str, sdate: str, edate: str):
      rows = []
      cltMeters: [] = self.__get_client_meters__(cltTag)
      for m in cltMeters:
         dbid, busAdr, mType, cirTag = m
         qry = repSQL.meter_kwhrs(int(dbid), sdate, edate)
         row = self.dbCore.run_query_fetchone(qry)
         rows.append(row)
      return rows

   def get_allClients(self):
      sel = "select * from reports.clients c order by c.client_name asc"
      qry = self.__json_rows__(sel)
      return self.dbCore.run_qry_fetch_scalar(qry)

   def get_allCircuits(self):
      sel = "select * from config.circuits c order by c.entag asc"
      qry = self.__json_rows__(sel)
      return self.dbCore.run_qry_fetch_scalar(qry)

   def get_cltCircuits(self):
      sel = "select c.client_name, cc.* from reports.client_circuits cc" \
         " join reports.clients c on cc.client_tag = c.client_tag " \
         " order by cc.client_tag asc"
      qry = self.__json_rows__(sel)
      return self.dbCore.run_qry_fetch_scalar(qry)

   def get_histogramData(self, meterDBID: int):
      qry = f"select * from streams.\"__basic_pwr_stats\" t" \
         f" where t.fk_meter_dbid = {meterDBID} order by t.reading_dts_utc desc limit 60"
      qry = self.__json_rows__(qry)
      return self.dbCore.run_qry_fetch_scalar(qry)

   def get_tableInfo(self, tableName):
      qry = f"select column_name colname, data_type dtype, character_maximum_length maxlen," \
         f" column_default coldef, is_nullable nullok, ordinal_position" \
         f" from INFORMATION_SCHEMA.COLUMNS" \
         f" where table_name = '{tableName}'"
      # -- update query --
      qry = self.__json_rows__(qry)
      return self.dbCore.run_qry_fetch_scalar(qry)

   def __save_kwhrs__(self, jObj) -> (int, str):
      # - - - - - - - -
      jph: jsonPackageHead.jsonPackageHead = jsonPackageHead.jsonPackageHead(jObj)
      dbid: int = self.__get_meterDBID__(jph)
      if dbid == 0:
         return appErrorCodes.METER_NOT_FOUND, None
      # -- get frame read time --
      readTimeSecs = 0.0
      if "readTimeSecs" in jObj:
         readTimeSecs: float = float(jObj["readTimeSecs"])
      # - - - - - - - -
      lst: List[kWhReading] = []
      readings: [] = jObj["readings"]
      for d in readings:
         lst.append(kWhReading.kWhReading(d))
      # - - - - - - - -
      total: kWhReading.kWhReading = sysutils.findRegister(lst, rn.TotalActiveEnergy)
      l1: kWhReading.kWhReading = sysutils.findRegister(lst, rn.L1_TotalActiveEnergy)
      l2: kWhReading.kWhReading = sysutils.findRegister(lst, rn.L2_TotalActiveEnergy)
      l3: kWhReading.kWhReading = sysutils.findRegister(lst, rn.L3_TotalActiveEnergy)
      # - - - - - - - -
      ins = f"insert into streams.kwhrs " \
         f"values({dbid}, cast('{jph.dtsUtc}' as timestamp), {readTimeSecs}, {total.regVal}," \
         f" {l1.regVal}, {l2.regVal}, {l3.regVal}, default);"
      # - - - - - - - -
      db: dbCore.dbCore = dbCore.dbCore()
      rowcount = db.run_insert(ins)
      # - - - - - - - -
      if rowcount == 1:
         ttlHrs = 2
         tblName = "__kwhrs"
         ins = f"insert into streams.{tblName}" \
            f" values({dbid}, cast('{jph.dtsUtc}' as timestamp), {readTimeSecs}, {total.regVal}," \
            f" {l1.regVal}, {l2.regVal}, {l3.regVal}, default);"
         # - - - - - - - -
         # db: dbCore.dbCore = dbCore.dbCore()
         val = db.run_insert(ins)
         self.__clear_live_tbl(tblName, ttlHrs)
      # - - - - - - - -
      error = appErrorCodes.BAD_DB_INSERT
      if rowcount == 1:
         error = appErrorCodes.OK
      return error, None

   def __save_basicPwrStats__(self, jObj) -> (appErrorCodes, str):
      # - - - - - - - -
      jph: jsonPackageHead.jsonPackageHead = jsonPackageHead.jsonPackageHead(jObj)
      dbid: int = self.__get_meterDBID__(jph)
      if dbid == 0:  # dbid 0 means meter not found
         return appErrorCodes.METER_NOT_FOUND, None
      # - - - - - - - -
      lst: List[kWhReading] = []
      readings: [] = jObj["readings"]
      for d in readings:
         lst.append(kWhReading.kWhReading(d))
      # -- get frame read time --
      readTimeSecs = 0.0
      if "readTimeSecs" in jObj:
         readTimeSecs: float = float(jObj["readTimeSecs"])
      # - - - - - - - - -
      hz: kWhReading.kWhReading = sysutils.findRegister(lst, rn.GridFreqHz)
      # voltage
      lv: kWhReading.kWhReading = sysutils.findRegister(lst, rn.LineVoltage)
      l1_v: kWhReading.kWhReading = sysutils.findRegister(lst, rn.L1_Voltage)
      l2_v: kWhReading.kWhReading = sysutils.findRegister(lst, rn.L2_Voltage)
      l3_v: kWhReading.kWhReading = sysutils.findRegister(lst, rn.L3_Voltage)
      # current
      t_amps: kWhReading.kWhReading = sysutils.findRegister(lst, rn.TotalAmps)
      l1_a: kWhReading.kWhReading = sysutils.findRegister(lst, rn.L1_Amps)
      l2_a: kWhReading.kWhReading = sysutils.findRegister(lst, rn.L2_Amps)
      l3_a: kWhReading.kWhReading = sysutils.findRegister(lst, rn.L3_Amps)
      # active power
      t_act_pwr: kWhReading.kWhReading = sysutils.findRegister(lst, rn.TotalActivePower)
      l1_act_pwr: kWhReading.kWhReading = sysutils.findRegister(lst, rn.L1_ActivePower)
      l2_act_pwr: kWhReading.kWhReading = sysutils.findRegister(lst, rn.L2_ActivePower)
      l3_act_pwr: kWhReading.kWhReading = sysutils.findRegister(lst, rn.L3_ActivePower)
      # reactive power
      t_pwr_f: kWhReading.kWhReading = sysutils.findRegister(lst, rn.TotalPowerFactor)
      l1_pwr_f: kWhReading.kWhReading = sysutils.findRegister(lst, rn.L1_PowerFactor)
      l2_pwr_f: kWhReading.kWhReading = sysutils.findRegister(lst, rn.L2_PowerFactor)
      l3_pwr_f: kWhReading.kWhReading = sysutils.findRegister(lst, rn.L3_PowerFactor)
      # - - insert into long term table - -
      ins = f"insert into streams.basic_pwr_stats" \
         f" values({dbid}, cast('{jph.dtsUtc}' as timestamp), {readTimeSecs}, {hz.regVal}, {lv.regVal}" \
         f", {l1_v.regVal}, {l2_v.regVal}, {l3_v.regVal}, {t_amps.regVal}, {l1_a.regVal}" \
         f", {l2_a.regVal}, {l3_a.regVal}, {t_act_pwr.regVal}, {l1_act_pwr.regVal}" \
         f", {l2_act_pwr.regVal}, {l3_act_pwr.regVal}, {t_pwr_f.regVal}, {l1_pwr_f.regVal}" \
         f", {l2_pwr_f.regVal}, {l3_pwr_f.regVal}, default);"
      # - - - - - - - -
      db: dbCore.dbCore = dbCore.dbCore()
      rowcount = db.run_insert(ins)
      # - - insert into live table - -
      if rowcount == 1:
         ttlHrs = 2
         tblName = "__basic_pwr_stats"
         ins = f"insert into streams.{tblName}" \
            f" values({dbid}, cast('{jph.dtsUtc}' as timestamp), {readTimeSecs}, {hz.regVal}, {lv.regVal}" \
            f", {l1_v.regVal}, {l2_v.regVal}, {l3_v.regVal}, {t_amps.regVal}, {l1_a.regVal}" \
            f", {l2_a.regVal}, {l3_a.regVal}, {t_act_pwr.regVal}, {l1_act_pwr.regVal}" \
            f", {l2_act_pwr.regVal}, {l3_act_pwr.regVal}, {t_pwr_f.regVal}, {l1_pwr_f.regVal}" \
            f", {l2_pwr_f.regVal}, {l3_pwr_f.regVal}, default);"
         # - - best try - -
         db.run_insert(ins)
         self.__clear_live_tbl(tblName, ttlHrs)
      # - - - - - - - - -
      error = appErrorCodes.BAD_DB_INSERT
      if rowcount == 1:
         error = appErrorCodes.OK
      return error, None

   def __get_meterDBID__(self, jph: jsonPackageHead.jsonPackageHead) -> int:
      qry = f"select m.meter_dbid from config.meters m where m.edge_name = '{jph.edgeName}'" \
            f" and m.bus_type = '{jph.busType}' and bus_address = {jph.busAddress};"
      dbid = self.dbCore.run_qry_fetch_scalar(qry)
      if dbid is None:
         # logging.warning(f"dbid not found! qry: {qry};")
         # reset dbid to zero as not found!
         dbid = 0
      else:
         dbid = int(dbid)
      # return dbid of the meter
      return dbid

   def __clear_live_tbl(self, tblName: str, ageHrs: int):
      try:
         # - - try table name - -
         if not tblName.startswith("__"):
            raise Exception(f"BadTableName: {tblName}")
         # - - - - - -
         qry = f"delete from streams.{tblName} where" \
            f" (date_part('hour', timezone('utc', now())) - " \
            f" date_part('hour', reading_dts_utc)) > {ageHrs};"
         self.dbCore.run_exec(qry)
      except Exception as e:
         print(e)

   def __json_rows__(self, qry: str):
      return f"select array_to_json(array_agg(row_to_json(t)))" \
         f" from ({qry}) t;"

   def __json_row__(self, qry: str):
      return f"select row_to_json(t) from ({qry}) t;"

   def __get_client_meters__(self, cltTag: str) -> []:
      qry = f"select m.meter_dbid, m.bus_address, m.meter_type, m.circuit_tag from config.meters m" \
         f" join reports.client_circuits cc on m.circuit_tag = cc.circuit_tag" \
         f" where cc.client_tag = '{cltTag}';"
      rows = self.dbCore.run_query(qry)
      return rows
