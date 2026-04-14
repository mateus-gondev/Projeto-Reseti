# Rotas para trabalhar as Reservas do Usuário
from flask import Blueprint, request, jsonify # type: ignore
from extensions import db, socketio
from models import Reserva, Equipamento, Usuario
from datetime import datetime
from utils import token_required 

reserva_bp = Blueprint('reservas', __name__)

#  CRIA UMA RESERVA 
@reserva_bp.route('/', methods=['POST'])
@token_required # Aqui informa que precisa do token para execultar a ação
def criar_reserva(current_user_id):
    data = request.get_json()
    
    # Verifica se o equipamento existe e se está disponível
    equipamento = Equipamento.query.get(data.get('id_equip'))
    if not equipamento:
        return jsonify({"error": "Equipamento não encontrado"}), 404
    
    if equipamento.status != 'Disponível':
        return jsonify({"error": "Este equipamento não está disponível para reserva"}), 400

    try:
        inicio = datetime.fromisoformat(data.get('data_inicio'))
        fim = datetime.fromisoformat(data.get('data_fim'))
    except ValueError:
        return jsonify({"error": "Formato de data inválido. Use AAAA-MM-DD THH:MM:SS"}), 400

    nova_reserva = Reserva(
        id_user=current_user_id, 
        id_equip=data.get('id_equip'),
        data_inicio=inicio,
        data_fim=fim,
        observacao=data.get('observacao'),
        status='Em Reserva' 
    )

    equipamento.status = 'Reservado'

    db.session.add(nova_reserva)
    db.session.commit()
    
    socketio.emit('atualizar_lista', {'tipo': 'reserva_criada'}, namespace='/')

    return jsonify({"message": "Reserva realizada com sucesso e equipamento bloqueado!"}), 201

# VER MINHAS RESERVAS 
@reserva_bp.route('/minhas-reservas/<int:id_user>', methods=['GET'])
def listar_minhas_reservas(id_user):
    reservas = Reserva.query.filter_by(id_user=id_user).all()
    output = []
    
    for res in reservas:
        equip = Equipamento.query.get(res.id_equip)
        output.append({
            'id_reserva': res.id_reserva,
            'equipamento': equip.nome if equip else "Removido",
            'data_inicio': res.data_inicio.strftime('%d/%m/%Y %H:%M'),
            'data_fim': res.data_fim.strftime('%d/%m/%Y %H:%M'),
            'observacao': res.observacao,
            'status': res.status
        })
    
    return jsonify(output), 200

# VER TODAS AS RESERVAS (ADM) 
@reserva_bp.route('/todas', methods=['GET'])
def listar_todas_reservas():
    reservas = Reserva.query.all()
    output = []
    
    for res in reservas:
        user = Usuario.query.get(res.id_user)
        equip = Equipamento.query.get(res.id_equip)
        output.append({
            'id_reserva': res.id_reserva,
            'solicitante': user.nome if user else "Desconhecido",
            'equipamento': equip.nome if equip else "Desconhecido",
            'inicio': res.data_inicio.strftime('%d/%m/%Y %H:%M'),
            'fim': res.data_fim.strftime('%d/%m/%Y %H:%M'),
            'observacao': res.observacao,
            'status': res.status
        })
    
    return jsonify(output), 200

# EDITAR RESERVA 
@reserva_bp.route('/<int:id>', methods=['PUT'])
def atualizar_reserva(id):
    data = request.get_json()
    reserva = Reserva.query.get_or_404(id)
    
    # Se o usuário estiver trocando o equipamento na edição
    novo_id_equip = data.get('id_equip')
    if novo_id_equip and novo_id_equip != reserva.id_equip:
        
        # Libera o equipamento antigo
        equip_antigo = Equipamento.query.get(reserva.id_equip)
        if equip_antigo:
            equip_antigo.status = 'Disponível'
        
        # Verifica e bloqueia o novo equipamento
        novo_equip = Equipamento.query.get(novo_id_equip)
        if not novo_equip or novo_equip.status != 'Disponível':
            return jsonify({"error": "O novo equipamento não está disponível"}), 400
        
        novo_equip.status = 'Reservado'
        reserva.id_equip = novo_id_equip

    # Atualiza os demais campos se eles existirem no JSON
    if data.get('data_inicio'):
        reserva.data_inicio = datetime.fromisoformat(data.get('data_inicio'))
    if data.get('data_fim'):
        reserva.data_fim = datetime.fromisoformat(data.get('data_fim'))
    
    reserva.observacao = data.get('observacao', reserva.observacao)
    reserva.status = data.get('status', reserva.status)

    db.session.commit()
    
    socketio.emit('atualizar_lista', {'tipo': 'reserva_editada'}, namespace='/')
    
    return jsonify({"message": "Reserva atualizada com sucesso!"}), 200

# FINALIZAR OU CANCELAR RESERVA 
@reserva_bp.route('/<int:id>', methods=['DELETE'])
@token_required
def cancelar_reserva(current_user_id, id):
    reserva = Reserva.query.get_or_404(id)
    equipamento = Equipamento.query.get(reserva.id_equip)
    
    from models import Usuario 
    user_logado = Usuario.query.get(current_user_id)

    if reserva.id_user != current_user_id and user_logado.permissao != 'Adm':
        return jsonify({"error": "Acesso negado: você não é o dono desta reserva"}), 403

    if equipamento:
        equipamento.status = 'Disponível'

    db.session.delete(reserva)
    db.session.commit()
    
    socketio.emit('atualizar_lista', {'tipo': 'reserva_cancelada'}, namespace='/')
    
    return jsonify({"message": "Reserva cancelada e equipamento liberado!"}), 200