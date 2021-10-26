
import logging
import flask, json
import flask_restful as fr
import core.data.databaseOps as dbOps


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class api_org(fr.Resource):

   @staticmethod
   def get():
      status = 400
      jsonStr = "{\"Error\": \"Unexpected\"}"
      try:
         db: dbOps.databaseOps = dbOps.databaseOps()
         resObj = db.get_org()
         if resObj is not None:
            jsonStr = json.dumps(resObj)
            status = 200
      except Exception as e:
         logging.error(e)
      finally:
         return flask.Response(response=jsonStr, status=status
            , content_type="application/json")
