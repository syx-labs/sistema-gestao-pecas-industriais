"""
Estilos e configuração Rich para a interface TUI.

Este módulo centraliza todos os estilos visuais do CLI usando a biblioteca Rich,
proporcionando uma interface moderna e profissional.
"""

from rich.console import Console
from rich.theme import Theme
from rich import box
from rich.style import Style

# ========================================
# TEMA DE CORES
# ========================================

# Tema customizado para o sistema
SISTEMA_THEME = Theme({
    # Estados
    "success": "bold green",
    "error": "bold red",
    "warning": "bold yellow",
    "info": "bold cyan",

    # Componentes
    "header": "bold white on blue",
    "title": "bold cyan",
    "subtitle": "bold white",
    "label": "cyan",
    "value": "yellow",

    # Peças
    "peca_aprovada": "green",
    "peca_reprovada": "red",
    "peca_id": "cyan",
    "peca_peso": "yellow",
    "peca_cor": "magenta",
    "peca_comprimento": "blue",

    # Caixas
    "caixa_fechada": "green",
    "caixa_aberta": "yellow",
    "caixa_id": "bold cyan",

    # Menu
    "menu_opcao": "cyan",
    "menu_descricao": "white",
    "menu_border": "blue",

    # Relatório
    "relatorio_titulo": "bold white on blue",
    "relatorio_valor": "bold yellow",
    "relatorio_percentual": "bold green",
})

# Console global com tema customizado
console = Console(theme=SISTEMA_THEME)


# ========================================
# ESTILOS DE BORDAS
# ========================================

# Box style para menu principal
MENU_BOX = box.ROUNDED

# Box style para painéis informativos
INFO_BOX = box.ROUNDED

# Box style para tabelas
TABLE_BOX = box.SIMPLE_HEAD

# Box style para relatórios
REPORT_BOX = box.DOUBLE


# ========================================
# ESTILOS REUTILIZÁVEIS
# ========================================

# Estilo para títulos de seção
STYLE_SECTION_TITLE = Style(color="cyan", bold=True)

# Estilo para valores numéricos
STYLE_NUMBER = Style(color="yellow", bold=True)

# Estilo para status de sucesso
STYLE_SUCCESS = Style(color="green", bold=True)

# Estilo para status de erro
STYLE_ERROR = Style(color="red", bold=True)

# Estilo para avisos
STYLE_WARNING = Style(color="yellow", bold=True)

# Estilo para informações
STYLE_INFO = Style(color="cyan", bold=True)


# ========================================
# ÍCONES E SÍMBOLOS
# ========================================

ICON_SUCCESS = "✅"
ICON_ERROR = "❌"
ICON_WARNING = "⚠️"
ICON_INFO = "ℹ️"
ICON_PECA = "🔧"
ICON_CAIXA = "📦"
ICON_CAIXA_FECHADA = "🔒"
ICON_CAIXA_ABERTA = "🔓"
ICON_RELATORIO = "📊"
ICON_CADASTRAR = "📝"
ICON_LISTAR = "📋"
ICON_REMOVER = "🗑️"
ICON_SAIR = "🚪"
ICON_FABRICA = "🏭"
ICON_QUALIDADE = "✨"


# ========================================
# HELPERS DE FORMATAÇÃO
# ========================================

def formatar_sucesso(mensagem: str) -> str:
    """Formata mensagem de sucesso com ícone e cor."""
    return f"[success]{ICON_SUCCESS} {mensagem}[/success]"


def formatar_erro(mensagem: str) -> str:
    """Formata mensagem de erro com ícone e cor."""
    return f"[error]{ICON_ERROR} {mensagem}[/error]"


def formatar_aviso(mensagem: str) -> str:
    """Formata mensagem de aviso com ícone e cor."""
    return f"[warning]{ICON_WARNING} {mensagem}[/warning]"


def formatar_info(mensagem: str) -> str:
    """Formata mensagem informativa com ícone e cor."""
    return f"[info]{ICON_INFO} {mensagem}[/info]"


def formatar_peca_id(peca_id: str) -> str:
    """Formata ID de peça com estilo."""
    return f"[peca_id]{peca_id}[/peca_id]"


def formatar_valor_numerico(valor: float, unidade: str = "") -> str:
    """Formata valor numérico com unidade."""
    if unidade:
        return f"[value]{valor}{unidade}[/value]"
    return f"[value]{valor}[/value]"


def formatar_percentual(valor: float) -> str:
    """Formata percentual com cor."""
    return f"[relatorio_percentual]{valor:.1f}%[/relatorio_percentual]"


def formatar_status_peca(aprovada: bool) -> str:
    """Formata status da peça (aprovada/reprovada)."""
    if aprovada:
        return f"[peca_aprovada]{ICON_SUCCESS} APROVADA[/peca_aprovada]"
    else:
        return f"[peca_reprovada]{ICON_ERROR} REPROVADA[/peca_reprovada]"


def formatar_status_caixa(fechada: bool) -> str:
    """Formata status da caixa (fechada/aberta)."""
    if fechada:
        return f"[caixa_fechada]{ICON_CAIXA_FECHADA} Fechada[/caixa_fechada]"
    else:
        return f"[caixa_aberta]{ICON_CAIXA_ABERTA} Em preenchimento[/caixa_aberta]"
