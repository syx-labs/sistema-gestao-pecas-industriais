# 🚀 Guia Rápido de Início

## ⚡ Início Rápido - Interface Visual

### Opção 1: Script Automático (Recomendado)

```bash
./run_visual.sh
```

O script irá:
- Criar o ambiente virtual automaticamente (se não existir)
- Instalar todas as dependências necessárias
- Iniciar o Streamlit

### Opção 2: Manual

```bash
# 1. Criar ambiente virtual
python3 -m venv venv

# 2. Ativar ambiente virtual
source venv/bin/activate

# 3. Instalar dependências
pip install streamlit plotly pandas 'altair<6' cachetools gitpython numpy pillow pydeck requests tenacity toml tornado python-dateutil pytz tzdata

# 4. Executar aplicação
streamlit run streamlit_app.py
```

## 🖥️ Interface CLI (Terminal)

```bash
python3 main.py
```

Não requer instalação de dependências!

## 📊 Acessando a Interface Visual

Após executar o comando, a aplicação abrirá automaticamente em:
```
http://localhost:8501
```

Se não abrir automaticamente, acesse manualmente no navegador.

## 🎯 Primeiros Passos

### 1. Cadastre Peças

Vá em "📝 Cadastrar Peça" e adicione algumas peças:

**Exemplo de Peça Aprovada:**
- ID: P001
- Peso: 100g
- Cor: azul
- Comprimento: 15cm

**Exemplo de Peça Reprovada:**
- ID: P002
- Peso: 120g (fora da faixa!)
- Cor: vermelho (cor não aceita!)
- Comprimento: 25cm (fora da faixa!)

### 2. Visualize o Dashboard

Vá em "📊 Dashboard" para ver:
- Métricas em tempo real
- Gráficos de aprovação
- Distribuição de peso

### 3. Gerencie Caixas

Vá em "📦 Caixas" para acompanhar:
- Progresso da caixa atual
- Lista de caixas fechadas

### 4. Veja Relatórios

Vá em "📈 Relatório" para análises completas

## 🔧 Solução de Problemas

### Erro: "Module not found"

```bash
# Reinstale as dependências
source venv/bin/activate
pip install --force-reinstall streamlit plotly pandas
```

### Erro: "Port already in use"

```bash
# Use outra porta
streamlit run streamlit_app.py --server.port 8502
```

### Erro: "Command not found: streamlit"

```bash
# Certifique-se de ativar o ambiente virtual
source venv/bin/activate
```

## 📝 Dicas

- Use **R** para recarregar a aplicação
- Use o botão "🔄 Resetar Sistema" para limpar todos os dados
- Cadastre 10 peças aprovadas para ver uma caixa ser fechada automaticamente
- Experimente cadastrar peças nos limites das tolerâncias

## 🎨 Personalização

Edite `.streamlit/config.toml` para personalizar:
- Cores do tema
- Porta do servidor
- Configurações de layout

## 📖 Documentação Completa

- [README.md](README.md) - Documentação completa do projeto
- [STREAMLIT_GUIDE.md](STREAMLIT_GUIDE.md) - Guia detalhado da interface visual

---

**Dúvidas?** Consulte a documentação completa ou abra uma issue no repositório.
