import os
from dotenv import load_dotenv

load_dotenv()

baseDir = os.path.dirname(os.path.abspath(__file__))
db = os.path.join(baseDir, 'beasiswa.db')
# print(db)
dir = os.getcwd()
# tes directori project
# print('Base Dir = ', baseDir)
# print('Dir = ', dir + '/app')


class Config(object):
    # general configuration
    SECRET_KEY = str(os.getenv('S_Key'))
    TESTING = str(os.getenv('TESTING'))

    # db configuration
    # SQLITE
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + db

    # MySQL
    username = str(os.getenv('DB_USER'))
    password = str(os.getenv('DB_PASSWORD'))
    host = str(os.getenv('DB_HOST'))
    database = str(os.getenv('DB_NAME'))
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + \
        username + ':' + password + '@' + host + '/' + database
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT Config
    JWT_SECRET_KEY = str(os.getenv('JWT_SECRET_KEY'))
    JWT_ACCESS_TOKEN_EXPIRES = str(os.getenv('JWT_ACCESS_TOKEN_EXPIRES'))
