#!/usr/bin/env python3

import datetime
import flask as f
import flask_restful as fr
import core.data.inProcStore as store
# import routes
from routes import api_alarmReport, api_kWhReport, \
   api_pingPong, api_streamer


APP_NAME = "sbms_gate"
app = f.Flask(APP_NAME)
restApi = fr.Api(app)


# put(s)
restApi.add_resource(api_kWhReport.api_kWhReport, "/report-kwh")
restApi.add_resource(api_alarmReport.api_alarmReport, "/report-alarm")
restApi.add_resource(api_streamer.api_streamer, "/streamer")
# get(s)
restApi.add_resource(api_pingPong.api_pingPong, "/ping")


# store run.py time
store.inProcStore.addKeyVal("AppStart", datetime.time())


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
if __name__ == "__main__":
   app.run(host="0.0.0.0", port=8082, debug=True)
