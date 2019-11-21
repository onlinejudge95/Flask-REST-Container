from app import db, utils
from app.src.model.user import User


def create_new_user(data):
    """
    Service function to add a user to the database.

    This should be called by the POST /users route.

    Parameters:
    data (dict): user data from request object

    Returns:
    int: public_id of the new user created
    """
    username = data.get("username")
    email = data.get("email")

    if utils.user_not_exists(email):
        new_user = User(email=email, username=username)
        db.session.add(new_user)
        db.session.commit()

        return new_user.public_id
    raise ValueError()


def get_user(public_id):
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        raise KeyError()

    return user.to_json()


def get_users():
    users = User.query.all()

    return [user.to_json() for user in users]
