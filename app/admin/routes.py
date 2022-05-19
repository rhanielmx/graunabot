from app import app
from flask import Blueprint, request
from flask_restx import Resource, Api, fields

from app.models import Category, Solicitation

admin_bp = Blueprint('admin',__name__)

# @admin_bp.route('/')
# def index():
#     return '<h1>Painel Admnistrativo!</h1>'

api = Api(admin_bp)

categories_model = api.model('Categories',{
    'name': fields.String,
    'description': fields.String,
})

update_solicitation_model = api.model('UpdateSolicitation',{
    'status': fields.String,
    'response': fields.String,
    'category_id': fields.Integer,
})

@api.route('/category', methods=['GET', 'POST', 'DELETE', 'PUT'])
class Categories(Resource):
    def get(self):
        categories = Category.query.all()   
        return {'Status':'OK', 'message':[c.json() for c in categories]}, 200

    @api.expect(categories_model)
    def post(self):
        data = request.json
        category = Category(**data)
        category.save()
        return {'Status':'OK', 'message':category.json()}, 200

@api.route('/category/<int:category_id>', methods=['GET', 'DELETE', 'PUT'])
class CategoryList(Resource):
    def get(self, category_id):
        category = Category.query.get(category_id)
        return {'Status':'OK', 'message':category.json()}, 200

    @api.expect(categories_model)
    def put(self, category_id):
        try:
            data = request.json
            category = Category.query.get(category_id)
            category.update(**data)
            return {'Status':'OK', 'message':category.json()}, 200
        except Exception as e:
            return {'Status':'ERROR', 'message':str(e)}, 500

    def delete(self, category_id):
        try:
            category = Category.query.get(category_id)
            category.delete()
            return {'Status':'OK', 'message':'Category deleted'}, 200
        except Exception as e:
            return {'Status':'ERROR', 'message':str(e)}, 500


@api.route('/solicitation/<int:id>', methods=['GET', 'DELETE', 'PUT'])
class Solicitations(Resource):
    def get(self, id):
        solicitation = Solicitation.query.filter_by(id=id).first()
        if solicitation:
            data = solicitation.json()
        else:
            return {'Status':'ERROR', 'message':'Solicitation not found'}
        return {'Status':'OK', 'message':data}, 200

    @api.expect(update_solicitation_model)
    def put(self, id):
        solicitation = Solicitation.query.filter_by(id=id).first()
        if solicitation:
            data = request.json
            solicitation.update(**data)
            data = solicitation.json()
        else:
            return {'Status':'ERROR', 'message':'Solicitation not found'}
        return {'Status':'OK', 'message':data}, 200