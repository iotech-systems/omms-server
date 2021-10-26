
import flask, json
import core.data.databaseOps as dbOps
import core.data.reportsSQL as repSQL


class sysReports(object):

   def __init__(self):
      pass

   def meter_kwhrs(self, req: flask.request):
      sDts: str = str(req.args.get("sDts"))
      eDts: str = str(req.args.get("eDts"))
      meterDBID: str = str(req.args.get("mDBID"))
      qry = repSQL.reportsSQL.meter_kwhrs(sDts, eDts, meterDBID)
      db: dbOps.databaseOps = dbOps.databaseOps()
      jobj = db.run_meter_kWhrsReport(qry)
      return json.dumps(jobj)

   def client_kwhrs(self, req: flask.request):
      pass
