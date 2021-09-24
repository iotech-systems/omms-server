#!/usr/bin/env python3

import datetime
import flask as f
import setproctitle
import flask_restful as fr
import core.data.inProcStore as store
# import routes
from routes import api_alarmReport, api_kWhReport, api_pingPong, \
   api_streamer, api_info, api_dbInfo, api_getMeters, api_org, \
   api_elecRoomMeters, api_report, api_clients, api_elecRoomActiveMeters, \
   api_histogram


APP_NAME = "sbms-api-server"
app = f.Flask(APP_NAME)
restApi = fr.Api(app)


restApi.add_resource(api_kWhReport.api_kWhReport, "/report-kwh")
restApi.add_resource(api_alarmReport.api_alarmReport, "/report-alarm")
restApi.add_resource(api_streamer.api_streamer, "/streamer")
restApi.add_resource(api_pingPong.api_pingPong, "/ping")
restApi.add_resource(api_info.api_info, "/info")
restApi.add_resource(api_dbInfo.api_dbinfo, "/db-info")
restApi.add_resource(api_getMeters.api_getMeters, "/meters")
restApi.add_resource(api_clients.api_clients, "/clients")
restApi.add_resource(api_report.api_report, "/report")
restApi.add_resource(api_elecRoomMeters.api_getElecRoomMeters, "/elc-room-meters")
restApi.add_resource(api_histogram.api_histogram, "/histogram")
restApi.add_resource(api_elecRoomActiveMeters.api_elecRoomActiveMeters, "/elc-room-meters-active")
restApi.add_resource(api_org.api_org, "/org")

# store run.py time
store.inProcStore.addKeyVal("AppStart", datetime.time())


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
if __name__ == "__main__":
   # dump flask info
   print(f"\n  * flask version: {f.__version__}\n")
   setproctitle.setproctitle("sbms-api-server")
   app.run(host="0.0.0.0", port=8082, debug=False)
