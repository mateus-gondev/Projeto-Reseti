
# Aqui trabalharemos com as Rotas de Ordem de Serviço (OS)
from flask import Blueprint, request, jsonify
from extensions import db
from models import CriarOS, Usuario
from datetime import datetime
import random # Para gerar um número de OS aleatório simples

os_bp = Blueprint('os', __name__)

# ABERTURA DE ORDEM DE SERVIÇO
@os_bp.route('/', methods=['POST'])
def abrir_os():
    data = request.get_json()
    id_usuario_logado = data.get('id_user') 

    usuario = Usuario.query.get(id_usuario_logado)
    if not usuario:
        return jsonify({"error": "Usuário não encontrado"}), 404

    # Gerar um número de OS único (Ano + Codigo Aleatorio)
    numero_gerado = f"OS-{datetime.now().year}-{random.randint(1000, 9999)}"

    nova_os = CriarOS(
        id_user=usuario.id_user,
        numero_os=numero_gerado,
        tipo_suporte=data.get('tipo_suporte'),
        assunto=data.get('assunto'),
        descricao=data.get('descricao'),
        prioridade=data.get('prioridade'),
        status='Ativo' 
    )

    db.session.add(nova_os)
    db.session.commit()

    return jsonify({
        "message": "Ordem de Serviço aberta com sucesso!",
        "numero_os": numero_gerado,
        "usuario_solicitante": {
            "nome": usuario.nome,
            "email": usuario.email,
            "setor": usuario.setor_curso
        }
    }), 201

# VER MINHAS OS 
@os_bp.route('/minhas-os/<int:id_user>', methods=['GET'])
def ver_minhas_os(id_user):
    ordens = CriarOS.query.filter_by(id_user=id_user).all()
    
    output = []
    for ordem in ordens: 
        output.append({
            "numero_os": ordem.numero_os,
            "assunto": ordem.assunto,
            "status": ordem.status,
            "data_inicio": ordem.data_inicio.strftime('%d/%m/%Y %H:%M')
        })
    
    return jsonify(output), 200

# VER TODAS AS OS (EXCLUSIVO ADM) 
@os_bp.route('/todas', methods=['GET'])
def ver_todas_os():
    # TODO Aqui futuramente checaremos quem é ADM
    todas_os = CriarOS.query.all()
    
    output = []
    for os in todas_os:
        usuario = Usuario.query.get(os.id_user)
        
        output.append({
            "id_os": os.id_os,
            "numero_os": os.numero_os,
            "solicitante": usuario.nome,
            "setor": usuario.setor_curso,
            "assunto": os.assunto,
            "status": os.status,
            "prioridade": os.prioridade
        })
    
    return jsonify(output), 200

# EDITAR ORDEM DE SERVIÇO
@os_bp.route('/<int:id>', methods=['PUT'])
def editar_os(id):
    data = request.get_json()
    ordem = CriarOS.query.get_or_404(id)

    ordem.tipo_suporte = data.get('tipo_suporte', ordem.tipo_suporte)
    ordem.assunto = data.get('assunto', ordem.assunto)
    ordem.descricao = data.get('descricao', ordem.descricao)
    ordem.prioridade = data.get('prioridade', ordem.prioridade)
    
    novo_status = data.get('status', ordem.status)
    if novo_status == 'Finalizado' and ordem.status != 'Finalizado':
        ordem.data_fim = datetime.utcnow()
    
    ordem.status = novo_status

    db.session.commit()
    return jsonify({"message": f"Ordem {ordem.numero_os} atualizada com sucesso!"}), 200

# REMOVER ORDEM DE SERVIÇO
@os_bp.route('/<int:id>', methods=['DELETE'])
def deletar_os(id):
    ordem = CriarOS.query.get_or_404(id)
    
    db.session.delete(ordem)
    db.session.commit()
    
    return jsonify({"message": f"Ordem {ordem.numero_os} removida do sistema!"}), 200