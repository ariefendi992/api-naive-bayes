from flasgger import Swagger
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_mail import Mail

swagger = Swagger()
db = SQLAlchemy()
migrate = Migrate()
jwtManager = JWTManager()
mail = Mail()