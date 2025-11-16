"""
Testes unitários para o módulo de geração de relatórios.

Testa:
- Geração de relatório completo com estatísticas
- Total de peças aprovadas
- Total de peças reprovadas e motivos
- Quantidade de caixas utilizadas
- Cálculos de percentuais
"""

import pytest
from models.peca import criar_peca
from services.relatorio import (
    gerar_relatorio_completo,
    gerar_estatisticas_reprovacao,
    analisar_motivos_reprovacao
)


# ========================================
# TESTES DE ANÁLISE DE MOTIVOS
# ========================================

class TestAnalisarMotivosReprovacao:
    """Testes para a função analisar_motivos_reprovacao()."""

    @pytest.mark.unit
    def test_lista_vazia_retorna_zeros(self):
        """Lista vazia deve retornar todos os contadores zerados."""
        contadores = analisar_motivos_reprovacao([])

        assert contadores['peso'] == 0
        assert contadores['cor'] == 0
        assert contadores['comprimento'] == 0

    @pytest.mark.unit
    def test_contar_reprovacao_por_peso(self):
        """Contar corretamente reprovações por peso."""
        pecas = [
            criar_peca("P001", 120.0, "azul", 15.0, False,
                      ["Peso fora do intervalo (95.0-105.0g): 120.0g"])
        ]

        contadores = analisar_motivos_reprovacao(pecas)

        assert contadores['peso'] == 1
        assert contadores['cor'] == 0
        assert contadores['comprimento'] == 0

    @pytest.mark.unit
    def test_contar_reprovacao_por_cor(self):
        """Contar corretamente reprovações por cor."""
        pecas = [
            criar_peca("P001", 100.0, "vermelho", 15.0, False,
                      ["Cor inadequada (esperado: azul ou verde): vermelho"])
        ]

        contadores = analisar_motivos_reprovacao(pecas)

        assert contadores['peso'] == 0
        assert contadores['cor'] == 1
        assert contadores['comprimento'] == 0

    @pytest.mark.unit
    def test_contar_reprovacao_por_comprimento(self):
        """Contar corretamente reprovações por comprimento."""
        pecas = [
            criar_peca("P001", 100.0, "azul", 25.0, False,
                      ["Comprimento fora do intervalo (10.0-20.0cm): 25.0cm"])
        ]

        contadores = analisar_motivos_reprovacao(pecas)

        assert contadores['peso'] == 0
        assert contadores['cor'] == 0
        assert contadores['comprimento'] == 1

    @pytest.mark.unit
    def test_contar_multiplos_motivos_mesma_peca(self):
        """Peça com múltiplos motivos deve incrementar múltiplos contadores."""
        pecas = [
            criar_peca("P001", 120.0, "vermelho", 25.0, False, [
                "Peso fora do intervalo (95.0-105.0g): 120.0g",
                "Cor inadequada (esperado: azul ou verde): vermelho",
                "Comprimento fora do intervalo (10.0-20.0cm): 25.0cm"
            ])
        ]

        contadores = analisar_motivos_reprovacao(pecas)

        assert contadores['peso'] == 1
        assert contadores['cor'] == 1
        assert contadores['comprimento'] == 1

    @pytest.mark.unit
    def test_contar_multiplas_pecas_mesmo_motivo(self):
        """Múltiplas peças com mesmo motivo devem incrementar contador."""
        pecas = [
            criar_peca("P001", 120.0, "azul", 15.0, False,
                      ["Peso fora do intervalo (95.0-105.0g): 120.0g"]),
            criar_peca("P002", 90.0, "verde", 15.0, False,
                      ["Peso fora do intervalo (95.0-105.0g): 90.0g"]),
            criar_peca("P003", 150.0, "azul", 15.0, False,
                      ["Peso fora do intervalo (95.0-105.0g): 150.0g"])
        ]

        contadores = analisar_motivos_reprovacao(pecas)

        assert contadores['peso'] == 3
        assert contadores['cor'] == 0
        assert contadores['comprimento'] == 0

    @pytest.mark.unit
    def test_mix_de_motivos_diversas_pecas(self):
        """Mix de motivos em diversas peças."""
        pecas = [
            criar_peca("P001", 120.0, "azul", 15.0, False, ["Peso fora..."]),
            criar_peca("P002", 100.0, "vermelho", 15.0, False, ["Cor inadequada..."]),
            criar_peca("P003", 100.0, "azul", 25.0, False, ["Comprimento fora..."]),
            criar_peca("P004", 90.0, "amarelo", 5.0, False,
                      ["Peso fora...", "Cor inadequada...", "Comprimento fora..."])
        ]

        contadores = analisar_motivos_reprovacao(pecas)

        assert contadores['peso'] == 2
        assert contadores['cor'] == 2
        assert contadores['comprimento'] == 2

    @pytest.mark.unit
    def test_case_insensitive(self):
        """Análise deve ser case-insensitive."""
        pecas = [
            criar_peca("P001", 120.0, "azul", 15.0, False, ["PESO fora..."]),
            criar_peca("P002", 100.0, "vermelho", 15.0, False, ["COR inadequada..."]),
            criar_peca("P003", 100.0, "azul", 25.0, False, ["Comprimento FORA..."])
        ]

        contadores = analisar_motivos_reprovacao(pecas)

        assert contadores['peso'] == 1
        assert contadores['cor'] == 1
        assert contadores['comprimento'] == 1


