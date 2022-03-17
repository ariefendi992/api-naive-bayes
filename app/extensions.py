from flasgger import Swagger
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

swagger = Swagger()
db = SQLAlchemy()
migrate = Migrate()
jwtManager = JWTManager()
