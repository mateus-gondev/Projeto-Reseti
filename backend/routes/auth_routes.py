
# Rotas para o Usuário Logar
from flask_mail import Message # type: ignore
from flask import Blueprint, request, jsonify, url_for, current_app # type: ignore
from werkzeug.security import generate_password_hash, check_password_hash # type: ignore
from itsdangerous import URLSafeTimedSerializer as Serializer # type: ignore
from extensions import db, mail 
from models import Usuario
import jwt 
import datetime

auth_bp = Blueprint('auth', __name__)

# CADASTRO 
@auth_bp.route('/cadastro', methods=['POST'])
def cadastro():
    data = request.get_json()
    
    # Aqui verifica se o usuário já existe
    if Usuario.query.filter_by(email=data.get('email')).first():
        return jsonify({"error": "E-mail já cadastrado"}), 400

    # Cria o hash da senha
    hashed_password = generate_password_hash(data.get('senha'), method='pbkdf2:sha256')

    novo_usuario = Usuario(
        nome=data.get('nome'),
        email=data.get('email'),
        setor_curso=data.get('setor_curso'),
        senha=hashed_password,
        permissao=data.get('permissao', 'Comum')
    )

    db.session.add(novo_usuario)
    db.session.commit()

    return jsonify({"message": "Usuário criado com sucesso!"}), 201

# LOGIN
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    usuario = Usuario.query.filter_by(email=data.get('email')).first()

    if not usuario or not check_password_hash(usuario.senha, data.get('senha')):
        return jsonify({"error": "Credenciais inválidas"}), 401

    token = jwt.encode({
        'public_id': usuario.id_user, 
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }, current_app.config['SECRET_KEY'], algorithm="HS256")

    return jsonify({
        "message": "Login realizado!",
        "token": token, 
        "user": {
            "nome": usuario.nome, 
            "permissao": usuario.permissao
        }
    }), 200


# Função auxiliar para gerar o token
def gerar_token_reset(email):
    s = Serializer(current_app.config['SECRET_KEY'])
    return s.dumps(email, salt='pw-reset-salt')


# Funçaõ para enviar mensagem ao Email
def enviar_email_reset(email_usuario, token):
    link_frontend = f"http://localhost:5173/reset-senha/{token}"
    
    msg = Message(
        subject="Recuperação de Senha - Projeto RESETI",
        recipients=[email_usuario],
        sender=current_app.config['MAIL_USERNAME'], 
        body=f"Para redefinir sua senha no RESETI, clique no link: {link_frontend}"
    )
    mail.send(msg)
        
    
# RESETE DE SENHA
@auth_bp.route('/reset-senha', methods=['POST'])
def reset_senha():
    data = request.get_json()
    usuario = Usuario.query.filter_by(email=data.get('email')).first()
    
    if usuario:
        s = Serializer(current_app.config['SECRET_KEY'])
        token = s.dumps(usuario.email, salt='pw-reset-salt')
        
        try:
            enviar_email_reset(usuario.email, token)
            return jsonify({"message": "E-mail de recuperação enviado com sucesso!"}), 200
        except Exception as e:
            return jsonify({"error": f"Falha ao enviar e-mail: {str(e)}"}), 500
    
    return jsonify({"error": "E-mail não encontrado"}), 404

# DEFINIR NOVA SENHA
@auth_bp.route('/reset-senha/<token>', methods=['POST'])
def reset_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        # O token expira em 30 minutos 
        email = s.loads(token, salt='pw-reset-salt', max_age=1800)
    except:
        return jsonify({"error": "Token inválido ou expirado"}), 400

    data = request.get_json()
    usuario = Usuario.query.filter_by(email=email).first()
    
    if usuario:
        usuario.senha = generate_password_hash(data.get('nova_senha'), method='pbkdf2:sha256')
        db.session.commit()
        return jsonify({"message": "Senha atualizada com sucesso!"}), 200
    
    return jsonify({"error": "Usuário não encontrado"}), 404