
import flask


class api_flask(object):

   @staticmethod
   def jsonResp(jsonStr: str, statusCode: int) -> flask.Response:
      return flask.Response(response=jsonStr, status=statusCode
            , content_type="application/json")
