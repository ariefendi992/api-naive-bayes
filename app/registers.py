from app.controllers.api.c_kampus import kampus
from app.controllers.api.c_auth import auth
from app.controllers.api.c_beasiswa_ukt import ukt



def registerApp(app):
    app.register_blueprint(kampus)
    app.register_blueprint(auth)
    app.register_blueprint(ukt)
