
import flask
import flask_restful as fr
import core.data.databaseOps as dbOps


class api_pingPong(fr.Resource):

   @staticmethod
   def get():
      try:
         hostName: str = str(flask.request.args.get("hostname"))
         ip = flask.request.remote_addr
         db: dbOps.databaseOps = dbOps.databaseOps()
         val = db.save_ping(ip, hostName)
         return f"PONG + {val}"
      except Exception as e:
         print(e)
