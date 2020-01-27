from flask import Blueprint, current_app as app
from flask_restful import Api, Resource


bp = Blueprint("ping", __name__)
api = Api(bp)


class PingView(Resource):
    @staticmethod
    def get():
        app.logger.info("received a /ping request")
        return {"status": "success", "message": "pong"}


api.add_resource(PingView, "/ping")
