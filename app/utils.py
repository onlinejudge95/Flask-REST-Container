from app.extensions import db
from app.src.model.user import User


def add_user(data):
    """
    Utility function to add a user to the database.

    Use this when you need to create a user but not while in
    `test_new_user` scope.

    Parameters:
    data (dict): user data from request object

    Returns:
    int: public_id of the new user created
    """
    user = User(username=data.get("username"), email=data.get("email"))

    db.session.add(user)
    db.session.commit()

    return user.public_id


def recreate_db():
    """
    Utility function to recreate the database.

    Use this when you need to make sure each tests run in isolation.
    """
    db.session.remove()
    db.drop_all()
    db.create_all()


def user_not_exists(email):
    """
    Utility function to check if the user exists.

    Use this when you need to make sure whether a user already exists

    Parameters:
    email (str): email field form the request object

    Returns:
    bool: Whether the user already exists
    """
    return User.query.filter_by(email=email).first() is None
