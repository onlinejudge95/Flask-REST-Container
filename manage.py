from app import create_app
from app.cli import cli


if __name__ == "__main__":
    app = create_app()
    cli()
