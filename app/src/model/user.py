import uuid

from sqlalchemy.sql import func

from app.extensions import db


class User(db.Model):
    __tablename__ = "users"
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(
        db.String(32), nullable=False, default=uuid.uuid4().hex
    )
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    created_date = db.Column(db.DateTime, default=func.now(), nullable=False)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def to_json(self):
        return {
            "public_id": self.public_id,
            "username": self.username,
            "email": self.email,
            "active": self.active,
        }
