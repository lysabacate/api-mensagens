from flask import Flask, request, jsonify, make_response
from models.mensagens import Mensagem
from utils import db, ma
from flask_migrate import Migrate
from controllers.mensagens import mensagens_bp
from flask_marshmallow import Marshmallow
from marshmallow import ValidationError
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dados.db'
db.init_app(app)
app.json.sort_keys = False
migrate = Migrate(app, db)
app.register_blueprint(mensagens_bp, url_prefix="/mensagens")
ma.init_app(app)

def register_error_handlers(app):

    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        return jsonify({
            "error": "Validation Error",
            "mensagens": error.messages
        }), 400

    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        return jsonify({
            "error": error.name,
            "mensagem": error.description
        }), error.code

    @app.errorhandler(Exception)
    def handle_generic_exception(error):
        return jsonify({
            "error": "Internal Server Error",
            "mensagem": str(error)
        }), 500

register_error_handlers(app)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)