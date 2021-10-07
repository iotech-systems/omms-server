
import logging
import codecs, flask, json
import flask_restful as fr
import core.data.databaseOps as dbOps
import routes.api_flask as api_flask


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class api_cltCircuits(fr.Resource):

   @staticmethod
   def get():
      status = 400
      jsonStr = "{\"Error\": \"MissingInput\"}"
      try:
         db: dbOps.databaseOps = dbOps.databaseOps()
         jsonObj = db.get_cltCircuits()
         jsonStr = json.dumps(jsonObj)
         status = 200
      except Exception as e:
         logging.error(e)
         jsonStr = f'{"Error": "{e}"}'
      finally:
         return api_flask.api_flask.jsonResp(jsonStr, status)

   @staticmethod
   def put():
      try:
         """
         # get request body; should be json string
         data = fr.request.data
         # json string
         jsonStr = codecs.decode(data, "UTF-8")
         # create model
         jObj = jsonx.getJsonObj(jsonStr)
         # save to database
         database = dbOps.databaseOps()
         res = database.save_streamer_put(jObj)
         # - - - - - - - - - - - - - - - - - -
         apiRes = api_response("api_streamer", "put", res[0], res[1])
         return api_flask.api_flask.jsonResp(apiRes.toJson(), 200)
         """
      except:
         pass
      finally:
         pass
