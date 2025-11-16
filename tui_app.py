#!/usr/bin/env python3
"""
Aplicação TUI interativa usando Textual
Interface moderna com navegação por setas inspirada em Charm/Bubble Tea
"""

from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Button, Static, Input, Label, DataTable, ListView, ListItem
from textual.containers import Container, Vertical, Horizontal, ScrollableContainer, VerticalScroll
from textual.binding import Binding
from textual import on
from rich.text import Text

from services.armazenamento import SistemaArmazenamento, inicializar_sistema, adicionar_peca_em_caixa, remover_peca_por_id
from models.peca import criar_peca
from services.validacao import validar_peca
from services.relatorio import analisar_motivos_reprovacao
from models.caixa import CAPACIDADE_MAXIMA_CAIXA
from utils.rich_styles import (
    ICON_FABRICA,
    ICON_CADASTRAR,
    ICON_LISTAR,
    ICON_REMOVER,
    ICON_CAIXA,
    ICON_RELATORIO,
    ICON_SAIR,
    ICON_SUCCESS,
    ICON_ERROR,
    ICON_WARNING,
)


# ============================================================================
# MENU PRINCIPAL
# ============================================================================

class MenuScreen(Screen):
    """Tela do menu principal com navegação por setas"""

    BINDINGS = [
        Binding("q", "quit", "Sair", priority=True),
        Binding("escape", "quit", "Sair", priority=True),
        Binding("1", "action_1", "Cadastrar"),
        Binding("2", "action_2", "Listar"),
        Binding("3", "action_3", "Remover"),
        Binding("4", "action_4", "Caixas"),
        Binding("5", "action_5", "Relatório"),
    ]

    def compose(self) -> ComposeResult:
        """Compõe o layout da tela"""
        yield Header()
        yield Static(f"\n[bold white]{ICON_FABRICA} SISTEMA DE GESTÃO DE PEÇAS[/bold white]\n", classes="title")
        yield Static("[cyan]Use as setas ↑↓ para navegar, Enter para selecionar[/cyan]\n", classes="subtitle")

        with ListView(id="menu_list"):
            yield ListItem(Label(f"{ICON_CADASTRAR} Cadastrar nova peça"))
            yield ListItem(Label(f"{ICON_LISTAR} Listar peças aprovadas/reprovadas"))
            yield ListItem(Label(f"{ICON_REMOVER} Remover peça cadastrada"))
            yield ListItem(Label(f"{ICON_CAIXA} Listar caixas fechadas"))
            yield ListItem(Label(f"{ICON_RELATORIO} Gerar relatório final"))
            yield ListItem(Label(f"{ICON_SAIR} Sair"))

        yield Footer()

    def on_mount(self) -> None:
        """Quando a tela é montada, dá foco no menu"""
        menu = self.query_one("#menu_list", ListView)
        menu.index = 0
        self.set_focus(menu)

    def action_action_1(self) -> None:
        """Cadastrar peça"""
        self.app.push_screen(CadastroScreen())

    def action_action_2(self) -> None:
        """Listar peças"""
        self.app.push_screen(ListagemScreen())

    def action_action_3(self) -> None:
        """Remover peça"""
        self.app.push_screen(RemoverScreen())

    def action_action_4(self) -> None:
        """Caixas"""
        self.app.push_screen(CaixasScreen())

    def action_action_5(self) -> None:
        """Relatório"""
        self.app.push_screen(RelatorioScreen())

    @on(ListView.Selected)
    def handle_menu_selection(self, event: ListView.Selected) -> None:
        """Lida com a seleção de menu"""
        menu = self.query_one("#menu_list", ListView)
        index = menu.index

        if index == 0:  # Cadastrar
            self.app.push_screen(CadastroScreen())
        elif index == 1:  # Listar
            self.app.push_screen(ListagemScreen())
        elif index == 2:  # Remover
            self.app.push_screen(RemoverScreen())
        elif index == 3:  # Caixas
            self.app.push_screen(CaixasScreen())
        elif index == 4:  # Relatório
            self.app.push_screen(RelatorioScreen())
        elif index == 5:  # Sair
            self.app.exit()


# ============================================================================
# TELA DE CADASTRO
# ============================================================================

