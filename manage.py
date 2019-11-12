from flask.cli import FlaskGroup

from app import app, db


cli = FlaskGroup()


@cli.command("init-db")
def init_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


if __name__ == "__main__":
    cli()
