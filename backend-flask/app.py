import os
from flask import Flask, jsonify
from flask_cors import CORS
from models import db
from routes import bp


def create_app():
    # Permite usar pasta 'instance/' para o banco
    app = Flask(__name__, instance_relative_config=True)

    # Cria a pasta instance se não existir
    os.makedirs(app.instance_path, exist_ok=True)

    # Configuração do SQLite no diretório instance
    db_path = os.path.join(app.instance_path, 'restaurant.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializa extensões e cria tabelas
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # Habilita CORS e rotas
    CORS(app)
    app.register_blueprint(bp)

    @app.route('/')
    def health_check():
        return jsonify({'status': 'ok', 'message': 'API Flask rodando'}), 200

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)