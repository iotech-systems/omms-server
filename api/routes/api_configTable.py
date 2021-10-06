
import logging
import codecs, flask, json
import flask_restful as fr
import core.data.databaseOps as dbOps
import routes.api_flask as api_flask


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class api_configTable(fr.Resource):

   @staticmethod
   def put():
      try:
         # get request body; should be json string
         data = fr.request.data
         # json string
         jsonStr = codecs.decode(data, "utf-8")
         # create model
         # save to database
         database = dbOps.databaseOps()
         res = database.save_configTablePUT(jsonStr)
         # - - - - - - - - - - - - - - - - - -
         return api_flask.api_flask.jsonResp("", 200)
      except:
         pass
      finally:
         pass