class CadastroScreen(Screen):
    """Tela para cadastrar nova peça"""

    BINDINGS = [
        Binding("escape", "voltar", "Voltar", priority=True),
    ]

    def compose(self) -> ComposeResult:
        """Compõe o layout da tela"""
        yield Header()
        yield Container(
            Static(f"[bold cyan]{ICON_CADASTRAR} CADASTRAR NOVA PEÇA[/bold cyan]", classes="title"),
            ScrollableContainer(
                Label("ID da peça:"),
                Input(placeholder="Ex: P001", id="input_id"),
                Label("Peso (g):"),
                Input(placeholder="Ex: 100.0", id="input_peso"),
                Label("Cor:"),
                Input(placeholder="Ex: azul ou verde", id="input_cor"),
                Label("Comprimento (cm):"),
                Input(placeholder="Ex: 15.0", id="input_comprimento"),
                Horizontal(
                    Button("Cadastrar", variant="success", id="btn_cadastrar"),
                    Button("Cancelar", variant="error", id="btn_cancelar"),
                    classes="button_row"
                ),
                Static("", id="mensagem"),
                id="form_container"
            ),
            id="cadastro_container"
        )
        yield Footer()

    def action_voltar(self) -> None:
        """Volta para o menu principal"""
        self.app.pop_screen()

    @on(Button.Pressed, "#btn_cancelar")
    def cancelar(self) -> None:
        """Cancela o cadastro"""
        self.app.pop_screen()

    @on(Button.Pressed, "#btn_cadastrar")
    def cadastrar(self) -> None:
        """Cadastra a peça"""
        # Obtém os valores dos inputs
        id_peca = self.query_one("#input_id", Input).value.strip()
        peso_str = self.query_one("#input_peso", Input).value.strip()
        cor = self.query_one("#input_cor", Input).value.strip()
        comprimento_str = self.query_one("#input_comprimento", Input).value.strip()

        mensagem_widget = self.query_one("#mensagem", Static)

        # Validações básicas
        if not id_peca:
            mensagem_widget.update(f"[red]{ICON_ERROR} ID não pode ser vazio[/red]")
            return

        # Verifica se ID já existe
        sistema: SistemaArmazenamento = self.app.sistema  # type: ignore
        todas_pecas = sistema['pecas_aprovadas'] + sistema['pecas_reprovadas']
        if any(p['id'] == id_peca for p in todas_pecas):
            mensagem_widget.update(f"[red]{ICON_ERROR} Já existe uma peça com ID '{id_peca}'[/red]")
            return

        try:
            peso = float(peso_str)
        except ValueError:
            mensagem_widget.update(f"[red]{ICON_ERROR} Peso deve ser um número válido[/red]")
            return

        if not cor:
            mensagem_widget.update(f"[red]{ICON_ERROR} Cor não pode ser vazia[/red]")
            return

        try:
            comprimento = float(comprimento_str)
        except ValueError:
            mensagem_widget.update(f"[red]{ICON_ERROR} Comprimento deve ser um número válido[/red]")
            return

        # Cria e valida peça
        peca = criar_peca(id_peca, peso, cor, comprimento)
        aprovada, motivos = validar_peca(peca)
        peca['aprovada'] = aprovada
        peca['motivos_reprovacao'] = motivos

        if aprovada:
            _, msg = adicionar_peca_em_caixa(peca, sistema)
            mensagem_widget.update(
                f"[green]{ICON_SUCCESS} Peça {id_peca} APROVADA![/green]\n[cyan]{msg}[/cyan]"
            )
            # Limpa os campos
            self.query_one("#input_id", Input).value = ""
            self.query_one("#input_peso", Input).value = ""
            self.query_one("#input_cor", Input).value = ""
            self.query_one("#input_comprimento", Input).value = ""
        else:
            sistema['pecas_reprovadas'].append(peca)
            motivos_str = "\n".join(f"• {m}" for m in motivos)
            mensagem_widget.update(
                f"[red]{ICON_ERROR} Peça {id_peca} REPROVADA![/red]\n[yellow]Motivos:\n{motivos_str}[/yellow]"
            )


# ============================================================================
# TELA DE LISTAGEM
# ============================================================================

