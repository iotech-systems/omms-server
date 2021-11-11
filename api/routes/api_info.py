
import json
import flask_restful as fr
from datetime import datetime
from routes.api_flask import api_flask
from ommslib.shared.misc import dtsFormats


app: str = "omms-api"
ver: str = "0.1.0"


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class api_info(fr.Resource):

   @staticmethod
   def get():
      try:
         dts: str = datetime.utcnow().strftime(dtsFormats.stdUtc)
         jsonBuff: str = f"{{\"app\": \"{app}\", \"ver\": \"{ver}\", \"dts\": \"{dts}\"}}"
         return api_flask.jsonResp(jsonBuff, 200)
      except Exception as e:
         return {f"exception: {str(e)}"}


# -- test --
if __name__ == "__main__":
   buff = api_info.get()
   print(buff)
