#!/bin/bash

# Script para alternar entre Dark Mode e Light Mode
# Uso: ./toggle_theme.sh [dark|light]

CONFIG_FILE=".streamlit/config.toml"
DARK_BG="#0E1117"
LIGHT_BG="#FFFFFF"

# Cores ANSI para output colorido
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_header() {
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "  🎨 Sistema de Alternância de Temas"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
}

detect_current_theme() {
    if grep -q "backgroundColor = \"$DARK_BG\"" "$CONFIG_FILE"; then
        echo "dark"
    else
        echo "light"
    fi
}

switch_to_dark() {
    echo -e "${BLUE}🌙 Ativando Dark Mode...${NC}"
    
    # Atualiza cores para dark mode
    sed -i.bak "s/backgroundColor = \".*\"/backgroundColor = \"$DARK_BG\"/" "$CONFIG_FILE"
    sed -i.bak "s/secondaryBackgroundColor = \".*\"/secondaryBackgroundColor = \"#1E2128\"/" "$CONFIG_FILE"
    sed -i.bak "s/textColor = \".*\"/textColor = \"#FAFAFA\"/" "$CONFIG_FILE"
    
    echo -e "${GREEN}✅ Dark Mode ativado com sucesso!${NC}"
    echo ""
    echo "🌙 Características:"
    echo "  • Fundo escuro (#0E1117)"
    echo "  • Texto claro (#FAFAFA)"
    echo "  • Ideal para ambientes com pouca luz"
}

switch_to_light() {
    echo -e "${YELLOW}☀️  Ativando Light Mode...${NC}"
    
    # Atualiza cores para light mode
    sed -i.bak "s/backgroundColor = \".*\"/backgroundColor = \"$LIGHT_BG\"/" "$CONFIG_FILE"
    sed -i.bak "s/secondaryBackgroundColor = \".*\"/secondaryBackgroundColor = \"#F0F2F6\"/" "$CONFIG_FILE"
    sed -i.bak "s/textColor = \".*\"/textColor = \"#262730\"/" "$CONFIG_FILE"
    
    echo -e "${GREEN}✅ Light Mode ativado com sucesso!${NC}"
    echo ""
    echo "☀️  Características:"
    echo "  • Fundo claro (#FFFFFF)"
    echo "  • Texto escuro (#262730)"
    echo "  • Ideal para ambientes bem iluminados"
}

show_current() {
    CURRENT=$(detect_current_theme)
    if [ "$CURRENT" = "dark" ]; then
        echo -e "Tema atual: ${BLUE}🌙 Dark Mode${NC}"
    else
        echo -e "Tema atual: ${YELLOW}☀️  Light Mode${NC}"
    fi
}

show_help() {
    echo "Uso: $0 [dark|light|toggle|status]"
    echo ""
    echo "Opções:"
    echo "  dark    - Ativa o tema escuro (Dark Mode)"
    echo "  light   - Ativa o tema claro (Light Mode)"
    echo "  toggle  - Alterna entre os temas automaticamente"
    echo "  status  - Mostra o tema atual"
    echo ""
    echo "Exemplos:"
    echo "  $0 dark     # Ativa dark mode"
    echo "  $0 light    # Ativa light mode"
    echo "  $0 toggle   # Alterna entre temas"
    echo "  $0          # Mesmo que toggle"
}

main() {
    print_header
    
    # Verifica se o arquivo de configuração existe
    if [ ! -f "$CONFIG_FILE" ]; then
        echo "❌ Erro: Arquivo $CONFIG_FILE não encontrado!"
        echo "Execute este script da raiz do projeto."
        exit 1
    fi
    
    COMMAND=${1:-toggle}
    
    case $COMMAND in
        dark)
            switch_to_dark
            ;;
        light)
            switch_to_light
            ;;
        toggle)
            CURRENT=$(detect_current_theme)
            show_current
            echo ""
            if [ "$CURRENT" = "dark" ]; then
                switch_to_light
            else
                switch_to_dark
            fi
            ;;
        status)
            show_current
            exit 0
            ;;
        help|--help|-h)
            show_help
            exit 0
            ;;
        *)
            echo "❌ Comando inválido: $COMMAND"
            echo ""
            show_help
            exit 1
            ;;
    esac
    
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo -e "${GREEN}🔄 Reinicie o aplicativo Streamlit para aplicar as mudanças${NC}"
    echo ""
    echo "Comandos úteis:"
    echo "  • Parar servidor: Ctrl+C"
    echo "  • Iniciar: streamlit run streamlit_app.py"
    echo "  • Ou use: ./run_visual.sh"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    
    # Limpa arquivos de backup
    rm -f "$CONFIG_FILE.bak"
}

main "$@"