class ListagemScreen(Screen):
    """Tela para listar peças"""

    BINDINGS = [
        Binding("escape", "voltar", "Voltar", priority=True),
        Binding("a", "mostrar_aprovadas", "Aprovadas"),
        Binding("r", "mostrar_reprovadas", "Reprovadas"),
        Binding("t", "mostrar_todas", "Todas"),
    ]

    def compose(self) -> ComposeResult:
        """Compõe o layout da tela"""
        yield Header()
        yield Container(
            Static(f"[bold cyan]{ICON_LISTAR} LISTAGEM DE PEÇAS[/bold cyan]", classes="title"),
            Static("[cyan]Pressione: A=Aprovadas | R=Reprovadas | T=Todas | ESC=Voltar[/cyan]", classes="subtitle"),
            ScrollableContainer(
                Static("", id="tabela_aprovadas"),
                Static("", id="tabela_reprovadas"),
                id="listagem_content"
            ),
            id="listagem_container"
        )
        yield Footer()

    def on_mount(self) -> None:
        """Quando a tela é montada, mostra todas as peças"""
        self.action_mostrar_todas()

    def action_voltar(self) -> None:
        """Volta para o menu principal"""
        self.app.pop_screen()

    def action_mostrar_aprovadas(self) -> None:
        """Mostra apenas peças aprovadas"""
        self._mostrar_aprovadas()
        self.query_one("#tabela_reprovadas", Static).update("")

    def action_mostrar_reprovadas(self) -> None:
        """Mostra apenas peças reprovadas"""
        self.query_one("#tabela_aprovadas", Static).update("")
        self._mostrar_reprovadas()

    def action_mostrar_todas(self) -> None:
        """Mostra todas as peças"""
        self._mostrar_aprovadas()
        self._mostrar_reprovadas()

    def _mostrar_aprovadas(self) -> None:
        """Mostra tabela de peças aprovadas"""
        sistema: SistemaArmazenamento = self.app.sistema  # type: ignore
        pecas = sistema['pecas_aprovadas']

        if not pecas:
            self.query_one("#tabela_aprovadas", Static).update(
                f"[yellow]{ICON_WARNING} Nenhuma peça aprovada cadastrada[/yellow]\n"
            )
            return

        content = f"\n[bold green]✅ PEÇAS APROVADAS ({len(pecas)})[/bold green]\n\n"
        content += "[bold]ID          Peso(g)  Cor          Comprimento(cm)[/bold]\n"
        content += "─" * 60 + "\n"

        for peca in pecas:
            content += f"{peca['id']:<12}{peca['peso']:>7.1f}  {peca['cor']:<12}{peca['comprimento']:>15.1f}\n"

        self.query_one("#tabela_aprovadas", Static).update(content)

    def _mostrar_reprovadas(self) -> None:
        """Mostra tabela de peças reprovadas"""
        sistema: SistemaArmazenamento = self.app.sistema  # type: ignore
        pecas = sistema['pecas_reprovadas']

        if not pecas:
            self.query_one("#tabela_reprovadas", Static).update(
                f"[yellow]{ICON_WARNING} Nenhuma peça reprovada cadastrada[/yellow]\n"
            )
            return

        content = f"\n[bold red]❌ PEÇAS REPROVADAS ({len(pecas)})[/bold red]\n\n"

        for peca in pecas:
            content += f"[bold cyan]ID:[/bold cyan] {peca['id']}\n"
            content += f"  Peso: {peca['peso']:.1f}g | Cor: {peca['cor']} | Comprimento: {peca['comprimento']:.1f}cm\n"
            content += f"  [red]Motivos:[/red]\n"
            for motivo in peca['motivos_reprovacao']:
                content += f"    • {motivo}\n"
            content += "\n"

        self.query_one("#tabela_reprovadas", Static).update(content)


# ============================================================================
# TELA DE REMOÇÃO
# ============================================================================

class RemoverScreen(Screen):
    """Tela para remover peça"""

    BINDINGS = [
        Binding("escape", "voltar", "Voltar", priority=True),
    ]

    def compose(self) -> ComposeResult:
        """Compõe o layout da tela"""
        yield Header()
        yield Container(
            Static(f"[bold red]{ICON_REMOVER} REMOVER PEÇA[/bold red]", classes="title"),
            ScrollableContainer(
                Label("ID da peça a remover:"),
                Input(placeholder="Ex: P001", id="input_id_remover"),
                Horizontal(
                    Button("Remover", variant="error", id="btn_remover"),
                    Button("Cancelar", variant="default", id="btn_cancelar_remover"),
                    classes="button_row"
                ),
                Static("", id="mensagem_remover"),
                id="remover_form"
            ),
            id="remover_container"
        )
        yield Footer()

    def action_voltar(self) -> None:
        """Volta para o menu principal"""
        self.app.pop_screen()

    @on(Button.Pressed, "#btn_cancelar_remover")
    def cancelar(self) -> None:
        """Cancela a remoção"""
        self.app.pop_screen()

    @on(Button.Pressed, "#btn_remover")
    def remover(self) -> None:
        """Remove a peça"""
        id_peca = self.query_one("#input_id_remover", Input).value.strip()
        mensagem_widget = self.query_one("#mensagem_remover", Static)

        if not id_peca:
            mensagem_widget.update(f"[red]{ICON_ERROR} ID não pode ser vazio[/red]")
            return

        sistema: SistemaArmazenamento = self.app.sistema  # type: ignore
        sucesso, mensagem = remover_peca_por_id(id_peca, sistema)

        if sucesso:
            mensagem_widget.update(f"[green]{ICON_SUCCESS} {mensagem}[/green]")
            self.query_one("#input_id_remover", Input).value = ""
        else:
            mensagem_widget.update(f"[red]{ICON_ERROR} {mensagem}[/red]")


