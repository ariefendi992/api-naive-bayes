from app.controllers.c_hello import hello
from app.controllers.c_kampus import kampus
from app.controllers.c_auth import auth


def registerApp(app):
    app.register_blueprint(hello)
    app.register_blueprint(kampus)
    app.register_blueprint(auth)
