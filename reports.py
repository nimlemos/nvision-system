from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER
from database import db, Chamado
from datetime import datetime

def gerar_relatorio_mensal(mes, ano):
    inicio = datetime(ano, mes, 1)
    if mes == 12:
        fim = datetime(ano + 1, 1, 1)
    else:
        fim = datetime(ano, mes + 1, 1)

    chamados = Chamado.query.filter(Chamado.data_criacao >= inicio, Chamado.data_criacao < fim).all()

    arquivo_pdf = f'Relatorio_Atendimentos_{mes:02d}_{ano}.pdf'
    doc = SimpleDocTemplate(arquivo_pdf, pagesize=A4)
    story = []

    styles = getSampleStyleSheet()
    titulo_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=24, textColor=colors.HexColor('#1f4788'), spaceAfter=30, alignment=TA_CENTER, fontName='Helvetica-Bold')
    subtitulo_style = ParagraphStyle('CustomSubtitle', parent=styles['Heading2'], fontSize=14, textColor=colors.HexColor('#1f4788'), spaceAfter=12, fontName='Helvetica-Bold')

    meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    mes_nome = meses[mes - 1]

    story.append(Paragraph(f'Relatório de Atendimentos - {mes_nome} de {ano}', titulo_style))
    story.append(Spacer(1, 0.3*inch))

    total_chamados = len(chamados)
    clientes_count = {}
    categorias_count = {}

    for chamado in chamados:
        clientes_count[chamado.cliente] = clientes_count.get(chamado.cliente, 0) + 1
        categorias_count[chamado.categoria] = categorias_count.get(chamado.categoria, 0) + 1

    story.append(Paragraph('Resumo Executivo', subtitulo_style))
    resumo_data = [['Total de Chamados', f'{total_chamados}'], ['Clientes Atendidos', f'{len(clientes_count)}'], ['Categorias', f'{len(categorias_count)}']]
    resumo_table = Table(resumo_data, colWidths=[4*inch, 2*inch])
    resumo_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#e8f0f7')), ('TEXTCOLOR', (0, 0), (-1, -1), colors.black), ('ALIGN', (0, 0), (-1, -1), 'CENTER'), ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'), ('FONTSIZE', (0, 0), (-1, -1), 11), ('BOTTOMPADDING', (0, 0), (-1, -1), 12), ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
    story.append(resumo_table)
    story.append(Spacer(1, 0.3*inch))

    if clientes_count:
        story.append(PageBreak())
        story.append(Paragraph('Clientes com Mais Atendimentos', subtitulo_style))
        story.append(Spacer(1, 0.2*inch))
        clientes_ordenados = sorted(clientes_count.items(), key=lambda x: x[1], reverse=True)
        clientes_data = [['Cliente', 'Atendimentos', 'Percentual']]
        for cliente, count in clientes_ordenados:
            percentual = f"{(count / total_chamados * 100):.1f}%" if total_chamados > 0 else "0%"
            clientes_data.append([cliente, str(count), percentual])
        clientes_table = Table(clientes_data, colWidths=[3*inch, 1.5*inch, 1.5*inch])
        clientes_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')), ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke), ('ALIGN', (0, 0), (-1, -1), 'CENTER'), ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'), ('FONTSIZE', (0, 0), (-1, -1), 10), ('BOTTOMPADDING', (0, 0), (-1, 0), 12), ('BACKGROUND', (0, 1), (-1, -1), colors.beige), ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
        story.append(clientes_table)
        story.append(Spacer(1, 0.3*inch))

    if categorias_count:
        story.append(Paragraph('Distribuição por Categoria', subtitulo_style))
        story.append(Spacer(1, 0.2*inch))
        categorias_ordenadas = sorted(categorias_count.items(), key=lambda x: x[1], reverse=True)
        categorias_data = [['Categoria', 'Chamados', 'Percentual']]
        for categoria, count in categorias_ordenadas:
            percentual = f"{(count / total_chamados * 100):.1f}%" if total_chamados > 0 else "0%"
            categorias_data.append([categoria, str(count), percentual])
        categorias_table = Table(categorias_data, colWidths=[3*inch, 1.5*inch, 1.5*inch])
        categorias_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')), ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke), ('ALIGN', (0, 0), (-1, -1), 'CENTER'), ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'), ('FONTSIZE', (0, 0), (-1, -1), 10), ('BOTTOMPADDING', (0, 0), (-1, 0), 12), ('BACKGROUND', (0, 1), (-1, -1), colors.beige), ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
        story.append(categorias_table)

    if chamados:
        story.append(PageBreak())
        story.append(Paragraph('Detalhes de Todos os Chamados', subtitulo_style))
        story.append(Spacer(1, 0.2*inch))
        chamados_data = [['ID', 'Cliente', 'Categoria', 'Data', 'Status']]
        for chamado in chamados:
            chamados_data.append([str(chamado.id), chamado.cliente[:20], chamado.categoria, chamado.data_criacao.strftime('%d/%m/%Y'), chamado.status])
        chamados_table = Table(chamados_data, colWidths=[0.7*inch, 1.5*inch, 1.5*inch, 1.3*inch, 1.0*inch])
        chamados_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')), ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke), ('ALIGN', (0, 0), (-1, -1), 'CENTER'), ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'), ('FONTSIZE', (0, 0), (-1, -1), 9), ('BOTTOMPADDING', (0, 0), (-1, 0), 12), ('BACKGROUND', (0, 1), (-1, -1), colors.beige), ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
        story.append(chamados_table)

    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph(f'Relatório gerado em {datetime.now().strftime("%d/%m/%Y às %H:%M")}', styles['Normal']))

    doc.build(story)
    return arquivo_pdf


