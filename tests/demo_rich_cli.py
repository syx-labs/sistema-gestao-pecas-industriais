#!/usr/bin/env python3
"""
Demo das melhorias visuais do CLI com Rich.
Este script demonstra as principais features do novo TUI.
"""

from utils.rich_styles import (
    console,
    formatar_sucesso,
    formatar_erro,
    formatar_aviso,
    formatar_info,
    formatar_peca_id,
    formatar_valor_numerico,
    formatar_percentual,
    formatar_status_peca,
    formatar_status_caixa,
    ICON_FABRICA,
    ICON_QUALIDADE,
)
from rich.panel import Panel
from rich.table import Table
from rich import box
from utils.menu import exibir_menu_principal
from services.armazenamento import inicializar_sistema
from models.peca import criar_peca


def demo_banner():
    """Demonstra o banner de boas-vindas."""
    console.print("\n[bold cyan]═══ DEMO: Banner de Boas-vindas ═══[/bold cyan]\n")

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


def demo_menu():
    """Demonstra o menu principal."""
    console.print("\n[bold cyan]═══ DEMO: Menu Principal ═══[/bold cyan]\n")
    exibir_menu_principal()


def demo_mensagens():
    """Demonstra os diferentes tipos de mensagens."""
    console.print("\n[bold cyan]═══ DEMO: Mensagens de Status ═══[/bold cyan]\n")

    console.print(formatar_sucesso("Operação concluída com sucesso!"))
    console.print(formatar_erro("Erro ao processar a solicitação"))
    console.print(formatar_aviso("Atenção: Limite quase atingido"))
    console.print(formatar_info("Informação: Sistema inicializado"))


def demo_tabela_pecas():
    """Demonstra tabela de peças aprovadas."""
    console.print("\n[bold cyan]═══ DEMO: Tabela de Peças Aprovadas ═══[/bold cyan]\n")

    table = Table(
        title="✅ [bold green]PEÇAS APROVADAS[/bold green] (3)",
        box=box.SIMPLE_HEAD,
        show_header=True,
        header_style="bold magenta",
        border_style="green",
    )

    table.add_column("ID", style="cyan", width=12)
    table.add_column("Peso (g)", style="yellow", justify="right", width=10)
    table.add_column("Cor", style="magenta", width=12)
    table.add_column("Comprimento (cm)", style="blue", justify="right", width=18)

    table.add_row("P001", "100.0", "azul", "15.0")
    table.add_row("P002", "98.5", "verde", "18.2")
    table.add_row("P003", "102.3", "azul", "12.5")

    console.print(table)


def demo_tabela_reprovadas():
    """Demonstra tabela de peças reprovadas."""
    console.print("\n[bold cyan]═══ DEMO: Tabela de Peças Reprovadas ═══[/bold cyan]\n")

    table = Table(
        title="❌ [bold red]PEÇAS REPROVADAS[/bold red] (2)",
        box=box.SIMPLE_HEAD,
        show_header=True,
        header_style="bold magenta",
        border_style="red",
        show_lines=True,
    )

    table.add_column("ID", style="cyan", width=12)
    table.add_column("Peso (g)", style="yellow", justify="right", width=10)
    table.add_column("Cor", style="magenta", width=12)
    table.add_column("Comprimento (cm)", style="blue", justify="right", width=18)
    table.add_column("Motivos de Reprovação", style="red", width=40)

    motivos1 = "• Peso fora do intervalo (95.0-105.0g): 120.0g\n• Cor inadequada (esperado: azul ou verde): vermelho"
    motivos2 = "• Comprimento fora do intervalo (10.0-20.0cm): 25.0cm"

    table.add_row("P004", "120.0", "vermelho", "15.0", motivos1)
    table.add_row("P005", "100.0", "azul", "25.0", motivos2)

    console.print(table)


