from app import app
from app.extensions import db


def create_all():
    app.app_context().push()
    db.create_all()


def drob_all():
    db.drop_all()
