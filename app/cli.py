from flask.cli import FlaskGroup

from app import create_app
from app.extensions import db
from app.src.model.user import User


cli = FlaskGroup(create_app=create_app)


@cli.command("init_db")
def init_db():
    """
    Flask command to create the database schemas.

    Use this when you are running your service for the 1st time,
    after editing db connection logic. This will drop the table,
    and rebuild it
    """
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    """
    Flask command to seed the database with some user.

    Run this command when you have a new database so
    that you can seed some data to prevent READ ALL
    APIs to fail.
    """
    db.session.add(
        User(username="onlinejudge95", email="onlinejudge95@gmail.com")
    )
    db.session.add(
        User(username="onlinejudge94", email="onlinejudge94@gmail.com")
    )
    db.session.commit()
