from flask import Flask, render_template, request, jsonify, send_file, session, redirect, url_for
from database import db, Chamado, Usuario
from reports import gerar_relatorio_mensal
from datetime import datetime, timedelta
from functools import wraps
import os

app = Flask(__name__)
app.secret_key = 'nvision_secret_2024_seguro'

# Configuração do banco de dados
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "chamados.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Criar banco de dados
with app.app_context():
    db.create_all()

    # Criar usuário padrão se não existir
    if not Usuario.query.filter_by(usuario='admin').first():
        admin = Usuario(
            usuario='admin',
            email='admin@nvision.com'
        )
        admin.definir_senha('admin123')
        db.session.add(admin)
        db.session.commit()
        print("✓ Usuário admin criado com sucesso!")
        print("  Usuário: admin")
        print("  Senha: admin123")


# Decorator para proteger rotas
def login_obrigatorio(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# Rotas de Autenticação
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if request.method == 'POST':
        usuario_nome = request.form.get('usuario')
        senha = request.form.get('senha')

        usuario = Usuario.query.filter_by(usuario=usuario_nome).first()

        if usuario and usuario.verificar_senha(senha) and usuario.ativo:
            session['usuario_id'] = usuario.id
            session['usuario_nome'] = usuario.usuario
            return redirect(url_for('index'))
        else:
            return render_template('login.html', erro='Usuário ou senha inválidos')

    return render_template('login.html')


@app.route('/logout')
def logout():
    """Logout"""
    session.clear()
    return redirect(url_for('login'))


@app.route('/')
@login_obrigatorio
def index():
    """Página inicial - Dashboard com formulário"""
    total_chamados = Chamado.query.count()
    chamados_abertos = Chamado.query.filter_by(status='aberto').count()

    # Últimos 10 chamados
    ultimos_chamados = Chamado.query.order_by(Chamado.data_criacao.desc()).limit(10).all()

    return render_template('index.html',
                         total_chamados=total_chamados,
                         chamados_abertos=chamados_abertos,
                         ultimos_chamados=ultimos_chamados)


@app.route('/api/chamados', methods=['POST'])
def criar_chamado():
    """API para criar novo chamado"""
    try:
        dados = request.json

        novo_chamado = Chamado(
            cliente=dados.get('cliente'),
            data_atendimento=datetime.fromisoformat(dados.get('data_atendimento')),
            categoria=dados.get('categoria'),
            descricao=dados.get('descricao'),
            tipo_atendimento=dados.get('tipo_atendimento', 'avulso'),
            valor_recebido=float(dados.get('valor_recebido', 0))
        )

        db.session.add(novo_chamado)
        db.session.commit()

        return jsonify({
            'sucesso': True,
            'mensagem': 'Chamado aberto com sucesso!',
            'chamado_id': novo_chamado.id
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'sucesso': False,
            'mensagem': f'Erro ao criar chamado: {str(e)}'
        }), 400


@app.route('/api/chamados', methods=['GET'])
def listar_chamados():
    """API para listar todos os chamados"""
    chamados = Chamado.query.order_by(Chamado.data_criacao.desc()).all()
    return jsonify([c.to_dict() for c in chamados])


@app.route('/api/chamados/<int:chamado_id>', methods=['GET'])
def obter_chamado(chamado_id):
    """API para obter detalhes de um chamado"""
    chamado = Chamado.query.get(chamado_id)
    if not chamado:
        return jsonify({'erro': 'Chamado não encontrado'}), 404
    return jsonify(chamado.to_dict())


@app.route('/api/chamados/<int:chamado_id>/status', methods=['PATCH'])
def atualizar_status(chamado_id):
    """API para atualizar status do chamado"""
    try:
        chamado = Chamado.query.get(chamado_id)
        if not chamado:
            return jsonify({'erro': 'Chamado não encontrado'}), 404

        dados = request.json
        novo_status = dados.get('status', 'aberto')

        if novo_status not in ['aberto', 'em_progresso', 'fechado']:
            return jsonify({'erro': 'Status inválido'}), 400

        chamado.status = novo_status
        db.session.commit()

        return jsonify({
            'sucesso': True,
            'mensagem': 'Status atualizado com sucesso'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 400


@app.route('/api/chamados/<int:chamado_id>', methods=['PUT'])
def editar_chamado(chamado_id):
    """API para editar um chamado"""
    try:
        chamado = Chamado.query.get(chamado_id)
        if not chamado:
            return jsonify({'erro': 'Chamado não encontrado'}), 404

        dados = request.json
        chamado.cliente = dados.get('cliente', chamado.cliente)
        chamado.categoria = dados.get('categoria', chamado.categoria)
        chamado.descricao = dados.get('descricao', chamado.descricao)
        chamado.tipo_atendimento = dados.get('tipo_atendimento', chamado.tipo_atendimento)
        chamado.valor_recebido = float(dados.get('valor_recebido', chamado.valor_recebido))
        chamado.tempo_gasto_minutos = int(dados.get('tempo_gasto_minutos', chamado.tempo_gasto_minutos))
        chamado.status = dados.get('status', chamado.status)

        db.session.commit()

        return jsonify({
            'sucesso': True,
            'mensagem': 'Chamado atualizado com sucesso'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 400


@app.route('/api/chamados/<int:chamado_id>', methods=['DELETE'])
def deletar_chamado(chamado_id):
    """API para deletar um chamado"""
    try:
        chamado = Chamado.query.get(chamado_id)
        if not chamado:
            return jsonify({'erro': 'Chamado não encontrado'}), 404

        db.session.delete(chamado)
        db.session.commit()

        return jsonify({
            'sucesso': True,
            'mensagem': 'Chamado deletado com sucesso'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 400


@app.route('/relatorio')
def relatorio():
    """Página de relatórios"""
    mes = request.args.get('mes', datetime.now().month, type=int)
    ano = request.args.get('ano', datetime.now().year, type=int)

    # Dados para o mês
    inicio = datetime(ano, mes, 1)
    if mes == 12:
        fim = datetime(ano + 1, 1, 1)
    else:
        fim = datetime(ano, mes + 1, 1)

    chamados_mes = Chamado.query.filter(
        Chamado.data_criacao >= inicio,
        Chamado.data_criacao < fim
    ).all()

    # Contar por cliente
    clientes_stats = {}
    for chamado in chamados_mes:
        if chamado.cliente not in clientes_stats:
            clientes_stats[chamado.cliente] = 0
        clientes_stats[chamado.cliente] += 1

    # Contar por categoria
    categorias_stats = {}
    for chamado in chamados_mes:
        if chamado.categoria not in categorias_stats:
            categorias_stats[chamado.categoria] = 0
        categorias_stats[chamado.categoria] += 1

    total_chamados_mes = len(chamados_mes)

    return render_template('relatorio.html',
                         mes=mes,
                         ano=ano,
                         total_chamados=total_chamados_mes,
                         clientes_stats=clientes_stats,
                         categorias_stats=categorias_stats,
                         chamados=chamados_mes)


@app.route('/relatorio/pdf')
def gerar_pdf():
    """Gera PDF do relatório mensal"""
    mes = request.args.get('mes', datetime.now().month, type=int)
    ano = request.args.get('ano', datetime.now().year, type=int)

    arquivo_pdf = gerar_relatorio_mensal(mes, ano)

    return send_file(
        arquivo_pdf,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'Relatorio_Atendimentos_{mes:02d}_{ano}.pdf'
    )


@app.route('/relatorio-cliente')
def relatorio_cliente():
    """Relatório detalhado por cliente"""
    from reports import gerar_relatorio_cliente_pdf
    mes = request.args.get('mes', datetime.now().month, type=int)
    ano = request.args.get('ano', datetime.now().year, type=int)

    inicio = datetime(ano, mes, 1)
    if mes == 12:
        fim = datetime(ano + 1, 1, 1)
    else:
        fim = datetime(ano, mes + 1, 1)

    chamados = Chamado.query.filter(Chamado.data_criacao >= inicio, Chamado.data_criacao < fim).all()

    clientes = {}
    total_contrato = 0
    total_avulso = 0

    for chamado in chamados:
        if chamado.cliente not in clientes:
            clientes[chamado.cliente] = {'contrato': [], 'avulso': [], 'total_contrato': 0, 'total_avulso': 0}

        if chamado.tipo_atendimento == 'contrato':
            clientes[chamado.cliente]['contrato'].append(chamado)
            clientes[chamado.cliente]['total_contrato'] += chamado.valor_recebido
            total_contrato += chamado.valor_recebido
        else:
            clientes[chamado.cliente]['avulso'].append(chamado)
            clientes[chamado.cliente]['total_avulso'] += chamado.valor_recebido
            total_avulso += chamado.valor_recebido

    return render_template('relatorio_cliente.html',
                         mes=mes,
                         ano=ano,
                         clientes=clientes,
                         total_contrato=total_contrato,
                         total_avulso=total_avulso)


@app.route('/relatorio-cliente/pdf')
def gerar_relatorio_cliente_pdf_route():
    """Gera PDF do relatório por cliente"""
    from reports import gerar_relatorio_cliente_pdf
    mes = request.args.get('mes', datetime.now().month, type=int)
    ano = request.args.get('ano', datetime.now().year, type=int)
    arquivo_pdf = gerar_relatorio_cliente_pdf(mes, ano)
    return send_file(arquivo_pdf, mimetype='application/pdf', as_attachment=True, download_name=f'Relatorio_Clientes_{mes:02d}_{ano}.pdf')


@app.route('/relatorio-receita')
def relatorio_receita():
    """Relatório de receita por cliente"""
    mes = request.args.get('mes', datetime.now().month, type=int)
    ano = request.args.get('ano', datetime.now().year, type=int)

    # Dados para o mês
    inicio = datetime(ano, mes, 1)
    if mes == 12:
        fim = datetime(ano + 1, 1, 1)
    else:
        fim = datetime(ano, mes + 1, 1)

    chamados = Chamado.query.filter(
        Chamado.data_criacao >= inicio,
        Chamado.data_criacao < fim
    ).order_by(Chamado.data_criacao.desc()).all()

    # Agrupar por cliente e calcular receita
    receita_clientes = {}
    receita_total = 0

    for chamado in chamados:
        if chamado.cliente not in receita_clientes:
            receita_clientes[chamado.cliente] = 0
        receita_clientes[chamado.cliente] += chamado.valor_recebido
        receita_total += chamado.valor_recebido

    # Ordenar por receita (maior primeiro)
    receita_ordenada = sorted(receita_clientes.items(), key=lambda x: x[1], reverse=True)

    return render_template('relatorio_receita.html',
                         mes=mes,
                         ano=ano,
                         receita_clientes=receita_ordenada,
                         receita_total=receita_total,
                         total_chamados=len(chamados))


@app.route('/relatorio-receita/pdf')
def gerar_relatorio_receita_pdf():
    """Gera PDF do relatório de receita"""
    from reports import gerar_relatorio_receita_pdf
    mes = request.args.get('mes', datetime.now().month, type=int)
    ano = request.args.get('ano', datetime.now().year, type=int)
    arquivo_pdf = gerar_relatorio_receita_pdf(mes, ano)
    return send_file(arquivo_pdf, mimetype='application/pdf', as_attachment=True, download_name=f'Relatorio_Receita_{mes:02d}_{ano}.pdf')


@app.route('/listagem')
def listagem():
    """Página de listagem de chamados"""
    filtro_status = request.args.get('status', 'todos')
    filtro_cliente = request.args.get('cliente', '')

    query = Chamado.query

    if filtro_status != 'todos':
        query = query.filter_by(status=filtro_status)

    if filtro_cliente:
        query = query.filter(Chamado.cliente.ilike(f'%{filtro_cliente}%'))

    chamados = query.order_by(Chamado.data_criacao.desc()).all()

    return render_template('listagem.html',
                         chamados=chamados,
                         filtro_status=filtro_status,
                         filtro_cliente=filtro_cliente)


# Rotas de Gerenciamento de Usuários
@app.route('/admin/usuarios')
@login_obrigatorio
def listar_usuarios():
    """Lista todos os usuários"""
    usuarios = Usuario.query.all()
    return render_template('admin_usuarios.html', usuarios=usuarios)


@app.route('/api/usuarios', methods=['POST'])
@login_obrigatorio
def criar_usuario():
    """Criar novo usuário"""
    try:
        dados = request.json

        # Verificar se usuário já existe
        if Usuario.query.filter_by(usuario=dados.get('usuario')).first():
            return jsonify({'sucesso': False, 'erro': 'Usuário já existe'}), 400

        if Usuario.query.filter_by(email=dados.get('email')).first():
            return jsonify({'sucesso': False, 'erro': 'Email já registrado'}), 400

        novo_usuario = Usuario(
            usuario=dados.get('usuario'),
            email=dados.get('email')
        )
        novo_usuario.definir_senha(dados.get('senha'))

        db.session.add(novo_usuario)
        db.session.commit()

        return jsonify({'sucesso': True, 'mensagem': 'Usuário criado com sucesso'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'sucesso': False, 'erro': str(e)}), 400


@app.route('/api/usuarios/<int:usuario_id>', methods=['PUT'])
@login_obrigatorio
def editar_usuario(usuario_id):
    """Editar usuário"""
    try:
        usuario = Usuario.query.get(usuario_id)
        if not usuario:
            return jsonify({'erro': 'Usuário não encontrado'}), 404

        dados = request.json
        usuario.email = dados.get('email', usuario.email)

        if dados.get('nova_senha'):
            usuario.definir_senha(dados.get('nova_senha'))

        if 'ativo' in dados:
            usuario.ativo = dados.get('ativo')

        db.session.commit()

        return jsonify({'sucesso': True, 'mensagem': 'Usuário atualizado com sucesso'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 400


@app.route('/api/usuarios/<int:usuario_id>', methods=['DELETE'])
@login_obrigatorio
def deletar_usuario(usuario_id):
    """Deletar usuário"""
    try:
        usuario = Usuario.query.get(usuario_id)
        if not usuario:
            return jsonify({'erro': 'Usuário não encontrado'}), 404

        db.session.delete(usuario)
        db.session.commit()

        return jsonify({'sucesso': True, 'mensagem': 'Usuário deletado com sucesso'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 400


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
