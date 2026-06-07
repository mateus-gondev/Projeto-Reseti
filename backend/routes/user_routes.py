
# AQUI NÓS ADMINISTRADORES REALIZAREMOS O CRUD DOS USUÁRIOS NO SISTEMA.
from flask import Blueprint, request, jsonify # type: ignore
from werkzeug.security import generate_password_hash # type: ignore
from extensions import db
from models import Usuario

user_bp = Blueprint('users', __name__)

# LISTAR TODOS OS USUÁRIOS
@user_bp.route('/', methods=['GET'])
def get_users():
    db.session.expire_all()
    usuarios = Usuario.query.order_by(Usuario.id_user).all()
    output = []
    for user in usuarios:
        output.append({
            'id_user': user.id_user,
            'nome': user.nome,
            'email': user.email,
            'setor_curso': user.setor_curso,
            'permissao': user.permissao,
            'status': user.status,
        })

    response = jsonify(output)
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    return response, 200

# BUSCAR USUÁRIO POR ID
@user_bp.route('/<int:id>', methods=['GET'])
def get_user(id):
    usuario = Usuario.query.get_or_404(id)

    return jsonify({
        'id_user': usuario.id_user,
        'nome': usuario.nome,
        'email': usuario.email,
        'setor_curso': usuario.setor_curso,
        'permissao': usuario.permissao,
        'status': usuario.status,
    }), 200

# CRIAR NOVO USUÁRIO PELO ADM 
@user_bp.route('/', methods=['POST'])
def create_user_admin():
    data = request.get_json()
    
    if Usuario.query.filter_by(email=data.get('email')).first():
        return jsonify({"error": "E-mail já cadastrado"}), 400

    hashed_password = generate_password_hash(data.get('senha'), method='pbkdf2:sha256')

    novo_usuario = Usuario(
        nome=data.get('nome'),
        email=data.get('email'),
        setor_curso=data.get('setor_curso'),
        senha=hashed_password,
        permissao=data.get('permissao', 'Comum'),
        status=data.get('status', 'Ativo')
    )

    db.session.add(novo_usuario)
    db.session.commit()

    return jsonify({"message": "Usuário criado com sucesso pelo administrador!"}), 201

# EDITAR USUÁRIO
@user_bp.route('/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    usuario = Usuario.query.get_or_404(id)

    usuario.nome = data.get('nome', usuario.nome)
    usuario.email = data.get('email', usuario.email)
    usuario.setor_curso = data.get('setor_curso', usuario.setor_curso)
    usuario.permissao = data.get('permissao', usuario.permissao)
    usuario.status = data.get('status', usuario.status)

    # Aqui o Adm reseta a senha
    if data.get('senha'):
        usuario.senha = generate_password_hash(data.get('senha'), method='pbkdf2:sha256')

    db.session.commit()
    db.session.refresh(usuario)

    return jsonify({
        "message": "Usuário atualizado com sucesso!",
        "user": {
            'id_user': usuario.id_user,
            'nome': usuario.nome,
            'email': usuario.email,
            'setor_curso': usuario.setor_curso,
            'permissao': usuario.permissao,
            'status': usuario.status,
        },
    }), 200

# REMOVER USUÁRIO
@user_bp.route('/<int:id>', methods=['DELETE'])
def delete_user(id):
    usuario = Usuario.query.get_or_404(id)
    
    db.session.delete(usuario)
    db.session.commit()
    
    return jsonify({"message": f"Usuário {usuario.nome} removido com sucesso!"}), 200