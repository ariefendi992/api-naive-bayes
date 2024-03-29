from app.controllers.api.c_kategori import kategori
from app.controllers.api.c_auth import auth
from app.controllers.api.c_beasiswa_ukt import ukt
from app.controllers.api.c_uploader import upload
from app.controllers.api.c_count_data import count_data
from app.controllers.api.c_download import download


def registerApp(app):
    app.register_blueprint(kategori)
    app.register_blueprint(auth)
    app.register_blueprint(ukt)
    app.register_blueprint(upload)
    app.register_blueprint(count_data)
    app.register_blueprint(download)
