from flask import Blueprint, request
from flask_restful import Api, Resource
from sqlalchemy import exc

from app.extensions import db
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
        except ValueError as e:
            return (
                {"status": "fail", "message": str(e),},
                400,
            )

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
        except KeyError as e:
            return {"status": "fail", "message": str(e)}, 404

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
        except KeyError as e:
            return {"status": "fail", "message": str(e)}, 404

    @staticmethod
    def put(public_id):
        data = request.get_json()

        if not data:
            return {"status": "fail", "message": "Empty payload"}, 400

        try:
            if "public_id" in data.keys():
                raise PermissionError("Can not modify public_id attribute")

            user = service.get_user(public_id)
            service.update_user(user.get("public_id"), data)
            return (
                {"status": "success", "message": f"{public_id} was updated!"},
                200,
            )
        except PermissionError as e:
            return (
                {"status": "fail", "message": str(e),},
                403,
            )
        except KeyError as e:
            return {"status": "fail", "message": str(e)}, 404


api.add_resource(UserSetAPI, "/users")
api.add_resource(UserAPI, "/users/<public_id>")
