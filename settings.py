import os
from dotenv import load_dotenv

load_dotenv()

baseDir = os.path.dirname(os.path.abspath(__file__))
dir = os.getcwd()
# tes directori project
# print('Base Dir = ', baseDir)
# print('Dir = ', dir + '/app')


class Config(object):
    # general configuration
    SECRET_KEY = str(os.getenv('S_Key'))
    TESTING = str(os.getenv('TESTING'))

    # db configuration
    SQLALCHEMY_DATABASE_URI = str(os.getenv('SQLALCHEMY_BATABASE_URI'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT Secret Key
    JWT_SECRET_KEY = str(os.getenv('JWT_SECRET_KEY'))

    # print(JWT_SECRET_KEY)
