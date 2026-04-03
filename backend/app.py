from flask import Flask
from config import Config
from flask_migrate import Migrate
from extensions import db, mail

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicialização
    db.init_app(app)
    Migrate(app, db)
    mail.init_app(app)

    # Registro de Blueprints 
    from routes.auth_routes import auth_bp
    from routes.user_routes import user_bp
    from routes.os_routes import os_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/usuarios')
    app.register_blueprint(os_bp, url_prefix='/os')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)