def gerar_relatorio_receita_pdf(mes, ano):
    """Gera relatório de receita por cliente"""
    inicio = datetime(ano, mes, 1)
    if mes == 12:
        fim = datetime(ano + 1, 1, 1)
    else:
        fim = datetime(ano, mes + 1, 1)

    chamados = Chamado.query.filter(Chamado.data_criacao >= inicio, Chamado.data_criacao < fim).all()

    arquivo_pdf = f'Relatorio_Receita_{mes:02d}_{ano}.pdf'
    doc = SimpleDocTemplate(arquivo_pdf, pagesize=A4)
    story = []

    styles = getSampleStyleSheet()
    titulo_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=24, textColor=colors.HexColor('#27ae60'), spaceAfter=30, alignment=TA_CENTER, fontName='Helvetica-Bold')
    subtitulo_style = ParagraphStyle('CustomSubtitle', parent=styles['Heading2'], fontSize=14, textColor=colors.HexColor('#229954'), spaceAfter=12, fontName='Helvetica-Bold')

    meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    mes_nome = meses[mes - 1]

    story.append(Paragraph(f'Relatório de Receita - {mes_nome} de {ano}', titulo_style))
    story.append(Spacer(1, 0.3*inch))

    # Calcular receita por cliente
    receita_clientes = {}
    receita_total = 0

    for chamado in chamados:
        if chamado.cliente not in receita_clientes:
            receita_clientes[chamado.cliente] = 0
        receita_clientes[chamado.cliente] += chamado.valor_recebido
        receita_total += chamado.valor_recebido

    # Resumo geral
    story.append(Paragraph('Resumo Geral', subtitulo_style))
    resumo_data = [
        ['Receita Total', f'R$ {receita_total:.2f}'],
        ['Clientes', f'{len(receita_clientes)}'],
        ['Chamados', f'{len(chamados)}']
    ]
    resumo_table = Table(resumo_data, colWidths=[4*inch, 2*inch])
    resumo_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 1), colors.HexColor('#e8f5e9')),
        ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#27ae60')),
        ('TEXTCOLOR', (0, 2), (-1, 2), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(resumo_table)
    story.append(Spacer(1, 0.3*inch))

    # Receita por cliente
    if receita_clientes:
        story.append(PageBreak())
        story.append(Paragraph('Receita por Cliente', subtitulo_style))
        story.append(Spacer(1, 0.2*inch))

        receita_ordenada = sorted(receita_clientes.items(), key=lambda x: x[1], reverse=True)
        receita_data = [['Cliente', 'Receita', 'Percentual']]

        for cliente, valor in receita_ordenada:
            percentual = f"{(valor / receita_total * 100):.1f}%" if receita_total > 0 else "0%"
            receita_data.append([cliente, f'R$ {valor:.2f}', percentual])

        receita_table = Table(receita_data, colWidths=[3*inch, 1.5*inch, 1.5*inch])
        receita_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27ae60')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#d5f4e6')),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(receita_table)
        story.append(Spacer(1, 0.3*inch))

        # Análise
        story.append(Paragraph('Análise de Receita', subtitulo_style))
        analise_data = [
            ['Ticket Médio', f'R$ {receita_total / len(chamados) if len(chamados) > 0 else 0:.2f}'],
            ['Receita Média por Cliente', f'R$ {receita_total / len(receita_clientes) if len(receita_clientes) > 0 else 0:.2f}'],
            ['Cliente com Maior Receita', f'{receita_ordenada[0][0] if receita_ordenada else "N/A"}']
        ]
        analise_table = Table(analise_data, colWidths=[3*inch, 3*inch])
        analise_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f39c12')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 1), (-1, 1), colors.white),
            ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#e74c3c')),
            ('TEXTCOLOR', (0, 2), (-1, 2), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(analise_table)

    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph(f'Relatório gerado em {datetime.now().strftime("%d/%m/%Y às %H:%M")}', styles['Normal']))

    doc.build(story)
    return arquivo_pdf


