import os

from dotenv import load_dotenv
load_dotenv(verbose=True)

basedir = os.path.abspath(os.path.dirname(__file__))

ENGINE = os.getenv('ENGINE')
USER = os.environ.get('USER')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')
DBNAME = os.environ.get('DBNAME')

POSTGRES_URL = f'{ENGINE}://{USER}:{PASSWORD}@{HOST}/{DBNAME}'
print(POSTGRES_URL)

class Config(object):
    DEBUG=True
    #SQLALCHEMY_DATABASE_URI='sqlite:///'+os.path.join(basedir, 'data.db')
    SQLALCHEMY_DATABASE_URI=os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False