from flask import Flask # type: ignore
from config import Config
from flask_migrate import Migrate # type: ignore
from extensions import db, mail, socketio
from flask_cors import CORS  # type: ignore


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicialização
    db.init_app(app)
    Migrate(app, db)
    mail.init_app(app)
    #CORS(app, resources={r"/*": {"origins": ["http://localhost:5174", "http://localhost:5173"]}})
    CORS(app, resources={r"/*": {"origins": "*"}}) # Liberei para toda Rede
    socketio.init_app(app)
    
    # Registro de Blueprints 
    from routes.auth_routes import auth_bp
    from routes.user_routes import user_bp
    from routes.os_routes import os_bp
    from routes.equipamento_routes import equip_bp
    from routes.reserva_routes import reserva_bp
    from routes.dashboard import dash_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/usuarios')
    app.register_blueprint(os_bp, url_prefix='/os')
    app.register_blueprint(equip_bp, url_prefix='/equipamentos')
    app.register_blueprint(reserva_bp, url_prefix='/reservas')
    app.register_blueprint(dash_bp, url_prefix='/dashboard')

    return app

if __name__ == '__main__':
    app = create_app()
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)