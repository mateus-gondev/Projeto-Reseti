# Definição das tabelas

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from extensions import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id_user = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    setor_curso = db.Column(db.String(100))
    senha = db.Column(db.String(255), nullable=False)
    permissao = db.Column(db.String(20), default='Comum') # Adm ou Comum
    status = db.Column(db.String(20), default='Ativo')

    # Relacionamentos
    reservas = db.relationship('Reserva', backref='usuario', lazy=True)
    ordens_servico = db.relationship('CriarOS', backref='usuario', lazy=True)

class Equipamento(db.Model):
    __tablename__ = 'equipamentos'
    id_equip = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    numero_serie = db.Column(db.String(50), unique=True)
    observacao = db.Column(db.Text)
    status = db.Column(db.String(20), default='Disponível')

class CriarOS(db.Model):
    __tablename__ = 'ordens_servico'
    id_os = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('usuarios.id_user'), nullable=False)
    numero_os = db.Column(db.String(50), unique=True)
    tipo_suporte = db.Column(db.String(50))
    assunto = db.Column(db.String(150))
    descricao = db.Column(db.Text)
    prioridade = db.Column(db.String(20))
    status = db.Column(db.String(20), default='Ativo')
    data_inicio = db.Column(db.DateTime, default=datetime.utcnow)
    data_fim = db.Column(db.DateTime)

class Reserva(db.Model):
    __tablename__ = 'reservas'
    id_reserva = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('usuarios.id_user'), nullable=False)
    id_equip = db.Column(db.Integer, db.ForeignKey('equipamentos.id_equip'), nullable=False)
    data_inicio = db.Column(db.DateTime, nullable=False)
    data_fim = db.Column(db.DateTime, nullable=False)
    observacao = db.Column(db.Text)
    status = db.Column(db.String(20), default='Pendente')