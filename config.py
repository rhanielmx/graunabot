import os

from dotenv import load_dotenv
load_dotenv(verbose=True)

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI='sqlite:///'+os.path.join(basedir, 'data.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False