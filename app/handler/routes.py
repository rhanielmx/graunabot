
import json
import re
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
        msgs = []
        url = None
       
        try:
            req=request.get_json(silent=True, force=True)
        except Exception as e:
            msgs.append('No request found')
        try:
            query_result = req.get('queryResult')
        except Exception as e:
            msgs.append('No query result found')

        try:
            url = query_result.get('parameters').get('url')
        except Exception as e:
            msgs.append('No url found')

        try:
            message = query_result.get('parameters').get('queryText')
        except Exception as e:
            print(e)
        
        try:
            requestNumber = query_result.get('parameters').get('requestNumber')
            requestNumber = str(int(requestNumber))
            data = News.query.filter_by(requestNumber=requestNumber).first()
            if data:
                if data.status == 'Pending':
                    msgs.append('Your request is pending! Try again later.')
                else:
                    msgs.append(f"We have verified your request. It is: {data.status}")
                    msgs.append(data.response if data.response else 'No response found')
                    msgs.append("Thank you for using our service.")
            else:
                if requestNumber:
                    msgs.append('No request found with this number')
        except Exception as e:
            print(e)
            

        try:
            url = query_result.get('parameters').get('url')
            if url:
                if not requestNumber:
                    msgs.append(f"Iremos olhar o conteúdo de {url} e lhe retornaremos em breve")
                    data = News(message=message, phoneNumber='', requestNumber=url)
                    data.save()                    
        except Exception as e:
            print(e)

        if not url and not requestNumber:
            msgs.append('Não conseguimos identificar o que você deseja! Tente nos enviando um link para que possamos verificar o conteúdo ou o número de uma solicitação.')
                
        fullfillmentMessages = f'{[{"text":{"text":[msg]}} for msg in msgs]}'
        print('msgs')
        print(msgs)
        print('fullfillmentMessages')
        print(fullfillmentMessages)

        responseObj = {
            "fulfillmentText": " ",
            "fulfillmentMessages": {"text":{"text":[msgs]}},
            "source": "webhook-response"
        }

        
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
