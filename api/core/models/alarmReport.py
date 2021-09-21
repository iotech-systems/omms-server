
import utils.jsonUtils as ju

"""
   CREATE TABLE streams.alarms (
   alarm_dbid serial NOT NULL,
   fk_meter_dbid int4 NOT NULL,
   "level" varchar(16) NOT NULL,
   status int not null default 0,
   alarm_short_str varchar(32) not null,
   alarm_msg varchar(512) NOT NULL,
   dts timestamp NOT NULL DEFAULT now()); 
"""


class alarmReport(object):

   def __init__(self, jsonBuff: str):
      self.jsonBuff = str(jsonBuff)
      self.dbid: int = 0
      self.read_dts_utc: str = ""
      self.level: str = ""
      self.status: int = 0
      self.alarm_tag: str = ""
      self.alarm_msg: str = ""

   def load(self):
      try:
         jObj: dict = ju.jsonUtils.getJsonObj(self.jsonBuff)
         print(f"jObj: {jObj}")
         if not jObj["_type_"] == self.__class__.__name__:
            raise Exception(f"BadObjectType: {jObj['_type_']}")
         # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
         self.read_dts_utc: str = str(jObj["dtsUTC"])
         self.dbid = int(jObj["meterDBID"])
         self.level = str(jObj["level"])
         self.alarm_tag = str(jObj["alarm_tag"])
         self.alarm_msg = str(jObj["alarm_msg"])
      except Exception as e:
         print(e)
