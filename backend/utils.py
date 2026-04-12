from functools import wraps
from flask import request, jsonify, current_app # type: ignore
import jwt

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']

            # Divide "Bearer <token>"
            token = auth_header.split(" ")[1] if " " in auth_header else None

        if not token:
            return jsonify({'error': 'Token de acesso ausente!'}), 401

        try:
            # Decodifica usando a SECRET_KEY 
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user_id = data['public_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'O token expirou!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token inválido!'}), 401
        except Exception as e:
            return jsonify({'error': f'Erro ao validar token: {str(e)}'}), 401

        # Passa o ID do usuário para a função da rota
        return f(current_user_id, *args, **kwargs)

    return decorated