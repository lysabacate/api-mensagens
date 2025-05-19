from flask import Flask, request, jsonify, make_response
from models.mensagens import Mensagem
from utils import db
from flask_migrate import Migrate
from controllers.mensagens import mensagens_bp
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dados.db'
db.init_app(app)
app.json.sort_keys = False
migrate = Migrate(app, db)
app.register_blueprint(mensagens_bp, url_prefix="/mensagens")
ma.initt_app(app)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)