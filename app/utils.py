from app import db
from app.src.model.user import User


def add_user(data):
    user = User(username=data.get("username"), email=data.get("email"))

    db.session.add(user)
    db.session.commit()

    return user


def recreate_db():
    db.session.remove()
    db.drop_all()
    db.create_all()
