
from app import app
from flask import Blueprint, request
from flask_restx import Resource, Api, fields

handler_bp = Blueprint('handler',__name__)
api = Api(handler_bp)

# class NullableString(fields.String):
#     __schema_type__ = ['string', 'null']
#     __schema_example__ = 'nullable string'



message_model = api.model('Message',{
    'message': fields.String,
    'num-pedido': fields.String
})

@api.route('/teste', methods=['POST'])
class Create_Solicitacao(Resource):
    @api.expect(message_model)
    def post(self):
        msg = request.json['message']
        print(request.json)
        return {'Status':'OK', 'message':msg}, 200
