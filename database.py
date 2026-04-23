from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    senha_hash = db.Column(db.String(255), nullable=False)
    ativo = db.Column(db.Boolean, default=True)
    data_criacao = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return f'<Usuario {self.usuario}>'

    def definir_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def verificar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

class Chamado(db.Model):
    __tablename__ = 'chamados'

    id = db.Column(db.Integer, primary_key=True)
    cliente = db.Column(db.String(150), nullable=False)
    data_atendimento = db.Column(db.DateTime, nullable=False, default=datetime.now)
    categoria = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    tipo_atendimento = db.Column(db.String(20), default='avulso')  # contrato ou avulso
    valor_recebido = db.Column(db.Float, default=0.0)
    tempo_gasto_minutos = db.Column(db.Integer, default=0)  # tempo técnico em minutos
    status = db.Column(db.String(20), default='aberto')
    data_criacao = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return f'<Chamado {self.id} - {self.cliente}>'

    def to_dict(self):
        horas = self.tempo_gasto_minutos // 60
        minutos = self.tempo_gasto_minutos % 60
        tempo_formatado = f'{horas}h {minutos}m' if horas > 0 else f'{minutos}m'

        return {
            'id': self.id,
            'cliente': self.cliente,
            'data_atendimento': self.data_atendimento.strftime('%d/%m/%Y %H:%M'),
            'categoria': self.categoria,
            'descricao': self.descricao,
            'tipo_atendimento': self.tipo_atendimento,
            'valor_recebido': f'R$ {self.valor_recebido:.2f}',
            'tempo_gasto_minutos': self.tempo_gasto_minutos,
            'tempo_formatado': tempo_formatado,
            'status': self.status,
            'data_criacao': self.data_criacao.strftime('%d/%m/%Y %H:%M')
        }
