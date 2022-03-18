import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

baseDir = os.path.dirname(os.path.abspath(__file__))
db = os.path.join(baseDir, 'beasiswa.db')
print(db)
dir = os.getcwd()
# tes directori project
# print('Base Dir = ', baseDir)
# print('Dir = ', dir + '/app')


class Config(object):
    # general configuration
    SECRET_KEY = str(os.getenv('S_Key'))
    TESTING = str(os.getenv('TESTING'))

    # db configuration
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + db
    # SQLALCHEMY_DATABASE_URI = str(os.getenv('SQLALCHEMY_BATABASE_URI'))
    print(SQLALCHEMY_DATABASE_URI)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT Config
    JWT_SECRET_KEY = str(os.getenv('JWT_SECRET_KEY'))
