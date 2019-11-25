from flask import Blueprint, request
from flask_restful import Api, Resource
from sqlalchemy import exc

from app import exceptions
from app.extensions import db
from app.src.service import user as service


bp = Blueprint("users", __name__)
api = Api(bp)


class UserCollectionView(Resource):
    @staticmethod
    def post():
        data = request.get_json()

        if not data:
            return {"status": "fail", "message": "Empty payload"}, 400

        try:
            public_id = service.create_new_user(data)
            return (
                {
                    "status": "success",
                    "message": f"{data.get('email')} was added!",
                    "data": {"public_id": public_id},
                },
                201,
            )
        except exc.IntegrityError:
            db.session.rollback()
            return {"status": "fail", "message": "Invalid payload."}, 400
        except exceptions.UserExistsError as e:
            return e.to_json(), 400

    @staticmethod
    def get():
        users = service.get_users()
        return {"status": "success", "data": {"users": users}}, 200


class UserView(Resource):
    @staticmethod
    def get(public_id):
        try:
            user = service.get_user(public_id)
            return {"status": "success", "data": user}, 200
        except exceptions.UserDoesNotExistsError as e:
            return e.to_json(), 404

    @staticmethod
    def delete(public_id):
        try:
            user = service.get_user(public_id)
            service.remove_user(user.get("public_id"))
            return (
                {
                    "status": "success",
                    "message": f"{user.get('email')} was removed!",
                },
                200,
            )
        except exceptions.UserDoesNotExistsError as e:
            return e.to_json(), 404

    @staticmethod
    def put(public_id):
        data = request.get_json()

        try:
            user = service.get_user(public_id)
            service.update_user(user.get("public_id"), data)
            return (
                {"status": "success", "message": f"{public_id} was updated!"},
                200,
            )
        except exceptions.IllegalArgumentError as e:
            return e.to_json(), 400
        except exceptions.ForbiddenOperationError as e:
            return e.to_json(), 403
        except exceptions.UserDoesNotExistsError as e:
            return e.to_json(), 404


api.add_resource(UserCollectionView, "/users")
api.add_resource(UserView, "/users/<public_id>")
