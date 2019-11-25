from flask import Blueprint
from flask_restful import Api, Resource


bp = Blueprint("ping", __name__)
api = Api(bp)


class PingView(Resource):
    @staticmethod
    def get():
        return {"status": "success", "message": "pong"}


api.add_resource(PingView, "/ping")
