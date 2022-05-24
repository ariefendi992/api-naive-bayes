from flask import Flask
from settings import Config
from app.registers import registerApp


def createApp():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    registerApp(app)
    registerExtension(app)
    from app.extensions import db, migrate
    
    @app.get('/')
    def index():
        return '<h2>Halaman Web APIS</h2>'

    return app


def registerExtension(app):
    from app.extensions import swagger, db, migrate, jwtManager

    swagger.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwtManager.init_app(app)


app = createApp()
