
from typing import List
import core.data.dbCore as dbCore
from sbmslib.shared.core.registerNames import registerNames as rn
from sbmslib.shared.models import alarmReport, kWhReport,\
   jsonPackageHead, kWhReading
from sbmslib.shared.utils.sysutils import sysutils


class databaseOps(object):

   def __init__(self):
      self.dbCore = dbCore.dbCore()

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
      row = db.run_query_fetch1(sel)
      if row is None:
         return "YES"
      return str(row[0]).upper()

   def save_ping(self, ip: str, hostName: str):
      ins = f"insert into diagnostics.edge_pings values ('{ip}', '{hostName}', default);"
      val = self.dbCore.run_insert(ins)
      qry = f"delete from diagnostics.edge_pings where ip = '{ip}' and" \
         f" age(timezone('utc', now()), dts_utc) > cast('06:00:00' as time);"
      self.dbCore.run_exec(qry)
      return val

   def save_streamer_put(self, jObj: dict):
      try:
         streamName = ""
         if "streamName" in jObj:
            streamName = jObj["streamName"]
         if streamName == "basicPwrStats":
            self.__save_basicPwrStats__(jObj)
         elif streamName == "kWhrs":
            self.__save_kwhrs__(jObj)
         else:
            return streamName
      except Exception as e:
         print(e)

   def __save_kwhrs__(self, jObj):
      # - - - - - - - -
      jph: jsonPackageHead.jsonPackageHead = jsonPackageHead.jsonPackageHead(jObj)
      dbid: int = self.__get_meterDBID__(jph)
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
         f"values({dbid}, cast('{jph.dtsUtc}' as timestamp), {total.regVal}, {l1.regVal}" \
         f", {l2.regVal}, {l3.regVal}, default);"
      # - - - - - - - -
      db: dbCore.dbCore = dbCore.dbCore()
      val = db.run_insert(ins)
      return val

   def __save_basicPwrStats__(self, jObj):
      # - - - - - - - - -
      jph: jsonPackageHead.jsonPackageHead = jsonPackageHead.jsonPackageHead(jObj)
      dbid: int = self.__get_meterDBID__(jph)
      # - - - - - - - -
      lst: List[kWhReading] = []
      readings: [] = jObj["readings"]
      for d in readings:
         lst.append(kWhReading.kWhReading(d))
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
      # - - - - - - - -
      ins = f"insert into streams.basic_pwr_stats" \
            f" values({dbid}, cast('{jph.dtsUtc}' as timestamp), {hz.regVal}, {lv.regVal}" \
            f", {l1_v.regVal}, {l2_v.regVal}, {l3_v.regVal}, {t_amps.regVal}, {l1_a.regVal}" \
            f", {l2_a.regVal}, {l3_a.regVal}, {t_act_pwr.regVal}, {l1_act_pwr.regVal}" \
            f", {l2_act_pwr.regVal}, {l3_act_pwr.regVal}, {t_pwr_f.regVal}, {l1_pwr_f.regVal}" \
            f", {l2_pwr_f.regVal}, {l3_pwr_f.regVal}, default);"
      # - - - - - - - -
      db: dbCore.dbCore = dbCore.dbCore()
      val = db.run_insert(ins)
      return val

   def __get_meterDBID__(self, jph: jsonPackageHead.jsonPackageHead) -> int:
      qry = f"select m.meter_dbid from config.meters m where m.edge_name = '{jph.edgeName}'" \
            f" and m.bus_type = '{jph.busType}' and bus_address = {jph.busAddress};"
      return int(self.dbCore.run_query_fetch1(qry)[0])