# ========================================
# TESTES DE ESTATÍSTICAS DE REPROVAÇÃO
# ========================================

class TestGerarEstatisticasReprovacao:
    """Testes para a função gerar_estatisticas_reprovacao()."""

    @pytest.mark.unit
    def test_retorna_estrutura_correta(self):
        """Deve retornar EstatisticasReprovacao com campos corretos."""
        pecas = []
        stats = gerar_estatisticas_reprovacao(pecas)

        assert 'peso_inadequado' in stats
        assert 'cor_inadequada' in stats
        assert 'comprimento_inadequado' in stats

    @pytest.mark.unit
    def test_estatisticas_lista_vazia(self):
        """Estatísticas de lista vazia devem ser todas zero."""
        stats = gerar_estatisticas_reprovacao([])

        assert stats['peso_inadequado'] == 0
        assert stats['cor_inadequada'] == 0
        assert stats['comprimento_inadequado'] == 0

    @pytest.mark.unit
    def test_estatisticas_com_dados(self, sistema_com_pecas_reprovadas):
        """Estatísticas devem refletir os dados corretamente."""
        pecas = sistema_com_pecas_reprovadas['pecas_reprovadas']
        stats = gerar_estatisticas_reprovacao(pecas)

        # A fixture tem 3 peças, cada uma com 1 motivo diferente
        total = stats['peso_inadequado'] + stats['cor_inadequada'] + stats['comprimento_inadequado']
        assert total == 3


# ========================================
# TESTES DE RELATÓRIO COMPLETO
# ========================================

