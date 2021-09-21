
from datetime import datetime
import flask_restful as fr
from sbmslib.shared.misc import dtsFormats


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class api_info(fr.Resource):

   @staticmethod
   def get():
      try:
         dts = datetime.utcnow().strftime(dtsFormats.std)
         buff = f"sbms-rest-api-server: {dts}"
         return buff
      except Exception as e:
         return {f"exception: {str(e)}"}
