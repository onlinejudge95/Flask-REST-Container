from flask import Blueprint, request
from flask_restful import Api, Resource
from sqlalchemy import exc

from app import db
from app.src.service import user as service


bp = Blueprint("users", __name__)
api = Api(bp)


class UserSetAPI(Resource):
    @staticmethod
    def post():
        data = request.get_json()

        if not data:
            return {"status": "fail", "message": "Empty payload"}, 400

        try:
            service.create_new_user(data)
            return {"status": "success", "message": f"{data.get('email')} was added!"}, 201
        except exc.IntegrityError:
            db.session.rollback()
            return {"status": "fail", "message": "Invalid payload."}, 400
        except ValueError:
            return {"status": "fail", "message": "Sorry. That email already exists."}, 400

    @staticmethod
    def get():
        users = service.get_users()
        return {"status": "success", "data": {"users": users}}, 200

class UserAPI(Resource):
    @staticmethod
    def get(public_id):
        try:
            user = service.get_user(public_id)
            return {"status": "success", "data": user}, 200
        except KeyError:
            return {"status": "fail", "message": "User does not exist"}, 404


api.add_resource(UserSetAPI, "/users")
api.add_resource(UserAPI, "/users/<public_id>")
