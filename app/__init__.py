from flask import Flask
from settings import Config
from app.registers import registerApp


def createApp(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_object(Config)
    else:
        app.config.from_mapping(test_config)

    registerExtension(app)
    registerApp(app)

    return app


def registerExtension(app):
    from app.extensions import swagger, db, migrate, jwtManager

    swagger.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwtManager.init_app(app)


app = createApp()
