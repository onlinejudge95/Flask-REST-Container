from app import utils, exceptions as exc
from app.extensions import db
from app.src.model.user import User


def create_new_user(data):
    """
    Service function to add a user to the database.

    This should be called by the POST /users route.

    Parameters:
    data (dict): user data from request object

    Returns:
    int: public_id of the new user created

    Raises:
    ValueError
    """
    username = data.get("username")
    email = data.get("email")

    if utils.user_not_exists(email):
        new_user = User(email=email, username=username)
        db.session.add(new_user)
        db.session.commit()

        return new_user.public_id
    raise exc.UserExistsError(email, "User with email {} already exists")


def get_user(public_id):
    """
    Service function to get a user with give identifier.

    This should be called by the GET /user/<public_id> route.

    Parameters:
    public_id (str): public identifier form the request object

    Returns:
    dict: jsonifyied user object

    Raises:
    KeyError
    """
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        raise exc.UserDoesNotExistsError(
            public_id, "User with id {} does not exists"
        )

    return user.to_json()


def get_users():
    """
    Service function to get all users.

    This should be called by the GET /user/ route.

    Returns:
    list: list of user objects
    """
    users = User.query.all()

    return [user.to_json() for user in users]


def remove_user(public_id):
    """
    Service function to remove the given user.

    This should be called by the DELETE /user/<public_id> route.

    Parameters:
    public_id (str): public identifier form the request object
    """
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        raise exc.UserDoesNotExistsError(
            public_id, "User with id {} does not exists"
        )

    db.session.delete(user)
    db.session.commit()


def update_user(public_id, data):
    """
    Service function to update the given user, with given data.

    This should be called by the PUT /user/<public_id> route.

    Parameters:
    public_id (str): public identifier form the request object
    data (dict): Key value pairs to modify
    """
    if not data:
        raise exc.IllegalArgumentError("Empty payload")

    if "public_id" in data.keys():
        raise exc.ForbiddenOperationError("Can not modify public_id attribute")

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        raise exc.UserDoesNotExistsError(
            public_id, "User with id {} does not exists"
        )

    for k in data.keys():
        setattr(user, k, data[k])

    db.session.commit()
