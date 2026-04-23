# Sistema de Atendimento - IT Service Desk

Um sistema web completo para gerenciar chamados de atendimento (tickets) com relatórios automáticos em PDF.

## 🎯 Funcionalidades

✅ **Dashboard** - Interface intuitiva para abrir novos chamados
✅ **Formulário Web** - Registro de cliente, categoria, data/hora e descrição
✅ **Banco de Dados** - Armazena todos os chamados (SQLite)
✅ **Listagem Completa** - Busca e filtro de chamados
✅ **Relatórios Mensais** - Estatísticas e gráficos automáticos
✅ **Exportação PDF** - Relatórios com gráficos para clientes
✅ **Acompanhamento** - Atualizar status do chamado (aberto/em progresso/fechado)

## 📋 Requisitos

- Python 3.7+
- pip (gerenciador de pacotes Python)

## 🚀 Instalação e Uso

### 1. Instalar Dependências

Abra o terminal/PowerShell na pasta do projeto e execute:

```bash
pip install -r requirements.txt
```

### 2. Iniciar o Servidor

No mesmo terminal, execute:

```bash
python app.py
```

Você verá uma mensagem como:
```
Running on http://127.0.0.1:5000
```

### 3. Acessar o Sistema

Abra seu navegador e vá para:
```
http://localhost:5000
```

## 📱 Páginas Disponíveis

### Dashboard (/)
- Resumo com total de chamados
- Formulário para abrir novo chamado
- Lista dos últimos 10 chamados

### Listagem (/listagem)
- Filtrar chamados por status
- Buscar por cliente
- Ver detalhes e atualizar status

### Relatórios (/relatorio)
- Selecionar mês e ano
- Ver estatísticas por cliente
- Ver distribuição por categoria
- Baixar relatório em PDF

## 📊 Campos do Chamado

Ao abrir um chamado, você precisa informar:

- **Cliente/Empresa** - Nome da empresa que solicita o atendimento
- **Categoria** - Tipo de atendimento (Suporte Técnico, Consultoria, etc)
- **Data e Hora** - Quando o atendimento foi realizado
- **Descrição** - Detalhes completos do problema/demanda

## 🎨 Categorias Disponíveis

- Suporte Técnico
- Consultoria
- Instalação
- Manutenção
- Treinamento
- Desenvolvimento
- Outro

## 📊 Status dos Chamados

- **Aberto** - Chamado recém criado
- **Em Progresso** - Sendo atendido
- **Fechado** - Problema resolvido

## 📥 Gerando Relatórios em PDF

1. Vá para "Relatórios"
2. Selecione o mês e ano desejados
3. Clique em "Baixar PDF"
4. O relatório incluirá:
   - Resumo com total de chamados
   - Gráfico dos clientes mais atendidos
   - Gráfico de distribuição por categoria
   - Gráfico de status dos chamados
   - Lista completa de chamados do período

## 💾 Banco de Dados

Os dados são armazenados em um arquivo chamado `chamados.db` na mesma pasta do projeto. Este arquivo é criado automaticamente na primeira execução.

Para resetar os dados, simplesmente delete o arquivo `chamados.db` e reinicie o servidor.

## 🔧 Troubleshooting

### Erro: "Module not found"
```bash
pip install -r requirements.txt
```

### Porta 5000 já está em uso
Edite a última linha do `app.py`:
```python
app.run(debug=True, host='127.0.0.1', port=5001)  # Mude 5000 para outra porta
```

### Erro ao gerar PDF
Certifique-se de que tem permissão de escrita na pasta do projeto.

## 📈 Aumentando seus Contratos

Use este sistema para:

1. **Demonstrar Quantidade de Atendimentos** - Gere PDFs mensais mostrando quantos clientes você atendeu
2. **Mostrar Especializações** - Os relatórios mostram o tipo de serviço mais demandado
3. **Apresentar Dados ao Cliente** - Leve o relatório PDF para reuniões
4. **Comprovar ROI** - Mostre quantas horas de trabalho você ofereceu

## 📧 Suporte

Se encontrar problemas, verifique:
- Python está instalado: `python --version`
- Dependências instaladas: `pip list`
- Porta não está bloqueada pelo firewall

## 📝 Licença

Sistema criado para uso pessoal e comercial.

---

**Desenvolvido com ❤️ para otimizar seu atendimento IT**
