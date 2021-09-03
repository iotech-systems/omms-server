
import utils.jsonUtils as ju


class kWhReport(object):

   # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
   def __init__(self, jsonBuff):
      self._type_ = "kWhRead"
      self.jsonBuff = str(jsonBuff)
      self.dbid: int = 0
      self.read_dts_utc: str = ""
      self.total: float = 0.0
      self.l1: float = 0.0
      self.l2: float = 0.0
      self.l3: float = 0.0

   # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
   def load(self):
      try:
         jObj: dict = ju.jsonUtils.getJsonObj(self.jsonBuff)
         print(f"jObj: {jObj}")
         if not jObj["_type_"] == self.__class__.__name__:
            raise Exception(f"BadObjectType: {jObj['_type_']}")
         # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
         self.dbid: int = int(jObj["meterDBID"])
         self.read_dts_utc: str = str(jObj["dtsUTC"])
         self.total: float = float(jObj["total"])
         self.l1: float = float(jObj["l1"])
         self.l2: float = float(jObj["l2"])
         self.l3: float = float(jObj["l3"])
      except Exception as e:
         print(e)

   # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
   def dump(self):
      print(self.__dir__())
