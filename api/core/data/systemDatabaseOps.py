
import logging
from typing import List
import core.data.dbCore as dbCore
from ommslib.shared.app_error_codes import appErrorCodes
from ommslib.shared.core.registerNames import registerNames as rn
from ommslib.shared.utils.sysutils import sysutils
from ommslib.shared.models import alarmReport, kWhReport,\
   jsonPackageHead, kWhReading
from core.data.reportsSQL import reportsSQL as repSQL
from core.data.configSQL import configSQL as confSQL


logfile = "logs/dbops.log"
level = logging.WARNING
HISTOGRAM_POINTS_HR = 30
LIVE_TBL_ROW_HRS_TTL = 24


class systemDatabaseOps(object):

   def __init__(self):
      self.dbCore = dbCore.dbCore()

   def get_systemEdges(self):
      qry = "select * from config.edges;"
      return self.dbCore.query_fetchall(qry)

   def get_edgeStatus(self, edgeName) -> {}:
      qry = f"select t.ip, t.hostname, cast(t.dts_utc as varchar) " \
         f" from diagnostics.edge_pings t where t.hostname = '{edgeName}'" \
         f" order by t.dts_utc desc limit 1;"
      ping = self.dbCore.run_query_fetchone(qry)
      return {"ping": ping, "ph0": None, "ph1": None}
