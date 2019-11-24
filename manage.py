from app import create_app
from app.cli import cli


if __name__ == "__main__":
    # from app.src.model.user import User

    app = create_app()
    cli()
