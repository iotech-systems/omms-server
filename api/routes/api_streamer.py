
import logging
import codecs, flask, json
import flask_restful as fr
from ommslib.shared.utils.jsonx import jsonx
from ommslib.shared.api_response import api_response
from ommslib.shared.webprint import webprint
import core.data.databaseOps as dbOps
import routes.api_flask as api_flask


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class api_streamer(fr.Resource):

   @staticmethod
   def put():
      try:
         # get request body; should be json string
         data = fr.request.data
         # json string
         jsonStr = codecs.decode(data, "UTF-8")
         wp: webprint = webprint()
         wp.print(jsonStr)
         # create model
         jObj = jsonx.getJsonObj(jsonStr)
         # save to database
         database = dbOps.databaseOps()
         res = database.save_streamerPUT(jObj)
         # - - - - - - - - - - - - - - - - - -
         apiRes = api_response("api_streamer", "put", res[0], res[1])
         return api_flask.api_flask.jsonResp(apiRes.toJson(), 200)
      except Exception as e:
         return {f"exception: {str(e)}"}

   @staticmethod
   def get():
      status = 400
      jsonStr = "{\"Error\": \"MissingInput\"}"
      try:
         badInput = (None, "None")
         streamTbl: str = str(flask.request.args.get("streamTbl"))
         if not streamTbl.startswith("__"):
            streamTbl = f"__{streamTbl}"
         meterDBID: str = str(flask.request.args.get("meterDBID"))
         if (streamTbl in badInput) or (meterDBID in badInput):
            raise Exception("MissingInput")
         db: dbOps.databaseOps = dbOps.databaseOps()
         resObj = db.read_lastFromStreamTbl(streamTbl, meterDBID)
         # tag returning data packet with the tbl it was targeting
         resObj["streamTbl"] = streamTbl
         if resObj is not None:
            jsonStr = json.dumps(resObj)
            status = 200
      except Exception as e:
         logging.error(e)
         jsonStr = f'{"Error": "{e}"}'
      finally:
         return api_flask.api_flask.jsonResp(jsonStr, status)


# -- test --
if __name__ == "__main__":
   # api_streamer.put()
   wp: webprint = webprint()
   wp.init()
   wp.print("test")
