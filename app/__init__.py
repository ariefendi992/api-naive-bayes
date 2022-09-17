from flask import Flask
from settings import Config
from app.registers import registerApp
import os



def createApp():
    # UPLOAD_FOLDER = '/app/static/'
    app = Flask(__name__)
    app.config.from_object(Config)
    # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    
    
    registerApp(app)
    registerExtension(app)
    # from app.extensions import db, migrate
    
    @app.get('/')
    def index():
        return '<h2>Halaman Web APIS</h2>'

    return app


def registerExtension(app):
    from app.extensions import swagger, db, migrate, jwtManager, mail

    swagger.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwtManager.init_app(app)
    mail.init_app(app)


app = createApp()
