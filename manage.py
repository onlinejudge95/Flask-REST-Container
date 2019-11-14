from flask.cli import FlaskGroup

from app import create_app, db
from app.src.model.user import User


app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command("init_db")
def init_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


if __name__ == "__main__":
    cli()
