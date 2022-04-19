from app.controllers.api.c_kampus import kampus
from app.controllers.api.c_auth import auth
from app.controllers.api.c_beasiswa_ukt import ukt
from app.controllers.api.c_uploader import upload
from app.controllers.api.c_count_data import count_data


def registerApp(app):
    app.register_blueprint(kampus)
    app.register_blueprint(auth)
    app.register_blueprint(ukt)
    app.register_blueprint(upload)
    app.register_blueprint(count_data)
