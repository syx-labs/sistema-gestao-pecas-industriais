#!/usr/bin/env python3
"""
Sistema de Automação Digital para Gestão de Peças Industriais

Desenvolvido para automatizar o controle de produção e qualidade de peças
fabricadas em linha de montagem.

Autor: Gabriel Falcão
Data: 2025-11-15
"""

import os
import sys

from services.armazenamento import inicializar_sistema
from utils.menu import (
    exibir_menu_principal,
    cadastrar_peca_interface,
    listar_pecas_interface,
    remover_peca_interface,
    listar_caixas_interface,
    gerar_relatorio_interface,
    limpar_terminal
)
from rich.panel import Panel
from rich.console import Console
from rich import box
from utils.rich_styles import ICON_FABRICA, ICON_QUALIDADE

console = Console()

# Tenta importar Textual para interface interativa
TEXTUAL_DISPONIVEL = False
try:
    from tui_app import run_tui_app
    TEXTUAL_DISPONIVEL = True
except ImportError:
    TEXTUAL_DISPONIVEL = False


def usar_modo_classico() -> bool:
    """
    Verifica se deve usar o modo clássico (menu numérico).

    Returns:
        True se deve usar modo clássico, False se deve usar TUI interativo
    """
    # Verifica variável de ambiente para forçar modo clássico
    if os.getenv('PECAS_CLI_CLASSICO', '').lower() in ('1', 'true', 'yes'):
        return True

    # Verifica argumento de linha de comando
    if '--classic' in sys.argv or '--classico' in sys.argv:
        return True

    # Se Textual não estiver disponível, usa clássico
    if not TEXTUAL_DISPONIVEL:
        return True

    # Por padrão, usa TUI interativo se disponível
    return False


def main() -> None:
    """
    Função principal do sistema.
    Inicializa o sistema e executa o loop do menu interativo.
    """
    # Verifica qual modo usar
    if usar_modo_classico():
        # Modo clássico (menu numérico)
        if not TEXTUAL_DISPONIVEL:
            console.print("[yellow]⚠️  TUI interativo não disponível. Usando modo clássico.[/yellow]")
            console.print("[cyan]💡 Para habilitar navegação por setas, instale: pip install textual[/cyan]\n")

        main_classico()
    else:
        # Modo TUI interativo (navegação por setas)
        console.print("[green]✨ Iniciando interface TUI interativa...[/green]")
        console.print("[cyan]💡 Use --classic para voltar ao modo numérico[/cyan]\n")
        run_tui_app()


def main_classico() -> None:
    """
    Executa o sistema no modo clássico (menu numérico).
    """
    # Inicializa o sistema
    sistema = inicializar_sistema()

    # Banner de boas-vindas com Rich
    limpar_terminal()

    banner_content = f"""[bold white]BEM-VINDO AO SISTEMA DE GESTÃO DE PEÇAS[/bold white]

{ICON_FABRICA} [cyan]Sistema de Automação Digital para Controle de Qualidade[/cyan]
{ICON_QUALIDADE} [green]Desenvolvido por Gabriel Falcão[/green]
"""

    banner_panel = Panel(
        banner_content,
        title=f"[bold white]{ICON_FABRICA} SISTEMA INDUSTRIAL {ICON_FABRICA}[/bold white]",
        border_style="bold blue",
        box=box.DOUBLE,
        padding=(1, 2),
    )

    console.print(banner_panel)
    console.print()
    input("Pressione ENTER para continuar...")

    # Loop principal do menu
    while True:
        exibir_menu_principal()

        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == '1':
            cadastrar_peca_interface(sistema)

        elif opcao == '2':
            listar_pecas_interface(sistema)

        elif opcao == '3':
            remover_peca_interface(sistema)

        elif opcao == '4':
            listar_caixas_interface(sistema)

        elif opcao == '5':
            gerar_relatorio_interface(sistema)

        elif opcao == '0':
            # Mensagem de despedida com Rich
            console.print()
            despedida_content = """[bold white]Encerrando sistema...[/bold white]

[green]✅ Obrigado por utilizar o sistema![/green]
[cyan]Todos os dados foram salvos com sucesso.[/cyan]
"""
            despedida_panel = Panel(
                despedida_content,
                border_style="bold green",
                box=box.ROUNDED,
                padding=(1, 2),
            )
            console.print(despedida_panel)
            break

        else:
            console.print("\n[bold red]❌ Opção inválida! Por favor, escolha uma opção de 0 a 5.[/bold red]")

        # Pausa antes de voltar ao menu
        input("\nPressione ENTER para continuar...")


if __name__ == "__main__":
    main()
