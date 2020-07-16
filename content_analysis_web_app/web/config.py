import os
basedir = os.path.abspath(os.path.dirname(__file__))
class Config_KEY(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

class Config_DB(object):

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
