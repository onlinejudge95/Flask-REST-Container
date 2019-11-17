from app import db
from app.src.model.user import User


def create_new_user(data):
    username = data.get("username")
    email = data.get("email")

    user = User.query.filter_by(email=email).first()

    if user:
        raise ValueError()

    db.session.add(User(email=email, username=username))
    db.session.commit()


def get_user(public_id):
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        raise KeyError()

    return user.to_json()


def get_users():
    users = User.query.all()

    return [user.to_json() for user in users]