def gerar_relatorio_cliente_pdf(mes, ano):
    """Gera relatório detalhado por cliente com valores"""
    inicio = datetime(ano, mes, 1)
    if mes == 12:
        fim = datetime(ano + 1, 1, 1)
    else:
        fim = datetime(ano, mes + 1, 1)

    chamados = Chamado.query.filter(Chamado.data_criacao >= inicio, Chamado.data_criacao < fim).all()

    arquivo_pdf = f'Relatorio_Clientes_{mes:02d}_{ano}.pdf'
    doc = SimpleDocTemplate(arquivo_pdf, pagesize=A4)
    story = []

    styles = getSampleStyleSheet()
    titulo_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=24, textColor=colors.HexColor('#27ae60'), spaceAfter=30, alignment=TA_CENTER, fontName='Helvetica-Bold')
    subtitulo_style = ParagraphStyle('CustomSubtitle', parent=styles['Heading2'], fontSize=14, textColor=colors.HexColor('#229954'), spaceAfter=12, fontName='Helvetica-Bold')

    meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    mes_nome = meses[mes - 1]

    story.append(Paragraph(f'Relatório Detalhado por Cliente - {mes_nome} de {ano}', titulo_style))
    story.append(Spacer(1, 0.3*inch))

    clientes = {}
    total_geral_contrato = 0
    total_geral_avulso = 0

    for chamado in chamados:
        if chamado.cliente not in clientes:
            clientes[chamado.cliente] = {'contrato': [], 'avulso': [], 'total_contrato': 0, 'total_avulso': 0}

        if chamado.tipo_atendimento == 'contrato':
            clientes[chamado.cliente]['contrato'].append(chamado)
            clientes[chamado.cliente]['total_contrato'] += chamado.valor_recebido
            total_geral_contrato += chamado.valor_recebido
        else:
            clientes[chamado.cliente]['avulso'].append(chamado)
            clientes[chamado.cliente]['total_avulso'] += chamado.valor_recebido
            total_geral_avulso += chamado.valor_recebido

    # Resumo geral
    story.append(Paragraph('Resumo Geral', subtitulo_style))
    resumo_data = [
        ['Atendimentos Contrato', f'R$ {total_geral_contrato:.2f}'],
        ['Atendimentos Avulsos', f'R$ {total_geral_avulso:.2f}'],
        ['TOTAL', f'R$ {total_geral_contrato + total_geral_avulso:.2f}']
    ]
    resumo_table = Table(resumo_data, colWidths=[4*inch, 2*inch])
    resumo_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 1), colors.HexColor('#e8f5e9')),
        ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#27ae60')),
        ('TEXTCOLOR', (0, 2), (-1, 2), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(resumo_table)
    story.append(Spacer(1, 0.3*inch))

    # Por cliente
    for cliente in sorted(clientes.keys()):
        story.append(PageBreak())
        story.append(Paragraph(f'Cliente: {cliente}', subtitulo_style))
        story.append(Spacer(1, 0.2*inch))

        cliente_total = clientes[cliente]['total_contrato'] + clientes[cliente]['total_avulso']
        cliente_resumo = [
            ['Atendimentos Contrato', f'{len(clientes[cliente]["contrato"])}', f'R$ {clientes[cliente]["total_contrato"]:.2f}'],
            ['Atendimentos Avulsos', f'{len(clientes[cliente]["avulso"])}', f'R$ {clientes[cliente]["total_avulso"]:.2f}'],
            ['TOTAL', f'{len(clientes[cliente]["contrato"]) + len(clientes[cliente]["avulso"])}', f'R$ {cliente_total:.2f}']
        ]
        cliente_resumo_table = Table(cliente_resumo, colWidths=[2*inch, 1.5*inch, 1.5*inch])
        cliente_resumo_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 1), colors.HexColor('#e8f5e9')),
            ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#f39c12')),
            ('TEXTCOLOR', (0, 2), (-1, 2), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(cliente_resumo_table)
        story.append(Spacer(1, 0.3*inch))

        # Atendimentos contrato
        if clientes[cliente]['contrato']:
            story.append(Paragraph('Atendimentos com Contrato', styles['Heading3']))
            story.append(Spacer(1, 0.1*inch))
            contrato_data = [['Data', 'Categoria', 'Valor', 'Status']]
            for chamado in clientes[cliente]['contrato']:
                contrato_data.append([
                    chamado.data_criacao.strftime('%d/%m/%Y'),
                    chamado.categoria,
                    f'R$ {chamado.valor_recebido:.2f}',
                    chamado.status
                ])
            contrato_table = Table(contrato_data, colWidths=[1.5*inch, 2*inch, 1.5*inch, 1.5*inch])
            contrato_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27ae60')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#d5f4e6')),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(contrato_table)
            story.append(Spacer(1, 0.2*inch))

        # Atendimentos avulsos
        if clientes[cliente]['avulso']:
            story.append(Paragraph('Atendimentos Avulsos', styles['Heading3']))
            story.append(Spacer(1, 0.1*inch))
            avulso_data = [['Data', 'Categoria', 'Valor', 'Status']]
            for chamado in clientes[cliente]['avulso']:
                avulso_data.append([
                    chamado.data_criacao.strftime('%d/%m/%Y'),
                    chamado.categoria,
                    f'R$ {chamado.valor_recebido:.2f}',
                    chamado.status
                ])
            avulso_table = Table(avulso_data, colWidths=[1.5*inch, 2*inch, 1.5*inch, 1.5*inch])
            avulso_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e74c3c')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#fadbd8')),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(avulso_table)

    story.append(PageBreak())
    story.append(Paragraph(f'Relatório gerado em {datetime.now().strftime("%d/%m/%Y às %H:%M")}', styles['Normal']))

    doc.build(story)
    return arquivo_pdf


