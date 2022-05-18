
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

parameters_fields = api.model('Parameters',{
    'url': fields.String,
    'requestNumber': fields.String,
})

query_fields = api.model('QueryFields',{
    'parameters': fields.Nested(parameters_fields),
})

query_model = api.model('Query',{
    'queryResult': fields.Nested(query_fields),
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
    @api.expect(query_model)
    def post(self):
        print(request.get_json(silent=True, force=True).get('queryResult'))
        msg = None
        url = None
       
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
        
        try:
            requestNumber = query_result.get('parameters').get('requestNumber')
            data = News.query.filter_by(requestNumber=requestNumber).first()
        except Exception as e:
            msg = 'No url found'
        
        if not msg:
            if url:
                msg = f"Iremos olhar o conteúdo de {url} e lhe retornaremos em breve"
            else:
                msg = 'Não conseguimos identificar o que você deseja! Tente nos enviando um link para que possamos verificar o conteúdo'

        
        responseObj = {
            "fulfillmentText": " ",
            "fulfillmentMessages": [{"text":{"text":[msg]}}],
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
