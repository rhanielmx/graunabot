
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
        message = None
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
            message = query_result.get('queryText')
        except Exception as e:
            print(e)
                  
        try:
            requestNumber = query_result.get('parameters').get('requestNumber')
            requestNumber = str(int(requestNumber))
            data = News.query.filter_by(id=requestNumber).first()
            if data:
                if data.status == 'Pending':
                    msgs.append('Essa solicitação ainda está sendo analisada. Por favor, solicite novamente mais tarde!')
                else:
                    msgs.append(f"Nós analisamos a sua solicitação. Ela é: {data.status}")
                    if data.response:
                        msgs.append(data.response)
                    msgs.append("Obrigado por usar o nosso serviço.")
            else:
                if requestNumber:
                    msgs.append('Não encontrei solicitação com esse número. Você tem certeza de que digitou o número correto?')
        except Exception as e:
            print(e)
            

        try:
            url = query_result.get('parameters').get('url')
            if url:
                if not requestNumber:
                    data = News(message=message, url=url)
                    data.save()                    
                    msgs.append(f"Iremos olhar o conteúdo de {url} e atualizaremos em nosso banco de dados.")
                    msgs.append(f"Você pode consultar a sua solicitação com o número de pedido {data.id}")
        except Exception as e:
            print(e)

        if not url and not requestNumber:
            msgs.append('Não conseguimos identificar o que você deseja! Tente nos enviando um link para que possamos verificar o conteúdo ou o número de uma solicitação.')
                
        #fullfillmentMessages = f'{[{"text":{"text":[msg]}} for msg in msgs]}'
        # print('msgs')
        # print(msgs)
        # print('fullfillmentMessages')
        # print(fullfillmentMessages)

        responseObj = {
            "fulfillmentText": " ",
            "fulfillmentMessages": [{"text":{"text":[msg]}} for msg in msgs],
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
