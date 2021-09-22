
import logging
import codecs, flask, json
import flask_restful as fr
import api.core.data.databaseOps as dbOps
import api.routes.api_flask as api_flask


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class api_clients(fr.Resource):

   @staticmethod
   def get():
      status = 400
      jsonStr = "{\"Error\": \"MissingInput\"}"
      try:
         db: dbOps.databaseOps = dbOps.databaseOps()
         jsonObj = db.get_allClients()
         jsonStr = json.dumps(jsonObj)
         status = 200
      except Exception as e:
         logging.error(e)
         jsonStr = f'{"Error": "{e}"}'
      finally:
         return api_flask.api_flask.jsonResp(jsonStr, status)
