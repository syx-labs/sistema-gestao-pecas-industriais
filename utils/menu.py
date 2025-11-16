"""
Funções de interface do menu interativo.
"""

import os
from typing import Optional
from models.peca import criar_peca
from services.validacao import validar_peca
from services.armazenamento import SistemaArmazenamento, adicionar_peca_em_caixa, remover_peca_por_id
from services.relatorio import gerar_relatorio_completo
from models.caixa import CAPACIDADE_MAXIMA_CAIXA
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, BarColumn, TextColumn
from rich.layout import Layout
from rich.columns import Columns
from rich import box
from utils.rich_styles import (
    console,
    MENU_BOX,
    INFO_BOX,
    TABLE_BOX,
    REPORT_BOX,
    ICON_FABRICA,
    ICON_CADASTRAR,
    ICON_LISTAR,
    ICON_REMOVER,
    ICON_CAIXA,
    ICON_RELATORIO,
    ICON_SAIR,
    formatar_sucesso,
    formatar_erro,
    formatar_aviso,
    formatar_info,
    formatar_peca_id,
    formatar_valor_numerico,
    formatar_percentual,
    formatar_status_peca,
    formatar_status_caixa,
)


def limpar_terminal() -> None:
    """Limpa o terminal de acordo com o sistema operacional."""
    os.system('clear' if os.name == 'posix' else 'cls')


def exibir_menu_principal() -> None:
    """Exibe o menu principal do sistema com interface Rich."""
    console.print()  # Linha em branco

    # Cria tabela para as opções do menu
    menu_table = Table(
        show_header=False,
        box=None,
        padding=(0, 2),
        collapse_padding=True,
    )
    menu_table.add_column("Opção", style="bold cyan", width=3, justify="center")
    menu_table.add_column("Separador", width=1)
    menu_table.add_column("Descrição", style="white")

    # Adiciona opções
    menu_table.add_row("1", "│", f"{ICON_CADASTRAR} Cadastrar nova peça")
    menu_table.add_row("2", "│", f"{ICON_LISTAR} Listar peças aprovadas/reprovadas")
    menu_table.add_row("3", "│", f"{ICON_REMOVER} Remover peça cadastrada")
    menu_table.add_row("4", "│", f"{ICON_CAIXA} Listar caixas fechadas")
    menu_table.add_row("5", "│", f"{ICON_RELATORIO} Gerar relatório final")
    menu_table.add_row("", "", "")  # Linha em branco
    menu_table.add_row("0", "│", f"{ICON_SAIR} Sair")

    # Cria painel com o menu
    menu_panel = Panel(
        menu_table,
        title=f"[bold white]{ICON_FABRICA} SISTEMA DE GESTÃO DE PEÇAS[/bold white]",
        border_style="blue",
        box=MENU_BOX,
        padding=(1, 2),
    )

    console.print(menu_panel)


def solicitar_numero(mensagem: str, tipo_numero: str = "float") -> Optional[float]:
    """
    Solicita um número ao usuário com validação.

    Args:
        mensagem: Mensagem a exibir
        tipo_numero: "float" ou "int"

    Returns:
        Número digitado ou None se inválido
    """
    try:
        valor = input(mensagem)
        if tipo_numero == "int":
            return int(valor)
        return float(valor)
    except ValueError:
        console.print(formatar_erro("Digite um número válido"))
        return None


