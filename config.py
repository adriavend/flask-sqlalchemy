import os

class Config(object):
    SECRET_KEY = 'my_secret_key'

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:gf637@localhost:3306/flask'
    SQLALCHEMY_TRACK_MODIFICATIONS = False