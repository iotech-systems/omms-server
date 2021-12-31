
import json
import flask_restful as fr
import core.data.systemDatabaseOps as dbSysOps
from routes.api_flask import api_flask


class api_sysOverview(fr.Resource):

   @staticmethod
   def get():
      try:
         buffOut = []
         sysOps: dbSysOps.systemDatabaseOps = dbSysOps.systemDatabaseOps()
         # -- oneach --
         def oneach(edge: str):
            edgename, _ = edge
            edgestats = sysOps.get_edgeStatus(edgename)
            buffOut.append(edgestats)
         # -- get edges --
         edges: [] = sysOps.get_systemEdges()
         for e in edges:
            oneach(e)
         # -- return --
         jsonStr = json.dumps(buffOut)
         return api_flask.jsonResp(jsonStr, 200)
      except Exception as e:
         print(e)
