from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
admin = Admin(template_mode="bootstrap3")
