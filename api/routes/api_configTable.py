
import logging
import codecs, flask, json
import flask_restful as fr
import core.data.databaseOps as dbOps
import routes.api_flask as api_flask


TBLS = {"0x00": "clients", "0x02": "circuits", "0x04": "meters", "0x06": "spaces"
        , "0x08": "client_circuits", "0x10": "client_spaces"}


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class api_configTable(fr.Resource):

   @staticmethod
   def put():
      try:
         # get request body; should be json string
         jsonStr = fr.request.args.get("load")
         # json string
         # jsonStr = codecs.decode(data, "utf-8")
         # create model
         # save to database
         dataDict: dict = json.loads(jsonStr)
         tblidx = dataDict.pop("tblidx")
         tblname = TBLS[tblidx]
         database = dbOps.databaseOps()
         rows = database.save_configTablePUT(tblname, dataDict)
         # - - - - - - - - - - - - - - - - - -
         return api_flask.api_flask.jsonResp(f"{{rows:{rows}}}", 200)
      except Exception as e:
         logging.error(e)
      finally:
         pass
