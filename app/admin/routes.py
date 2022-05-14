from app import app
from flask import Blueprint, request
from flask_restx import Resource, Api, fields

admin_bp = Blueprint('admin',__name__)

@admin_bp.route('/')
def index():
    return '<h1>Painel Admnistrativo!</h1>'

#api = Api(admin_bp)

# @api.route('/teste', methods=['GET'])
# class Show_Admin(Resource):
#     def get(self):
        
#         return {'Status':'OK', 'message':'I am Admin'}, 200