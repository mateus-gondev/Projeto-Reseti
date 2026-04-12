from flask_sqlalchemy import SQLAlchemy # type: ignore
from flask_mail import Mail # type: ignore
from flask_socketio import SocketIO # type: ignore

db = SQLAlchemy()
mail = Mail()
socketio = SocketIO(cors_allowed_origins="*")
