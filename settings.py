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

    SQLALCHEMY_DATABASE_URI = 'sqlite:///db_beasiswa.db'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:' + APP_ROOT + 'db_beasiswa.db'

    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + \
    #     username + ':' + password + '@' + host + '/' + database
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT Config
    JWT_SECRET_KEY = str(os.getenv('JWT_SECRET_KEY'))
    JWT_ACCESS_TOKEN_EXPIRES = str(os.getenv('JWT_ACCESS_TOKEN_EXPIRES'))

    # MAIL Config
    MAIL_SERVER = str(os.getenv('mail_server'))
    MAIL_PORT = str(os.getenv('mail_port'))
    MAIL_USE_SSL = str(os.getenv('mail_ssl'))
    MAIL_USERNAME = str(os.getenv('mail_username'))
    MAIL_PASSWORD = str(os.getenv('mail_password'))
    
    
    # uploads folder
    # UPLOAD_FOLDER = str(os.getenv('UPLOAD_FOLDER'))
    print(SQLALCHEMY_DATABASE_URI)


