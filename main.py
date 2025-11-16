#!/usr/bin/env python3
"""
Sistema de Automação Digital para Gestão de Peças Industriais

Desenvolvido para automatizar o controle de produção e qualidade de peças
fabricadas em linha de montagem.

Autor: Gabriel Falcão
Data: 2025-11-15
"""

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


def main() -> None:
    """
    Função principal do sistema.
    Inicializa o sistema e executa o loop do menu interativo.
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