class TestGerarRelatorioCompleto:
    """Testes para a função gerar_relatorio_completo()."""

    @pytest.mark.unit
    def test_relatorio_sistema_vazio(self, sistema_vazio):
        """Relatório de sistema vazio deve mostrar zeros."""
        relatorio = gerar_relatorio_completo(sistema_vazio)

        assert "Total de peças processadas: 0" in relatorio
        assert "Peças aprovadas: 0" in relatorio
        assert "Peças reprovadas: 0" in relatorio
        assert "Caixas fechadas: 0" in relatorio

    @pytest.mark.unit
    def test_relatorio_contem_titulo(self, sistema_vazio):
        """Relatório deve conter título formatado."""
        relatorio = gerar_relatorio_completo(sistema_vazio)

        assert "RELATÓRIO FINAL" in relatorio
        assert "=" in relatorio

    @pytest.mark.unit
    def test_relatorio_mostra_total_processadas(self, sistema_com_pecas_aprovadas):
        """Relatório deve mostrar total de peças processadas."""
        sistema = sistema_com_pecas_aprovadas
        total = len(sistema['pecas_aprovadas']) + len(sistema['pecas_reprovadas'])

        relatorio = gerar_relatorio_completo(sistema)

        assert f"Total de peças processadas: {total}" in relatorio

    @pytest.mark.unit
    def test_relatorio_mostra_aprovadas(self, sistema_com_pecas_aprovadas):
        """Relatório deve mostrar quantidade de peças aprovadas."""
        sistema = sistema_com_pecas_aprovadas
        total_aprovadas = len(sistema['pecas_aprovadas'])

        relatorio = gerar_relatorio_completo(sistema)

        assert f"Peças aprovadas: {total_aprovadas}" in relatorio

    @pytest.mark.unit
    def test_relatorio_mostra_reprovadas(self, sistema_com_pecas_reprovadas):
        """Relatório deve mostrar quantidade de peças reprovadas."""
        sistema = sistema_com_pecas_reprovadas
        total_reprovadas = len(sistema['pecas_reprovadas'])

        relatorio = gerar_relatorio_completo(sistema)

        assert f"Peças reprovadas: {total_reprovadas}" in relatorio

    @pytest.mark.unit
    def test_relatorio_calcula_percentual_aprovadas(self, sistema_com_pecas_aprovadas):
        """Relatório deve calcular percentual de aprovadas corretamente."""
        sistema = sistema_com_pecas_aprovadas
        relatorio = gerar_relatorio_completo(sistema)

        # Sistema tem apenas aprovadas, então deve ser 100%
        assert "100.0%" in relatorio or "(100%" in relatorio

    @pytest.mark.unit
    def test_relatorio_calcula_percentual_reprovadas(self, sistema_com_pecas_reprovadas):
        """Relatório deve calcular percentual de reprovadas corretamente."""
        sistema = sistema_com_pecas_reprovadas
        relatorio = gerar_relatorio_completo(sistema)

        # Sistema tem apenas reprovadas, então deve ser 100%
        assert "100.0%" in relatorio or "(100%" in relatorio

    @pytest.mark.unit
    def test_relatorio_mostra_caixas_fechadas(self, sistema_com_multiplas_caixas):
        """Relatório deve mostrar quantidade de caixas fechadas."""
        sistema = sistema_com_multiplas_caixas
        total_fechadas = len(sistema['caixas_fechadas'])

        relatorio = gerar_relatorio_completo(sistema)

        assert f"Caixas fechadas: {total_fechadas}" in relatorio

    @pytest.mark.unit
    def test_relatorio_mostra_caixa_atual(self, sistema_com_pecas_aprovadas):
        """Relatório deve mostrar status da caixa em preenchimento."""
        sistema = sistema_com_pecas_aprovadas
        pecas_caixa = len(sistema['caixa_atual']['pecas'])

        relatorio = gerar_relatorio_completo(sistema)

        assert f"{pecas_caixa}/10" in relatorio

    @pytest.mark.unit
    def test_relatorio_caixa_vazia(self, sistema_vazio):
        """Relatório deve indicar quando caixa está vazia."""
        relatorio = gerar_relatorio_completo(sistema_vazio)

        assert "vazia" in relatorio.lower()

    @pytest.mark.unit
    def test_relatorio_mostra_detalhamento_reprovacoes(self, sistema_com_pecas_reprovadas):
        """Relatório deve detalhar motivos de reprovação."""
        relatorio = gerar_relatorio_completo(sistema_com_pecas_reprovadas)

        assert "DETALHAMENTO DE REPROVAÇÕES" in relatorio
        assert "peso inadequado" in relatorio.lower()
        assert "cor inadequada" in relatorio.lower()
        assert "comprimento inadequado" in relatorio.lower()

    @pytest.mark.unit
    def test_relatorio_sem_reprovacoes_nao_mostra_detalhamento(self, sistema_com_pecas_aprovadas):
        """Relatório sem reprovações não deve mostrar seção de detalhamento."""
        relatorio = gerar_relatorio_completo(sistema_com_pecas_aprovadas)

        assert "DETALHAMENTO DE REPROVAÇÕES" not in relatorio

    @pytest.mark.unit
    def test_relatorio_usa_emojis(self, sistema_vazio):
        """Relatório deve usar emojis para melhor visualização."""
        relatorio = gerar_relatorio_completo(sistema_vazio)

        assert "📊" in relatorio or "RESUMO" in relatorio
        assert "📦" in relatorio or "ARMAZENAMENTO" in relatorio

    @pytest.mark.unit
    def test_percentual_50_50(self):
        """Teste com 50% aprovadas e 50% reprovadas."""
        from services.armazenamento import inicializar_sistema

        sistema = inicializar_sistema()

        # Adicionar 5 aprovadas
        for i in range(5):
            peca = criar_peca(f"PA{i}", 100.0, "azul", 15.0, True)
            sistema['pecas_aprovadas'].append(peca)

        # Adicionar 5 reprovadas
        for i in range(5):
            peca = criar_peca(f"PR{i}", 120.0, "vermelho", 15.0, False, ["Peso", "Cor"])
            sistema['pecas_reprovadas'].append(peca)

        relatorio = gerar_relatorio_completo(sistema)

        assert "50.0%" in relatorio

    @pytest.mark.unit
    @pytest.mark.edge_case
    def test_divisao_por_zero_protegida(self, sistema_vazio):
        """Sistema vazio não deve causar erro de divisão por zero."""
        # Não deve lançar exceção
        relatorio = gerar_relatorio_completo(sistema_vazio)

        assert relatorio is not None
        assert "0.0%" in relatorio or "(0%" in relatorio

    @pytest.mark.unit
    def test_relatorio_e_string(self, sistema_vazio):
        """Relatório deve retornar uma string."""
        relatorio = gerar_relatorio_completo(sistema_vazio)

        assert isinstance(relatorio, str)
        assert len(relatorio) > 0

    @pytest.mark.unit
    def test_relatorio_formatacao_multiplas_linhas(self, sistema_vazio):
        """Relatório deve ter múltiplas linhas."""
        relatorio = gerar_relatorio_completo(sistema_vazio)

        linhas = relatorio.split('\n')
        assert len(linhas) > 5

    @pytest.mark.unit
    def test_relatorio_contem_secoes(self, sistema_com_multiplas_caixas):
        """Relatório deve conter todas as seções principais."""
        relatorio = gerar_relatorio_completo(sistema_com_multiplas_caixas)

        assert "RESUMO GERAL" in relatorio
        assert "ARMAZENAMENTO" in relatorio

    @pytest.mark.unit
    def test_valores_numericos_corretos(self):
        """Valores numéricos no relatório devem estar corretos."""
        from services.armazenamento import inicializar_sistema

        sistema = inicializar_sistema()

        # Adicionar 7 aprovadas
        for i in range(7):
            peca = criar_peca(f"PA{i}", 100.0, "azul", 15.0, True)
            sistema['pecas_aprovadas'].append(peca)
            sistema['caixa_atual']['pecas'].append(peca)

        # Adicionar 3 reprovadas
        for i in range(3):
            peca = criar_peca(f"PR{i}", 120.0, "azul", 15.0, False, ["Peso fora..."])
            sistema['pecas_reprovadas'].append(peca)

        relatorio = gerar_relatorio_completo(sistema)

        assert "Total de peças processadas: 10" in relatorio
        assert "Peças aprovadas: 7" in relatorio
        assert "Peças reprovadas: 3" in relatorio
        assert "70.0%" in relatorio  # 7/10 = 70%
        assert "30.0%" in relatorio  # 3/10 = 30%

    @pytest.mark.unit
    def test_motivos_reprovacao_contados_corretamente(self):
        """Motivos de reprovação devem ser contados corretamente."""
        from services.armazenamento import inicializar_sistema

        sistema = inicializar_sistema()

        # 2 peças com peso inválido
        for i in range(2):
            peca = criar_peca(f"PP{i}", 120.0, "azul", 15.0, False,
                            ["Peso fora do intervalo (95.0-105.0g): 120.0g"])
            sistema['pecas_reprovadas'].append(peca)

        # 1 peça com cor inválida
        peca = criar_peca("PC1", 100.0, "vermelho", 15.0, False,
                         ["Cor inadequada (esperado: azul ou verde): vermelho"])
        sistema['pecas_reprovadas'].append(peca)

        relatorio = gerar_relatorio_completo(sistema)

        assert "Por peso inadequado: 2 peças" in relatorio
        assert "Por cor inadequada: 1 peças" in relatorio or "Por cor inadequada: 1 peça" in relatorio
        assert "Por comprimento inadequado: 0 peças" in relatorio