def cadastrar_peca_interface(sistema: SistemaArmazenamento) -> None:
    """
    Interface para cadastrar uma nova peça com Rich.

    Args:
        sistema: Estado atual do sistema
    """
    console.print()
    console.print(Panel(
        "[bold white]CADASTRAR NOVA PEÇA[/bold white]",
        border_style="cyan",
        box=INFO_BOX,
    ))
    console.print()

    # Coleta dados da peça
    id_peca = input("ID da peça: ").strip()
    if not id_peca:
        console.print(formatar_erro("ID não pode ser vazio"))
        return

    # Verifica se ID já existe
    todas_pecas = sistema['pecas_aprovadas'] + sistema['pecas_reprovadas']
    if any(p['id'] == id_peca for p in todas_pecas):
        console.print(formatar_erro(f"Já existe uma peça com ID '{id_peca}'"))
        return

    peso = solicitar_numero("Peso (g): ")
    if peso is None:
        return

    cor = input("Cor: ").strip()
    if not cor:
        console.print(formatar_erro("Cor não pode ser vazia"))
        return

    comprimento = solicitar_numero("Comprimento (cm): ")
    if comprimento is None:
        return

    # Cria peça
    peca = criar_peca(
        id_peca=id_peca,
        peso=peso,
        cor=cor,
        comprimento=comprimento
    )

    # Valida peça
    aprovada, motivos = validar_peca(peca)
    peca['aprovada'] = aprovada
    peca['motivos_reprovacao'] = motivos

    console.print()
    if aprovada:
        console.print(formatar_sucesso(f"Peça {formatar_peca_id(id_peca)} APROVADA!"))
        _, mensagem = adicionar_peca_em_caixa(peca, sistema)
        console.print(formatar_info(mensagem))
    else:
        console.print(formatar_erro(f"Peça {formatar_peca_id(id_peca)} REPROVADA!"))
        console.print("\n[bold red]Motivos:[/bold red]")
        for motivo in motivos:
            console.print(f"  [red]•[/red] {motivo}")
        sistema['pecas_reprovadas'].append(peca)


def listar_pecas_interface(sistema: SistemaArmazenamento) -> None:
    """
    Interface para listar peças aprovadas e/ou reprovadas com Rich.

    Args:
        sistema: Estado atual do sistema
    """
    console.print()
    console.print(Panel(
        "[bold white]LISTAR PEÇAS[/bold white]",
        border_style="cyan",
        box=INFO_BOX,
    ))
    console.print()

    console.print("[bold cyan]Opções:[/bold cyan]")
    console.print("  [green]a)[/green] Listar peças aprovadas")
    console.print("  [red]b)[/red] Listar peças reprovadas")
    console.print("  [yellow]c)[/yellow] Listar todas as peças")
    console.print()

    opcao = input("Escolha uma opção: ").strip().lower()

    console.print()
    if opcao == 'a':
        listar_pecas_aprovadas(sistema)
    elif opcao == 'b':
        listar_pecas_reprovadas(sistema)
    elif opcao == 'c':
        listar_pecas_aprovadas(sistema)
        console.print()
        listar_pecas_reprovadas(sistema)
    else:
        console.print(formatar_erro("Opção inválida"))


def listar_pecas_aprovadas(sistema: SistemaArmazenamento) -> None:
    """Lista todas as peças aprovadas com tabela Rich."""
    pecas = sistema['pecas_aprovadas']

    if not pecas:
        console.print(formatar_info("Nenhuma peça aprovada cadastrada"))
        return

    # Cria tabela de peças aprovadas
    table = Table(
        title=f"✅ [bold green]PEÇAS APROVADAS[/bold green] ({len(pecas)})",
        box=TABLE_BOX,
        show_header=True,
        header_style="bold magenta",
        border_style="green",
    )

    table.add_column("ID", style="cyan", width=12)
    table.add_column("Peso (g)", style="yellow", justify="right", width=10)
    table.add_column("Cor", style="magenta", width=12)
    table.add_column("Comprimento (cm)", style="blue", justify="right", width=18)

    for peca in pecas:
        table.add_row(
            peca['id'],
            f"{peca['peso']:.1f}",
            peca['cor'],
            f"{peca['comprimento']:.1f}",
        )

    console.print(table)


def listar_pecas_reprovadas(sistema: SistemaArmazenamento) -> None:
    """Lista todas as peças reprovadas com motivos em tabela Rich."""
    pecas = sistema['pecas_reprovadas']

    if not pecas:
        console.print(formatar_info("Nenhuma peça reprovada cadastrada"))
        return

    # Cria tabela de peças reprovadas
    table = Table(
        title=f"❌ [bold red]PEÇAS REPROVADAS[/bold red] ({len(pecas)})",
        box=TABLE_BOX,
        show_header=True,
        header_style="bold magenta",
        border_style="red",
        show_lines=True,  # Mostra linhas entre rows para separar peças
    )

    table.add_column("ID", style="cyan", width=12)
    table.add_column("Peso (g)", style="yellow", justify="right", width=10)
    table.add_column("Cor", style="magenta", width=12)
    table.add_column("Comprimento (cm)", style="blue", justify="right", width=18)
    table.add_column("Motivos de Reprovação", style="red", width=40)

    for peca in pecas:
        # Formata motivos como lista com bullets
        motivos_formatados = "\n".join(f"• {motivo}" for motivo in peca['motivos_reprovacao'])

        table.add_row(
            peca['id'],
            f"{peca['peso']:.1f}",
            peca['cor'],
            f"{peca['comprimento']:.1f}",
            motivos_formatados,
        )

    console.print(table)


