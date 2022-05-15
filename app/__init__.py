from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

from app.admin.routes import admin_bp
from app.handler.routes import handler_bp

app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(handler_bp, url_prefix='/handler')