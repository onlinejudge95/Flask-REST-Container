from flask.cli import FlaskGroup

from app import app


cli = FlaskGroup()


if __name__ == "__main__":
    cli()
