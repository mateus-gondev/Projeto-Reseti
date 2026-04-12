
# Rotas para cadastrar os Equipamentos
import os
from flask import Blueprint, request, jsonify # type: ignore
from extensions import db
from models import Equipamento

equip_bp = Blueprint('equipamentos', __name__)

# LISTAR OS EQUIPAMENTOS
@equip_bp.route('/', methods=['GET'])
def listar_equipamentos():
    equipamentos = Equipamento.query.all()
    output = []
    
    for equip in equipamentos:
        output.append({
            'id_equip': equip.id_equip,
            'nome': equip.nome,
            'numero_serie': equip.numero_serie,
            'observacao': equip.observacao,
            'status': equip.status
        })
    
    return jsonify(output), 200

# CADASTRAR
@equip_bp.route('/', methods=['POST'])
def criar_equipamento():
    data = request.get_json()
    
    # Verifica se o número de série já existe 
    if Equipamento.query.filter_by(numero_serie=data.get('numero_serie')).first():
        return jsonify({"error": "Já existe um equipamento com este número de série"}), 400

    novo_equip = Equipamento(
        nome=data.get('nome'),
        numero_serie=data.get('numero_serie'),
        observacao=data.get('observacao'),
        status=data.get('status', 'Disponível') 
    )

    db.session.add(novo_equip)
    db.session.commit()

    return jsonify({"message": "Equipamento cadastrado com sucesso!", "id_equip": novo_equip.id_equip}), 201

# ATUALIZAR 
@equip_bp.route('/<int:id>', methods=['PUT'])
def atualizar_equipamento(id):
    data = request.get_json()
    equip = Equipamento.query.get_or_404(id)

    equip.nome = data.get('nome', equip.nome)
    equip.numero_serie = data.get('numero_serie', equip.numero_serie)
    equip.observacao = data.get('observacao', equip.observacao)
    equip.status = data.get('status', equip.status)

    db.session.commit()
    return jsonify({"message": "Equipamento atualizado com sucesso!"}), 200

# REMOVER 
@equip_bp.route('/<int:id>', methods=['DELETE'])
def deletar_equipamento(id):
    equip = Equipamento.query.get_or_404(id)
    
    db.session.delete(equip)
    db.session.commit()
    
    return jsonify({"message": f"Equipamento '{equip.nome}' removido com sucesso!"}), 200


@equip_bp.route('/dashboard/stats', methods=['GET'])
def get_stats():
    os_pendentes = os.query.filter_by(status='Pendente').count()
    equip_uso = Equipamento.query.filter_by(status='Reservado').count()
    
    return jsonify({
        "os_pendentes": os_pendentes,
        "equipamentos_uso": equip_uso,
        "reservas_hoje": 5, 
        "atividade": 92
    })