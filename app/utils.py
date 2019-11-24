import logging

from flask import current_app, has_request_context, request
from flask.logging import default_handler

from app.extensions import db
from app.src.model.user import User


class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
        else:
            record.url = None
            record.remote_addr = None

        return super().format(record)


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
    current_app.logger.debug(f"Added {user.to_json()} to db session")

    db.session.commit()
    current_app.logger.debug(f"Session comitted")

    return user.public_id


def recreate_db():
    """
    Utility function to recreate the database.

    Use this when you need to make sure each tests run in isolation.
    """
    db.session.remove()
    current_app.logger.debug("Current db session removed")

    db.drop_all()
    current_app.logger.debug("Dropped all databases")

    db.create_all()
    current_app.logger.debug("Created all database schema")


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


def init_logger():
    """
    Utility function to initialise the logger.

    Use this to set up logging for your server.
    This should be called just after the app object is intantiated.
    """
    formatter = RequestFormatter(
        "[%(asctime)s] %(remote_addr)s requested %(url)s\n"
        "%(levelname)s in %(module)s: %(message)s"
    )
    default_handler.setLevel(logging.INFO)
    default_handler.setFormatter(formatter)
