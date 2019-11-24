import os

from flask import Flask

from app import extensions as ext, utils


def create_app():
    """
    App factory for the server.

    Receive an app instance for differnet env like development, testing etc

    Returns:
    flask.Flask: App instance
    """
    utils.init_logger()

    app = Flask(__name__)

    app.config.from_object(os.getenv("APP_SETTINGS"))

    ext.db.init_app(app)

    from app.src.routes.ping import bp as ping_bp

    app.register_blueprint(ping_bp)

    from app.src.routes.user import bp as user_bp

    app.register_blueprint(user_bp)

    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": ext.db}

    return app