def remover_peca_interface(sistema: SistemaArmazenamento) -> None:
    """
    Interface para remover uma peça cadastrada com Rich.

    Args:
        sistema: Estado atual do sistema
    """
    console.print()
    console.print(Panel(
        "[bold white]REMOVER PEÇA[/bold white]",
        border_style="red",
        box=INFO_BOX,
    ))
    console.print()

    id_peca = input("ID da peça a remover: ").strip()
    if not id_peca:
        console.print(formatar_erro("ID não pode ser vazio"))
        return

    confirmacao = input(f"Confirma remoção da peça '[cyan]{id_peca}[/cyan]'? (s/n): ").strip().lower()
    if confirmacao != 's':
        console.print(formatar_aviso("Operação cancelada"))
        return

    sucesso, mensagem = remover_peca_por_id(id_peca, sistema)
    console.print()
    if sucesso:
        console.print(formatar_sucesso(mensagem))
    else:
        console.print(formatar_erro(mensagem))


def listar_caixas_interface(sistema: SistemaArmazenamento) -> None:
    """
    Interface para listar todas as caixas (fechadas e atual) com Panels Rich.

    Args:
        sistema: Estado atual do sistema
    """
    console.print()
    console.print(Panel(
        "[bold white]LISTAGEM DE CAIXAS[/bold white]",
        border_style="cyan",
        box=INFO_BOX,
    ))
    console.print()

    caixas_fechadas = sistema['caixas_fechadas']
    caixa_atual = sistema['caixa_atual']

    if not caixas_fechadas and len(caixa_atual['pecas']) == 0:
        console.print(formatar_info("Nenhuma caixa com peças cadastradas"))
        return

    # Lista caixas fechadas
    if caixas_fechadas:
        console.print(f"\n[bold green]📦 CAIXAS FECHADAS ({len(caixas_fechadas)}):[/bold green]\n")

        for caixa in caixas_fechadas:
            # Cria conteúdo do painel
            conteudo = f"[bold cyan]Status:[/bold cyan] {formatar_status_caixa(caixa['fechada'])}\n"
            conteudo += f"[bold cyan]Capacidade:[/bold cyan] {len(caixa['pecas'])}/{CAPACIDADE_MAXIMA_CAIXA} peças\n"
            conteudo += f"[bold cyan]IDs das peças:[/bold cyan] {', '.join(p['id'] for p in caixa['pecas'])}"

            panel = Panel(
                conteudo,
                title=f"[bold white]Caixa #{caixa['id']}[/bold white]",
                border_style="green",
                box=INFO_BOX,
            )
            console.print(panel)

    # Lista caixa atual (em preenchimento)
    if len(caixa_atual['pecas']) > 0:
        console.print(f"\n[bold yellow]📦 CAIXA EM PREENCHIMENTO:[/bold yellow]\n")

        # Calcula progresso
        total_pecas = len(caixa_atual['pecas'])
        percentual = (total_pecas / CAPACIDADE_MAXIMA_CAIXA) * 100

        # Cria conteúdo do painel com progress bar
        conteudo = f"[bold cyan]Status:[/bold cyan] {formatar_status_caixa(caixa_atual['fechada'])}\n"
        conteudo += f"[bold cyan]Capacidade:[/bold cyan] {total_pecas}/{CAPACIDADE_MAXIMA_CAIXA} peças "
        conteudo += f"({percentual:.0f}%)\n"

        # Progress bar visual
        filled = int((total_pecas / CAPACIDADE_MAXIMA_CAIXA) * 20)
        bar = "█" * filled + "░" * (20 - filled)
        conteudo += f"[bold cyan]Progresso:[/bold cyan] [{bar}]\n"

        conteudo += f"[bold cyan]IDs das peças:[/bold cyan] {', '.join(p['id'] for p in caixa_atual['pecas'])}"

        panel = Panel(
            conteudo,
            title=f"[bold white]Caixa #{caixa_atual['id']}[/bold white]",
            border_style="yellow",
            box=INFO_BOX,
        )
        console.print(panel)