# ============================================================================
# TELA DE CAIXAS
# ============================================================================

class CaixasScreen(Screen):
    """Tela para visualizar caixas"""

    BINDINGS = [
        Binding("escape", "voltar", "Voltar", priority=True),
    ]

    def compose(self) -> ComposeResult:
        """Compõe o layout da tela"""
        yield Header()
        yield Container(
            Static(f"[bold cyan]{ICON_CAIXA} VISUALIZAÇÃO DE CAIXAS[/bold cyan]", classes="title"),
            ScrollableContainer(
                Static("", id="caixas_content"),
                id="caixas_scroll"
            ),
            id="caixas_container"
        )
        yield Footer()

    def on_mount(self) -> None:
        """Quando a tela é montada, carrega as caixas"""
        self._carregar_caixas()

    def action_voltar(self) -> None:
        """Volta para o menu principal"""
        self.app.pop_screen()

    def _carregar_caixas(self) -> None:
        """Carrega e exibe as caixas"""
        sistema: SistemaArmazenamento = self.app.sistema  # type: ignore
        caixas_fechadas = sistema['caixas_fechadas']
        caixa_atual = sistema['caixa_atual']

        content = ""

        if not caixas_fechadas and len(caixa_atual['pecas']) == 0:
            content = f"[yellow]{ICON_WARNING} Nenhuma caixa com peças cadastradas[/yellow]"
        else:
            # Caixas fechadas
            if caixas_fechadas:
                content += f"[bold green]📦 CAIXAS FECHADAS ({len(caixas_fechadas)})[/bold green]\n\n"
                for caixa in caixas_fechadas:
                    content += f"[bold cyan]Caixa #{caixa['id']}[/bold cyan]\n"
                    content += f"  Status: 🔒 Fechada\n"
                    content += f"  Capacidade: {len(caixa['pecas'])}/{CAPACIDADE_MAXIMA_CAIXA} peças\n"
                    content += f"  IDs: {', '.join(p['id'] for p in caixa['pecas'])}\n\n"

            # Caixa atual
            if len(caixa_atual['pecas']) > 0:
                total_pecas = len(caixa_atual['pecas'])
                percentual = (total_pecas / CAPACIDADE_MAXIMA_CAIXA) * 100
                filled = int((total_pecas / CAPACIDADE_MAXIMA_CAIXA) * 20)
                bar = "█" * filled + "░" * (20 - filled)

                content += f"[bold yellow]📦 CAIXA EM PREENCHIMENTO[/bold yellow]\n\n"
                content += f"[bold cyan]Caixa #{caixa_atual['id']}[/bold cyan]\n"
                content += f"  Status: 🔓 Em preenchimento\n"
                content += f"  Capacidade: {total_pecas}/{CAPACIDADE_MAXIMA_CAIXA} peças ({percentual:.0f}%)\n"
                content += f"  Progresso: [{bar}]\n"
                content += f"  IDs: {', '.join(p['id'] for p in caixa_atual['pecas'])}\n"

        self.query_one("#caixas_content", Static).update(content)


# ============================================================================
# TELA DE RELATÓRIOS
# ============================================================================

