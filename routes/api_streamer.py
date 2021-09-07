
import logging
import codecs, flask, json
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

   @staticmethod
   def get():
      status = 400
      jsonStr = "{\"Error\": \"MissingInput\"}"
      try:
         badInput = (None, "None")
         streamTbl: str = str(flask.request.args.get("streamTbl"))
         meterDBID: str = str(flask.request.args.get("meterDBID"))
         if (streamTbl in badInput) or (meterDBID in badInput):
            raise Exception("MissingInput")
         db: dbOps.databaseOps = dbOps.databaseOps()
         resObj = db.read_lastFromStreamTbl(streamTbl, meterDBID)
         # tag returning data packet
         resObj["streamTbl"] = streamTbl
         if resObj is not None:
            jsonStr = json.dumps(resObj)
            status = 200
      except Exception as e:
         logging.error(e)
      finally:
         return flask.Response(response=jsonStr, status=status
            , content_type="application/json")