def gerar_relatorio_interface(sistema: SistemaArmazenamento) -> None:
    """
    Interface para gerar e exibir o relatório final com Layout Rich.

    Args:
        sistema: Estado atual do sistema
    """
    from services.relatorio import analisar_motivos_reprovacao

    console.print()

    # Calcula estatísticas
    total_aprovadas = len(sistema['pecas_aprovadas'])
    total_reprovadas = len(sistema['pecas_reprovadas'])
    total_processadas = total_aprovadas + total_reprovadas

    # Calcula percentuais
    if total_processadas > 0:
        percentual_aprovadas = (total_aprovadas / total_processadas) * 100
        percentual_reprovadas = (total_reprovadas / total_processadas) * 100
    else:
        percentual_aprovadas = 0.0
        percentual_reprovadas = 0.0

    # Contabiliza caixas
    total_caixas_fechadas = len(sistema['caixas_fechadas'])
    pecas_caixa_atual = len(sistema['caixa_atual']['pecas'])

    # Analisa motivos de reprovação
    contadores_motivos = analisar_motivos_reprovacao(sistema['pecas_reprovadas'])

    # === PAINEL 1: RESUMO GERAL ===
    resumo_content = f"""[bold cyan]Total de peças processadas:[/bold cyan] {formatar_valor_numerico(total_processadas, '')}

[bold green]✅ Peças aprovadas:[/bold green] {formatar_valor_numerico(total_aprovadas, '')} ({formatar_percentual(percentual_aprovadas)})
[bold red]❌ Peças reprovadas:[/bold red] {formatar_valor_numerico(total_reprovadas, '')} ({formatar_percentual(percentual_reprovadas)})
"""

    painel_resumo = Panel(
        resumo_content,
        title="[bold white]📊 RESUMO GERAL[/bold white]",
        border_style="blue",
        box=REPORT_BOX,
    )

    # === PAINEL 2: ARMAZENAMENTO ===
    if pecas_caixa_atual > 0:
        status_caixa = f"1 caixa ({pecas_caixa_atual}/10 peças)"
        percentual_caixa = (pecas_caixa_atual / 10) * 100
        barra = "█" * int(percentual_caixa / 5) + "░" * (20 - int(percentual_caixa / 5))
        status_visual = f"[{barra}] {percentual_caixa:.0f}%"
    else:
        status_caixa = "vazia"
        status_visual = "[" + "░" * 20 + "] 0%"

    armazenamento_content = f"""[bold cyan]Caixas fechadas:[/bold cyan] {formatar_valor_numerico(total_caixas_fechadas, '')}
[bold cyan]Caixa em preenchimento:[/bold cyan] {status_caixa}
{status_visual}
"""

    painel_armazenamento = Panel(
        armazenamento_content,
        title="[bold white]📦 ARMAZENAMENTO[/bold white]",
        border_style="green",
        box=REPORT_BOX,
    )

    # === PAINEL 3: DETALHAMENTO DE REPROVAÇÕES ===
    if total_reprovadas > 0:
        reprovacoes_content = f"""[bold red]Por peso inadequado:[/bold red] {formatar_valor_numerico(contadores_motivos['peso'], '')} peças
[bold red]Por cor inadequada:[/bold red] {formatar_valor_numerico(contadores_motivos['cor'], '')} peças
[bold red]Por comprimento inadequado:[/bold red] {formatar_valor_numerico(contadores_motivos['comprimento'], '')} peças
"""
    else:
        reprovacoes_content = "[bold green]Nenhuma peça reprovada! 🎉[/bold green]"

    painel_reprovacoes = Panel(
        reprovacoes_content,
        title="[bold white]❌ DETALHAMENTO DE REPROVAÇÕES[/bold white]",
        border_style="red",
        box=REPORT_BOX,
    )

    # Exibe título principal
    titulo_panel = Panel(
        "[bold white]RELATÓRIO FINAL DO SISTEMA[/bold white]",
        style="bold white on blue",
        box=REPORT_BOX,
    )
    console.print(titulo_panel)
    console.print()

    # Exibe painéis
    console.print(painel_resumo)
    console.print()
    console.print(painel_armazenamento)
    console.print()
    console.print(painel_reprovacoes)