def gerar_relatorio_receita_pdf(mes, ano):
    """Gera relatório de receita por cliente"""
    inicio = datetime(ano, mes, 1)
    if mes == 12:
        fim = datetime(ano + 1, 1, 1)
    else:
        fim = datetime(ano, mes + 1, 1)

    chamados = Chamado.query.filter(Chamado.data_criacao >= inicio, Chamado.data_criacao < fim).all()

    arquivo_pdf = f'Relatorio_Receita_{mes:02d}_{ano}.pdf'
    doc = SimpleDocTemplate(arquivo_pdf, pagesize=A4)
    story = []

    styles = getSampleStyleSheet()
    titulo_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=24, textColor=colors.HexColor('#27ae60'), spaceAfter=30, alignment=TA_CENTER, fontName='Helvetica-Bold')
    subtitulo_style = ParagraphStyle('CustomSubtitle', parent=styles['Heading2'], fontSize=14, textColor=colors.HexColor('#229954'), spaceAfter=12, fontName='Helvetica-Bold')

    meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    mes_nome = meses[mes - 1]

    story.append(Paragraph(f'Relatório de Receita - {mes_nome} de {ano}', titulo_style))
    story.append(Spacer(1, 0.3*inch))

    # Calcular receita por cliente
    receita_clientes = {}
    receita_total = 0

    for chamado in chamados:
        if chamado.cliente not in receita_clientes:
            receita_clientes[chamado.cliente] = 0
        receita_clientes[chamado.cliente] += chamado.valor_recebido
        receita_total += chamado.valor_recebido

    # Resumo geral
    story.append(Paragraph('Resumo Geral', subtitulo_style))
    resumo_data = [
        ['Receita Total', f'R$ {receita_total:.2f}'],
        ['Clientes', f'{len(receita_clientes)}'],
        ['Chamados', f'{len(chamados)}']
    ]
    resumo_table = Table(resumo_data, colWidths=[4*inch, 2*inch])
    resumo_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 1), colors.HexColor('#e8f5e9')),
        ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#27ae60')),
        ('TEXTCOLOR', (0, 2), (-1, 2), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(resumo_table)
    story.append(Spacer(1, 0.3*inch))

    # Receita por cliente
    if receita_clientes:
        story.append(PageBreak())
        story.append(Paragraph('Receita por Cliente', subtitulo_style))
        story.append(Spacer(1, 0.2*inch))

        receita_ordenada = sorted(receita_clientes.items(), key=lambda x: x[1], reverse=True)
        receita_data = [['Cliente', 'Receita', 'Percentual']]

        for cliente, valor in receita_ordenada:
            percentual = f"{(valor / receita_total * 100):.1f}%" if receita_total > 0 else "0%"
            receita_data.append([cliente, f'R$ {valor:.2f}', percentual])

        receita_table = Table(receita_data, colWidths=[3*inch, 1.5*inch, 1.5*inch])
        receita_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27ae60')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#d5f4e6')),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(receita_table)
        story.append(Spacer(1, 0.3*inch))

        # Análise
        story.append(Paragraph('Análise de Receita', subtitulo_style))
        analise_data = [
            ['Ticket Médio', f'R$ {receita_total / len(chamados) if len(chamados) > 0 else 0:.2f}'],
            ['Receita Média por Cliente', f'R$ {receita_total / len(receita_clientes) if len(receita_clientes) > 0 else 0:.2f}'],
            ['Cliente com Maior Receita', f'{receita_ordenada[0][0] if receita_ordenada else "N/A"}']
        ]
        analise_table = Table(analise_data, colWidths=[3*inch, 3*inch])
        analise_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f39c12')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 1), (-1, 1), colors.white),
            ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#e74c3c')),
            ('TEXTCOLOR', (0, 2), (-1, 2), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(analise_table)

    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph(f'Relatório gerado em {datetime.now().strftime("%d/%m/%Y às %H:%M")}', styles['Normal']))

    doc.build(story)
    return arquivo_pdf