def demo_caixas():
    """Demonstra painéis de caixas."""
    console.print("\n[bold cyan]═══ DEMO: Painéis de Caixas ═══[/bold cyan]\n")

    # Caixa fechada
    conteudo_fechada = f"""[bold cyan]Status:[/bold cyan] {formatar_status_caixa(True)}
[bold cyan]Capacidade:[/bold cyan] 10/10 peças
[bold cyan]IDs das peças:[/bold cyan] P001, P002, P003, P004, P005, P006, P007, P008, P009, P010
"""

    panel_fechada = Panel(
        conteudo_fechada,
        title="[bold white]Caixa #1[/bold white]",
        border_style="green",
        box=box.ROUNDED,
    )

    console.print(panel_fechada)
    console.print()

    # Caixa em preenchimento
    total_pecas = 7
    percentual = (total_pecas / 10) * 100
    filled = int((total_pecas / 10) * 20)
    bar = "█" * filled + "░" * (20 - filled)

    conteudo_aberta = f"""[bold cyan]Status:[/bold cyan] {formatar_status_caixa(False)}
[bold cyan]Capacidade:[/bold cyan] {total_pecas}/10 peças ({percentual:.0f}%)
[bold cyan]Progresso:[/bold cyan] [{bar}]
[bold cyan]IDs das peças:[/bold cyan] P011, P012, P013, P014, P015, P016, P017
"""

    panel_aberta = Panel(
        conteudo_aberta,
        title="[bold white]Caixa #2[/bold white]",
        border_style="yellow",
        box=box.ROUNDED,
    )

    console.print(panel_aberta)


def demo_relatorio():
    """Demonstra painéis do relatório."""
    console.print("\n[bold cyan]═══ DEMO: Relatório Final ═══[/bold cyan]\n")

    # Título principal
    titulo_panel = Panel(
        "[bold white]RELATÓRIO FINAL DO SISTEMA[/bold white]",
        style="bold white on blue",
        box=box.DOUBLE,
    )
    console.print(titulo_panel)
    console.print()

    # Painel 1: Resumo Geral
    resumo_content = f"""[bold cyan]Total de peças processadas:[/bold cyan] {formatar_valor_numerico(25, '')}

[bold green]✅ Peças aprovadas:[/bold green] {formatar_valor_numerico(18, '')} ({formatar_percentual(72.0)})
[bold red]❌ Peças reprovadas:[/bold red] {formatar_valor_numerico(7, '')} ({formatar_percentual(28.0)})
"""

    painel_resumo = Panel(
        resumo_content,
        title="[bold white]📊 RESUMO GERAL[/bold white]",
        border_style="blue",
        box=box.DOUBLE,
    )

    console.print(painel_resumo)
    console.print()

    # Painel 2: Armazenamento
    barra = "█" * 14 + "░" * 6
    armazenamento_content = f"""[bold cyan]Caixas fechadas:[/bold cyan] {formatar_valor_numerico(1, '')}
[bold cyan]Caixa em preenchimento:[/bold cyan] 1 caixa (8/10 peças)
[{barra}] 80%
"""

    painel_armazenamento = Panel(
        armazenamento_content,
        title="[bold white]📦 ARMAZENAMENTO[/bold white]",
        border_style="green",
        box=box.DOUBLE,
    )

    console.print(painel_armazenamento)
    console.print()

    # Painel 3: Reprovações
    reprovacoes_content = f"""[bold red]Por peso inadequado:[/bold red] {formatar_valor_numerico(3, '')} peças
[bold red]Por cor inadequada:[/bold red] {formatar_valor_numerico(5, '')} peças
[bold red]Por comprimento inadequado:[/bold red] {formatar_valor_numerico(2, '')} peças
"""

    painel_reprovacoes = Panel(
        reprovacoes_content,
        title="[bold white]❌ DETALHAMENTO DE REPROVAÇÕES[/bold white]",
        border_style="red",
        box=box.DOUBLE,
    )

    console.print(painel_reprovacoes)


def main():
    """Executa todas as demos."""
    console.print("[bold green]" + "=" * 60 + "[/bold green]")
    console.print("[bold green]DEMONSTRAÇÃO: CLI com Rich (Lipgloss Quality)[/bold green]".center(60))
    console.print("[bold green]" + "=" * 60 + "[/bold green]")

    demo_banner()
    demo_menu()
    demo_mensagens()
    demo_tabela_pecas()
    demo_tabela_reprovadas()
    demo_caixas()
    demo_relatorio()

    console.print("\n[bold green]" + "=" * 60 + "[/bold green]")
    console.print("[bold green]FIM DA DEMONSTRAÇÃO[/bold green]".center(60))
    console.print("[bold green]" + "=" * 60 + "[/bold green]\n")


if __name__ == "__main__":
    main()
