
import json


class jsonUtils(object):

   @staticmethod
   def getJsonObj(jsonBuff: str) -> dict:
      jObj = json.loads(jsonBuff)
      if isinstance(jObj, str):
         jObj = json.loads(jObj)
      if isinstance(jObj, str):
         raise Exception(f"json.lads: bad input string:\n\t {jObj}")
      # - - -
      return jObj
