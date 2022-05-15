
from app import app, db
from flask import Blueprint, request
from flask_restx import Resource, Api, fields

from app.models import News

handler_bp = Blueprint('handler',__name__)
api = Api(handler_bp)

# class NullableString(fields.String):
#     __schema_type__ = ['string', 'null']
#     __schema_example__ = 'nullable string'



message_model = api.model('Message',{
    'message': fields.String,
    'requestNumber': fields.String
})

@api.route('/new', methods=['POST'])
class Create_Solicitacao(Resource):
    @api.expect(message_model)
    def post(self):
        msg = request.json['message']
        data = News(id=12131,**request.json)
        data.save()
        return {'Status':'OK', 'message':msg}, 200

@api.route('/list', methods=['GET'])
class ListNews(Resource):
    def get(self):
        data = News.query.all()
        return {'Status':'OK', 'News':[d.json() for d in data]}, 200

@api.route('/list/<int:id>', methods=['GET'])
class ListNews(Resource):
    def get(self, id):
        data = News.query.filter_by(id=id).first()
        return {'Status':'OK', 'News':data.json()}, 200
