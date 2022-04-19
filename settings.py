import os
from dotenv import load_dotenv

load_dotenv()
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


class Config(object):
    # general configuration
    SECRET_KEY = str(os.getenv('S_Key'))

    # MySQL
    username = str(os.getenv('DB_USER'))
    password = str(os.getenv('DB_PASSWORD'))
    host = str(os.getenv('DB_HOST'))
    database = str(os.getenv('DB_NAME'))

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + \
        username + ':' + password + '@' + host + '/' + database
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://beaa2475_root:TeknikUIM17@localhost/beaa2475_db_beasiswa'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT Config
    JWT_SECRET_KEY = str(os.getenv('JWT_SECRET_KEY'))
    JWT_ACCESS_TOKEN_EXPIRES = str(os.getenv('JWT_ACCESS_TOKEN_EXPIRES'))

    # uploads folder
    # UPLOAD_FOLDER = str(os.getenv('UPLOAD_FOLDER'))
