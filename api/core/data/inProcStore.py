
class inProcStore(object):

   __store__: dict = {}

   @staticmethod
   def clear():
      inProcStore.__store__.clear()

   @staticmethod
   def addKeyVal(key: str, obj: object) -> bool:
      if key in inProcStore.__store__.keys():
         return False
      inProcStore.__store__[key] = obj
      return True
