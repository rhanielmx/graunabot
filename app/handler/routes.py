from app import app, db
from flask import Blueprint, request
from flask_restx import Resource, Api, fields

from app.models import Solicitation

handler_bp = Blueprint('handler',__name__)
api = Api(handler_bp)

# class NullableString(fields.String):
#     __schema_type__ = ['string', 'null']
#     __schema_example__ = 'nullable string'

message_model = api.model('Message',{
    'message': fields.String,
    'url': fields.String,
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
        data = Solicitation(**request.json)
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
            data = Solicitation.query.filter_by(id=requestNumber).first()
            if data:
                if data.status == 'Pending':
                    msgs.append((
                        """Oi 👋🏽\n"""
                        """\n"""
                        """Você solicitou uma checagem e estou trabalhando nisso! 🕵🏽‍♀️\n"""
                        """\n"""
                        """Acesse nosso site e veja outras checagens que já foram feitas: <url-do-site>\n"""
                    ))
                else:
                    msgs.append(f"Eu e minha equipe checamos a informação que você nos enviou e aqui está o resultado: Esse link é {data.status}")
                    if data.response:
                        msgs.append(data.response)
                    msgs.append((
                        f"Sua checagem foi solicitada às {data.created_at} e respondida às {data.responded_at}.\n"
                        "\n"
                        "O que você achou do atendimento? 💬\n"
                        "\n"
                        "Ajude-nos a melhorar o meu funcionamento!\n" 
                        "\n"
                        "Responda o formulário e conte-nos sobre sua experiência com a Ana, a robô que analisa 🕵🏽‍♀️\n"
                        "\n"
                        "<url-do-formulario>\n"                     
                    ))
            else:
                if requestNumber:
                    msgs.append('Não encontrei solicitação com esse número. Você tem certeza de que digitou o número correto?')
        except Exception as e:
            print(e)
            
        try:
            url = query_result.get('parameters').get('url')
            if url:
                if not requestNumber:
                    data = Solicitation(message=message, url=url)
                    data.save()
                    msgs.append("Olá, essa é uma mensagem automática. Já recebi sua solicitação e trago uma resposta assim que possível 😉")                    
                    msgs.append((                        
                                "Sabia que você mesmo pode fazer uma checagem inicial? 🤔\n"
                                "\n"
                                 "Confira como descobrir se um link é verdadeiro:\n"
                                "\n"
                                "💻 Veja se o link corresponde a um site de confiança e credibilidade;\n"
                                "⌨️ Veja se o link possui critérios de segurança como “https” no início;\n"
                                "🔎 Procure quem fez a matéria e pesquise o nome do jornalista que assinou.\n"
                                "\n"
                                "Enquanto isso, estou trabalhando e checando seu pedido 🕵🏽‍♀️"
                                )
                    )                               
                    msgs.append(f"Você pode consultar a sua solicitação com o número de pedido: {data.id}")
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

        
        return responseObj, 200

@api.route('/list', methods=['GET'])
class ListNews(Resource):
    def get(self):
        data = Solicitation.query.order_by(Solicitation.id).all()
        return {'Status':'OK', 'News':[d.json() for d in data]}, 200

@api.route('/list/<int:id>', methods=['GET'])
class ListNews(Resource):
    def get(self, id):
        solicitation = Solicitation.query.filter_by(id=id).first()
        if solicitation:
            data = solicitation.json()
        else:
            data = []

        return {'Status':'OK', 'Solicitation':data}, 200
