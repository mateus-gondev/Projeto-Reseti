from datetime import datetime
from flask import Blueprint, request, jsonify # type: ignore
from extensions import db
from models import Reserva, Equipamento, CriarOS

dash_bp = Blueprint('dashboard', __name__)

@dash_bp.route('/dados/stats', methods=['GET'])
def get_stats():
    CriarOS_pendentes = CriarOS.query.filter_by(status='Pendente').count()
    equip_uso = Equipamento.query.filter_by(status='Reservado').count()
    
    hoje = datetime.utcnow().date()
    reservas_hoje = Reserva.query.filter(
        db.func.date(Reserva.data_inicio) == hoje
    ).count()

    # EquipamentCriarOS Manutenções 
    manutencoes_query = Equipamento.query.filter_by(status='Manutenção').limit(2).all()
    lista_manutencoes = [
        {"id": m.id_equip, "nome": m.nome, "progresso": 75} 
        for m in manutencoes_query
    ]

    # Atividade do Sistema
    total_CriarOS = CriarOS.query.count()
    atividade_calc = 100
    if total_CriarOS > 0:
        resolvidas = CriarOS.query.filter(CriarOS.status != 'Pendente').count()
        atividade_calc = int((resolvidas / total_CriarOS) * 100)

    return jsonify({
        "os_pendentes": CriarOS_pendentes,     
        "equipamentos_uso": equip_uso,     
        "reservas_hoje": reservas_hoje,
        "atividade": atividade_calc,
        "manutencoes": lista_manutencoes
    })