
import codecs
import flask_restful as fr
from sbmslib.shared.utils.jsonx import jsonx
import core.data.databaseOps as dbOps


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class api_streamer(fr.Resource):

   @staticmethod
   def put():
      try:
         # get request body; should be json string
         data = fr.request.data
         # json string
         jsonStr = codecs.decode(data, "UTF-8")
         # create model
         jObj = jsonx.getJsonObj(jsonStr)
         database = dbOps.databaseOps()
         database.save_streamer_put(jObj)
         # save to database
         # - - - - - - - - - - - - - - - - - -
         return {"val": 2}
      except Exception as e:
         return {f"exception: {str(e)}"}
