from app.controllers.c_hello import hello
from app.controllers.api.c_kampus import kampus
from app.controllers.api.c_auth import auth
from app.controllers.api.c_beasiswa_ukt import ukt
from app.controllers.admin.c_admin import admin


def registerApp(app):
    app.register_blueprint(hello)
    app.register_blueprint(kampus)
    app.register_blueprint(auth)
    app.register_blueprint(ukt)
    app.register_blueprint(admin)
