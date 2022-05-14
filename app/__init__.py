from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)
migrate = Migrate(app,db)

from app.admin.routes import admin_bp
from app.handler.routes import handler_bp

app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(handler_bp, url_prefix='/handler')