from flask import Blueprint, jsonify
from app.models.message import Message

mensagens_bp = Blueprint('mensagens', __name__)

@mensagens_bp.route('/', methods=['GET'])
def read_all_mensagens():
    mensagens = Mensagem.query.all()
    lista_mensagens = []
    for mensagem in mensagens:
        lista_mensagens.append({
            'id_mensagem': mensagem.id_mensagem,
            'conteudo': mensagem.conteudo
        })
    return jsonify(lista_mensagens)

@mensagens_bp.route('/<int:id_mensagem>', methods=['GET'])
def read_one_mensagens(id_mensagem):
    mensagem = Mensagem.query.get_or_404(id_mensagem, description="A mensagem com o ID digitado não existe")
    return jsonify({
        'id_mensagem': mensagem.id_mensagem,
        'conteudo': mensagem.conteudo
    })

@mensagens_bp.route('/', methods=['POST'])
def create_mensagem():
    conteudo = request.form.get('conteudo')
    nova_mensagem = Mensagem(conteudo=conteudo)

    db.session.add(nova_mensagem)
    db.session.commit()
    return jsonify({
        'id_mensagem': nova_mensagem.id_mensagem,
        'conteudo': nova_mensagem.conteudo
    })

@mensagens_bp.route('/<int:id_mensagem>', methods=['PUT'])
def update_mensagem(id_mensagem):
    new_content = request.form.get('conteudo')
    mensagem = Mensagem.query.get_or_404(id_mensagem, description="A mensagem com o ID digitado não existe")
    mensagem.conteudo = new_content
    db.session.commit()
    return jsonify({
        'id_mensagem': mensagem.id_mensagem,
        'conteudo': mensagem.conteudo
    })

@mensagens_bp.route('/<int:id_mensagem>', methods=['DELETE'])
def delete_mensagem(id_mensagem):
    mensagem = Mensagem.query.get_or_404(id_mensagem, description="A mensagem com o ID digitado não existe")
    db.session.delete(mensagem)
    db.session.commit()
    return jsonify(
        {'mensagem':'Sua mensagem foi apagada com sucesso! Verifique a lista agora :)'}
    )