class RelatorioScreen(Screen):
    """Tela para visualizar relatórios"""

    BINDINGS = [
        Binding("escape", "voltar", "Voltar", priority=True),
    ]

    def compose(self) -> ComposeResult:
        """Compõe o layout da tela"""
        yield Header()
        yield Container(
            Static(f"[bold cyan]{ICON_RELATORIO} RELATÓRIO FINAL DO SISTEMA[/bold cyan]", classes="title"),
            ScrollableContainer(
                Static("", id="relatorio_content"),
                id="relatorio_scroll"
            ),
            id="relatorio_container"
        )
        yield Footer()

    def on_mount(self) -> None:
        """Quando a tela é montada, gera o relatório"""
        self._gerar_relatorio()

    def action_voltar(self) -> None:
        """Volta para o menu principal"""
        self.app.pop_screen()

    def _gerar_relatorio(self) -> None:
        """Gera e exibe o relatório"""
        sistema: SistemaArmazenamento = self.app.sistema  # type: ignore

        total_aprovadas = len(sistema['pecas_aprovadas'])
        total_reprovadas = len(sistema['pecas_reprovadas'])
        total_processadas = total_aprovadas + total_reprovadas

        if total_processadas > 0:
            percentual_aprovadas = (total_aprovadas / total_processadas) * 100
            percentual_reprovadas = (total_reprovadas / total_processadas) * 100
        else:
            percentual_aprovadas = 0.0
            percentual_reprovadas = 0.0

        total_caixas_fechadas = len(sistema['caixas_fechadas'])
        pecas_caixa_atual = len(sistema['caixa_atual']['pecas'])

        contadores_motivos = analisar_motivos_reprovacao(sistema['pecas_reprovadas'])

        content = f"""
[bold white]═══════════════════════════════════════════════════════[/bold white]
[bold cyan]                    📊 RESUMO GERAL                    [/bold cyan]
[bold white]═══════════════════════════════════════════════════════[/bold white]

[bold]Total de peças processadas:[/bold] {total_processadas}

[green]✅ Peças aprovadas:[/green] {total_aprovadas} ({percentual_aprovadas:.1f}%)
[red]❌ Peças reprovadas:[/red] {total_reprovadas} ({percentual_reprovadas:.1f}%)

[bold white]═══════════════════════════════════════════════════════[/bold white]
[bold cyan]                   📦 ARMAZENAMENTO                    [/bold cyan]
[bold white]═══════════════════════════════════════════════════════[/bold white]

[bold]Caixas fechadas:[/bold] {total_caixas_fechadas}
"""

        if pecas_caixa_atual > 0:
            percentual_caixa = (pecas_caixa_atual / 10) * 100
            filled = int(percentual_caixa / 5)
            barra = "█" * filled + "░" * (20 - filled)
            content += f"[bold]Caixa em preenchimento:[/bold] 1 caixa ({pecas_caixa_atual}/10 peças)\n"
            content += f"  [{barra}] {percentual_caixa:.0f}%\n"
        else:
            content += f"[bold]Caixa em preenchimento:[/bold] vazia\n"

        content += f"""
[bold white]═══════════════════════════════════════════════════════[/bold white]
[bold cyan]            ❌ DETALHAMENTO DE REPROVAÇÕES            [/bold cyan]
[bold white]═══════════════════════════════════════════════════════[/bold white]
"""

        if total_reprovadas > 0:
            content += f"""
[red]Por peso inadequado:[/red] {contadores_motivos['peso']} peças
[red]Por cor inadequada:[/red] {contadores_motivos['cor']} peças
[red]Por comprimento inadequado:[/red] {contadores_motivos['comprimento']} peças
"""
        else:
            content += "\n[bold green]Nenhuma peça reprovada! 🎉[/bold green]\n"

        self.query_one("#relatorio_content", Static).update(content)


# ============================================================================
# APLICAÇÃO PRINCIPAL
# ============================================================================

class PecasApp(App):
    """Aplicação principal do sistema TUI"""

    CSS_PATH = "tui_styles.tcss"

    BINDINGS = [
        Binding("q", "quit", "Sair", priority=True),
    ]

    def __init__(self):
        """Inicializa a aplicação"""
        super().__init__()
        self.sistema: SistemaArmazenamento = inicializar_sistema()

    def on_mount(self) -> None:
        """Quando a aplicação é montada"""
        self.title = "Sistema de Gestão de Peças"
        self.sub_title = "Navegue com as setas ↑↓ | Enter para selecionar | Q ou ESC para sair"
        self.push_screen(MenuScreen())


def run_tui_app() -> None:
    """Executa a aplicação TUI interativa"""
    app = PecasApp()
    app.run()


if __name__ == "__main__":
    run_tui_app()
