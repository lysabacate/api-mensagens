from flask import Blueprint, jsonify, request
from models.mensagens import Mensagem
from utils import db
from schemas.mensagem_schema import MensagemSchema

mensagens_bp = Blueprint('mensagens', __name__)
mensagem_schema = MensagemSchema()
mensagem_schema = MensagemSchema(many=True)

@mensagens_bp.route('/', methods=['GET'])
def read_all_mensagens():
    mensagens = Mensagem.query.all()
    return mensagem_schema.jsonify(mensagens), 200

@mensagens_bp.route('/<int:id_mensagem>', methods=['GET'])
def read_one_mensagens(id_mensagem):
    mensagem = Mensagem.query.get_or_404(id_mensagem, description="A mensagem com o ID digitado não existe")
    return mensagem_schema.jsonify(mensagem), 200

@mensagens_bp.route('/', methods=['POST'])
def create_mensagem():
    conteudo = request.form.get('conteudo')
    if not conteudo:
        return jsonify({'mensagem': 'O campo "conteudo" é obrigatório'}), 400

    nova_mensagem = Mensagem(conteudo=conteudo)

    db.session.add(nova_mensagem)
    db.session.commit()
    return mensagem_schema.jsonify(conteudo), 201

@mensagens_bp.route('/<int:id_mensagem>', methods=['PUT'])
def update_mensagem(id_mensagem):
    new_content = request.form('conteudo')
    if not new_content:
        return jsonify({'mensagem': 'O campo "conteudo" é obrigatório'}), 400

    mensagem = Mensagem.query.get_or_404(id_mensagem, description="A mensagem com o ID digitado não existe")
    mensagem.conteudo = new_content
    db.session.commit()
    return mensagem_schema.jsonify(mensagens), 200

@mensagens_bp.route('/<int:id_mensagem>', methods=['DELETE'])
def delete_mensagem(id_mensagem):
    mensagem = Mensagem.query.get_or_404(id_mensagem, description="A mensagem com o ID digitado não existe")
    db.session.delete(mensagem)
    db.session.commit()
    return jsonify(
        {'mensagem':'Sua mensagem foi apagada com sucesso! Verifique a lista agora :)'}
    ), 204
