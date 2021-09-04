
import datetime
import flask_restful as fr


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
class api_info(fr.Resource):

   @staticmethod
   def get():
      try:
         buff = f"""
            sbms-rest-api-server: {datetime.datetime.utcnow()}
         """
         return buff
      except Exception as e:
         return {f"exception: {str(e)}"}
