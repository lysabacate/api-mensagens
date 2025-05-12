from flask import Flask, request, jsonify, make_response
from models.mensagens import Mensagem
from utils import db
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dados.db'
db.init_app(app)
app.json.sort_keys = False
migrate = Migrate(app, db)

@app.route('/mensagens', methods=['GET'])
def read_all_mensagens():
    mensagens = Mensagem.query.all()
    lista_mensagens = []
    for mensagem in mensagens:
        lista_mensagens.append({
            'id_mensagem': mensagem.id_mensagem,
            'conteudo': mensagem.conteudo
        })
    return jsonify(lista_mensagens)

@app.route('/mensagens/<int:id_mensagem>', methods=['GET'])
def read_one_mensagens(id_mensagem):
    mensagem = Mensagem.query.get(id_mensagem)
    return jsonify({
        'id_mensagem': mensagem.id_mensagem,
        'conteudo': mensagem.conteudo
    })

@app.route('/mensagens', methods=['POST'])
def create_mensagem():
    conteudo = request.form.get('conteudo')
    nova_mensagem = Mensagem(conteudo=conteudo)

    db.session.add(nova_mensagem)
    db.session.commit()
    return jsonify({
        'id_mensagem': nova_mensagem.id_mensagem,
        'conteudo': nova_mensagem.conteudo
    })

@app.route('/mensagens/<int:id_mensagem>', methods=['PUT'])
def update_mensagem(id_mensagem):
    new_content = request.form.get('conteudo')
    mensagem = Mensagem.query.get(id_mensagem)
    mensagem.conteudo = new_content
    db.session.commit()
    return jsonify({
        'id_mensagem': mensagem.id_mensagem,
        'conteudo': mensagem.conteudo
    })

@app.route('/mensagens/<int:id_mensagem>', methods=['DELETE'])
def delete_mensagem(id_mensagem):
    mensagem = Mensagem.query.get(id_mensagem)
    db.session.delete(mensagem)
    db.session.commit()
    return jsonify(
        {'mensagem':'Sua mensagem foi apagada com sucesso! Verifique a lista agora :)'}
    )


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)