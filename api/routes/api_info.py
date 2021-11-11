import json
from datetime import datetime
import flask_restful as fr
from routes.api_flask import api_flask
from ommslib.shared.misc import dtsFormats

app = "omms-api"
ver = "0.1.0"


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class api_info(fr.Resource):

   @staticmethod
   def get():
      try:
         dts = datetime.utcnow().strftime(dtsFormats.stdUtc)
         out = {"app": app, "ver": ver, "dts": dts}
         return api_flask.jsonResp(json.dumps(out), 200)
      except Exception as e:
         return {f"exception: {str(e)}"}
