
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
      out: dict = {}; status = 200
      try:
         jsonStr = fr.request.args.get("load")
         dataDict: dict = json.loads(jsonStr)
         tblidx = dataDict.pop("tblidx")
         tblname = TBLS[tblidx]
         database = dbOps.databaseOps()
         out["rows"] = database.configTablePUT(tblname, dataDict)
         # -- end --
      except Exception as e:
         logging.error(e)
      finally:
         return api_flask.api_flask.jsonResp(json.dumps(out), status)

   @staticmethod
   def delete():
      out: dict = {}; status = 200
      try:
         jsonStr = fr.request.args.get("load")
         dataDict: dict = json.loads(jsonStr)
         tblidx = dataDict.pop("tblidx")
         tblname = TBLS[tblidx]
         database = dbOps.databaseOps()
         out["rows"] = database.configTableDELETE(tblname, dataDict)
         # -- end --
      except Exception as e:
         logging.error(e)
      finally:
         return api_flask.api_flask.jsonResp(json.dumps(out), status)
