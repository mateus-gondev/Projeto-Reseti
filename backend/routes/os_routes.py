
# Aqui trabalharemos com as Rotas de Ordem de Serviço (OS)
import os
import random
import uuid
from datetime import datetime

from flask import Blueprint, request, jsonify, current_app  # type: ignore
from sqlalchemy.exc import IntegrityError, SQLAlchemyError  # type: ignore
from werkzeug.utils import secure_filename  # type: ignore

from extensions import db
from models import CriarOS, Usuario

os_bp = Blueprint('os', __name__)

EXTENSOES_PERMITIDAS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx'}


def _arquivo_permitido(nome_arquivo):
    return '.' in nome_arquivo and nome_arquivo.rsplit('.', 1)[1].lower() in EXTENSOES_PERMITIDAS


def _salvar_anexo(arquivo):
    """Salva o anexo em disco local. Futuramente substituir por AWS S3 ou Supabase Storage."""
    if not arquivo or arquivo.filename == '':
        return None

    if not _arquivo_permitido(arquivo.filename):
        raise ValueError('Tipo de arquivo não permitido. Use imagens, PDF ou documentos Word.')

    pasta_upload = os.path.join(current_app.root_path, 'uploads', 'os')
    os.makedirs(pasta_upload, exist_ok=True)

    nome_seguro = secure_filename(arquivo.filename)
    nome_unico = f"{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}_{nome_seguro}"
    caminho_completo = os.path.join(pasta_upload, nome_unico)

    arquivo.save(caminho_completo)

    # Caminho relativo salvo no banco — em produção, trocar por URL pública do bucket na nuvem
    return f"uploads/os/{nome_unico}"


def _remover_anexo(caminho_relativo):
    if not caminho_relativo:
        return

    caminho_completo = os.path.join(current_app.root_path, caminho_relativo.replace('/', os.sep))
    if os.path.exists(caminho_completo):
        os.remove(caminho_completo)


def _gerar_numero_os():
    """Gera número único evitando colisão na restrição unique=True do banco."""
    ano_atual = datetime.now().year

    for _ in range(10):
        numero = f"OS-{ano_atual}-{random.randint(1000, 9999)}"
        if not CriarOS.query.filter_by(numero_os=numero).first():
            return numero

    return f"OS-{ano_atual}-{uuid.uuid4().hex[:8].upper()}"


# ABERTURA DE ORDEM DE SERVIÇO
@os_bp.route('/', methods=['POST'])
def abrir_os():
    id_usuario_logado = request.form.get('id_user')
    tipo_suporte = request.form.get('tipo_suporte', '').strip()
    assunto = request.form.get('assunto', '').strip()
    descricao = request.form.get('descricao', '').strip()
    prioridade = request.form.get('prioridade', '').strip()
    arquivo_anexo = request.files.get('anexo')
    caminho_anexo = None

    # VALIDAÇÃO DOS CAMPOS OBRIGATÓRIOS
    if not id_usuario_logado:
        return jsonify({"error": "Usuário não identificado"}), 400

    try:
        id_usuario_logado = int(id_usuario_logado)
    except (TypeError, ValueError):
        return jsonify({"error": "Identificador de usuário inválido"}), 400

    if not tipo_suporte or not assunto or not descricao or not prioridade:
        return jsonify({"error": "Preencha todos os campos obrigatórios"}), 400

    usuario = Usuario.query.get(id_usuario_logado)
    if not usuario:
        return jsonify({"error": "Usuário não encontrado"}), 404

    # SALVAR ANEXO (SE ENVIADO)
    if arquivo_anexo and arquivo_anexo.filename:
        try:
            caminho_anexo = _salvar_anexo(arquivo_anexo)
        except ValueError as erro:
            return jsonify({"error": str(erro)}), 400

    # GERAR NÚMERO DE OS ÚNICO E PERSISTIR NO BANCO
    numero_gerado = _gerar_numero_os()

    nova_os = CriarOS(
        id_user=usuario.id_user,
        numero_os=numero_gerado,
        tipo_suporte=tipo_suporte,
        assunto=assunto,
        descricao=descricao,
        prioridade=prioridade,
        anexo=caminho_anexo,
        status='Ativo'
    )

    try:
        db.session.add(nova_os)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        _remover_anexo(caminho_anexo)
        return jsonify({"error": "Número de OS duplicado. Tente novamente."}), 409
    except SQLAlchemyError as erro:
        db.session.rollback()
        _remover_anexo(caminho_anexo)
        mensagem = str(erro.orig) if getattr(erro, 'orig', None) else "Falha ao salvar a Ordem de Serviço no banco."
        return jsonify({"error": mensagem}), 500

    return jsonify({
        "message": "Ordem de Serviço aberta com sucesso!",
        "numero_os": numero_gerado,
        "anexo": caminho_anexo,
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
