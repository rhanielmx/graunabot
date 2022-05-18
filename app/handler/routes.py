
from ast import Attribute
from tkinter import E
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
    'phoneNumber': fields.String,
    'requestNumber': fields.String
})

@api.route('/new', methods=['POST'])
class Create_Solicitacao(Resource):
    @api.expect(message_model)
    def post(self):
        msg = request.json['message']
        data = News(**request.json)
        data.save()
        return {'Status':'OK', 'message':msg}, 200

@api.route('/webhook', methods=['POST'])
class Webhook(Resource):
    @api.expect(message_model)
    def post(self):
        msg = None
        if not request:
            msg = 'No request found'
        # try:
        #     body = request.body
        # except AttributeError:
        #     body = None
        #     msg = 'No body found'
        # if body:
        #     try:
        #         url = body.queryResult.parameters['url']        
        #     except AttributeError:
        #         msg='No url found'
        try:
            req=request.get_json(silent=True, force=True)
        except Exception as e:
            msg = 'No request found'
        try:
            query_result = req.get('queryResult')
        except Exception as e:
            msg = 'No query result found'
        try:
            url = query_result.get('parameters').get('url')
        except Exception as e:
            msg = 'No url found'
        
        if not msg:
            msg = f"Iremos olhar o conteúdo de {url} e lhe retornaremos em breve"

        responseObj = {
            "fulfillmentText": "Ok, I will open the link for you",
            "fulfillmentMessages": [{"text":{"text":[url]}}],
            "source": "webhook-response"
        }
        #data = News(message=msg, phoneNumber='', requestNumber=url)
        return responseObj#{'Status':'OK', 'message':'msg', 'body': body, 'url': url}, 200

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
