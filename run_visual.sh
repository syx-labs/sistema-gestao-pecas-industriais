#!/bin/bash
# Script para executar a interface visual do Sistema de Gestão de Peças

echo "🏭 Iniciando Sistema de Gestão de Peças - Interface Visual"
echo "=================================================="
echo ""

# Verifica se o ambiente virtual existe
if [ ! -d "venv" ]; then
    echo "⚠️  Ambiente virtual não encontrado. Criando..."
    python3 -m venv venv
    echo "✅ Ambiente virtual criado!"
    echo ""
fi

# Ativa o ambiente virtual e verifica dependências
source venv/bin/activate

if ! python -c "import streamlit" 2>/dev/null; then
    echo "📦 Instalando dependências..."
    pip install -q streamlit plotly pandas
    echo "✅ Dependências instaladas!"
    echo ""
fi

echo "📊 Dashboard abrirá em: http://localhost:8501"
echo ""
echo "Pressione CTRL+C para encerrar"
echo ""

streamlit run streamlit_app.py
