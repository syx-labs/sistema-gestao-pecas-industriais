"""
Testes de cenários reais de produção.

Simula casos de uso reais do sistema:
- Produção de 25 peças (exemplo do README)
- Dias de produção com diferentes taxas de aprovação
- Casos extremos de produção
"""

import pytest
from models.peca import criar_peca
from services.validacao import validar_peca
from services.armazenamento import inicializar_sistema, adicionar_peca_em_caixa
from services.relatorio import gerar_relatorio_completo


# ========================================
# CENÁRIO DO README (25 PEÇAS)
# ========================================

class TestCenarioREADME:
    """
    Cenário descrito no README: 25 peças processadas.
    18 aprovadas (72%) e 7 reprovadas (28%).
    """

    @pytest.mark.integration
    def test_cenario_readme_25_pecas(self):
        """Simular o cenário exato descrito no README."""
        sistema = inicializar_sistema()

        # 18 peças aprovadas
        pecas_aprovadas_dados = [
            ("P001", 100.0, "azul", 15.0),
            ("P003", 98.5, "verde", 17.0),
            ("P005", 102.0, "azul", 12.5),
            ("P006", 95.0, "verde", 10.0),
            ("P008", 100.0, "azul", 15.0),
            ("P010", 105.0, "verde", 20.0),
            ("P011", 97.0, "azul", 14.0),
            ("P013", 100.0, "verde", 16.0),
            ("P014", 103.0, "azul", 18.0),
            ("P016", 99.0, "verde", 13.0),
            ("P017", 100.0, "azul", 15.0),
            ("P019", 96.0, "verde", 11.0),
            ("P020", 104.0, "azul", 19.0),
            ("P022", 100.0, "verde", 15.0),
            ("P023", 98.0, "azul", 17.0),
            ("P024", 101.0, "verde", 14.0),
            ("P025", 100.0, "azul", 15.0),
            ("P026", 99.5, "verde", 16.5),
        ]

        for id_peca, peso, cor, comprimento in pecas_aprovadas_dados:
            peca = criar_peca(id_peca, peso, cor, comprimento)
            aprovada, motivos = validar_peca(peca)
            peca['aprovada'] = aprovada
            peca['motivos_reprovacao'] = motivos
            assert aprovada is True
            adicionar_peca_em_caixa(peca, sistema)

        # 7 peças reprovadas com diferentes motivos
        pecas_reprovadas_dados = [
            ("P002", 120.0, "azul", 15.0),       # Peso
            ("P004", 90.0, "verde", 15.0),       # Peso
            ("P007", 100.0, "vermelho", 15.0),   # Cor
            ("P009", 100.0, "amarelo", 15.0),    # Cor
            ("P012", 100.0, "azul", 25.0),       # Comprimento
            ("P015", 110.0, "roxo", 5.0),        # Todos
            ("P018", 85.0, "preto", 22.0),       # Todos
        ]

        for id_peca, peso, cor, comprimento in pecas_reprovadas_dados:
            peca = criar_peca(id_peca, peso, cor, comprimento)
            aprovada, motivos = validar_peca(peca)
            peca['aprovada'] = aprovada
            peca['motivos_reprovacao'] = motivos
            assert aprovada is False
            sistema['pecas_reprovadas'].append(peca)

        # Verificar totais
        assert len(sistema['pecas_aprovadas']) == 18
        assert len(sistema['pecas_reprovadas']) == 7

        # Verificar caixas (18 peças = 1 caixa fechada + 8 na atual)
        assert len(sistema['caixas_fechadas']) == 1
        assert len(sistema['caixa_atual']['pecas']) == 8

        # Verificar relatório
        relatorio = gerar_relatorio_completo(sistema)
        assert "Total de peças processadas: 25" in relatorio
        assert "Peças aprovadas: 18 (72.0%)" in relatorio
        assert "Peças reprovadas: 7 (28.0%)" in relatorio
        assert "Caixas fechadas: 1" in relatorio
        assert "8/10 peças" in relatorio


# ========================================
# CENÁRIOS DE PRODUÇÃO DIÁRIA
# ========================================

class TestCenariosProducaoDiaria:
    """Cenários simulando dias de produção."""

    @pytest.mark.integration
    def test_dia_producao_perfeito(self):
        """Dia de produção com 100% de aprovação."""
        sistema = inicializar_sistema()

        # 30 peças todas aprovadas
        for i in range(30):
            peca = criar_peca(f"P{i:03d}", 100.0, "azul" if i % 2 == 0 else "verde", 15.0)
            aprovada, _ = validar_peca(peca)
            peca['aprovada'] = aprovada
            adicionar_peca_em_caixa(peca, sistema)

        assert len(sistema['pecas_aprovadas']) == 30
        assert len(sistema['pecas_reprovadas']) == 0

        # 3 caixas fechadas
        assert len(sistema['caixas_fechadas']) == 3

        relatorio = gerar_relatorio_completo(sistema)
        assert "100.0%" in relatorio
        assert "Caixas fechadas: 3" in relatorio

    @pytest.mark.integration
    def test_dia_producao_ruim(self):
        """Dia de produção com alta taxa de reprovação."""
        sistema = inicializar_sistema()

        # 20 peças: 5 aprovadas, 15 reprovadas
        for i in range(5):
            peca = criar_peca(f"PA{i:03d}", 100.0, "azul", 15.0)
            aprovada, _ = validar_peca(peca)
            peca['aprovada'] = aprovada
            adicionar_peca_em_caixa(peca, sistema)

        for i in range(15):
            # Peso variando fora do intervalo
            peso = 85.0 + (i * 3)  # 85, 88, 91, ..., 130
            peca = criar_peca(f"PR{i:03d}", peso, "azul", 15.0)
            aprovada, motivos = validar_peca(peca)
            peca['aprovada'] = aprovada
            peca['motivos_reprovacao'] = motivos
            sistema['pecas_reprovadas'].append(peca)

        assert len(sistema['pecas_aprovadas']) == 5
        assert len(sistema['pecas_reprovadas']) == 15

        relatorio = gerar_relatorio_completo(sistema)
        assert "Peças aprovadas: 5 (25.0%)" in relatorio
        assert "Peças reprovadas: 15 (75.0%)" in relatorio

    @pytest.mark.integration
    @pytest.mark.slow
    def test_dia_producao_alta_escala(self):
        """Dia de produção em alta escala (100 peças)."""
        sistema = inicializar_sistema()

        # 100 peças: 80 aprovadas, 20 reprovadas
        for i in range(80):
            peca = criar_peca(f"PA{i:03d}", 100.0, "azul", 15.0)
            aprovada, _ = validar_peca(peca)
            peca['aprovada'] = aprovada
            adicionar_peca_em_caixa(peca, sistema)

        for i in range(20):
            peca = criar_peca(f"PR{i:03d}", 120.0, "vermelho", 15.0)
            aprovada, motivos = validar_peca(peca)
            peca['aprovada'] = aprovada
            peca['motivos_reprovacao'] = motivos
            sistema['pecas_reprovadas'].append(peca)

        # Verificar
        assert len(sistema['pecas_aprovadas']) == 80
        assert len(sistema['pecas_reprovadas']) == 20

        # 8 caixas fechadas
        assert len(sistema['caixas_fechadas']) == 8

        relatorio = gerar_relatorio_completo(sistema)
        assert "Total de peças processadas: 100" in relatorio


# ========================================
# CENÁRIOS DE CASOS EXTREMOS
# ========================================

class TestCenariosExtremos:
    """Cenários extremos e casos especiais."""

    @pytest.mark.integration
    def test_todas_pecas_reprovadas(self):
        """Cenário onde 100% das peças são reprovadas."""
        sistema = inicializar_sistema()

        for i in range(10):
            peca = criar_peca(f"P{i:03d}", 150.0, "roxo", 30.0)
            aprovada, motivos = validar_peca(peca)
            peca['aprovada'] = aprovada
            peca['motivos_reprovacao'] = motivos
            sistema['pecas_reprovadas'].append(peca)

        assert len(sistema['pecas_aprovadas']) == 0
        assert len(sistema['pecas_reprovadas']) == 10
        assert len(sistema['caixas_fechadas']) == 0

        relatorio = gerar_relatorio_completo(sistema)
        assert "Peças reprovadas: 10 (100.0%)" in relatorio
        assert "DETALHAMENTO DE REPROVAÇÕES" in relatorio

    @pytest.mark.integration
    def test_exatamente_uma_caixa_cheia(self):
        """Cenário de exatamente 10 peças aprovadas (1 caixa completa)."""
        sistema = inicializar_sistema()

        for i in range(10):
            peca = criar_peca(f"P{i:03d}", 100.0, "verde", 15.0)
            aprovada, _ = validar_peca(peca)
            peca['aprovada'] = aprovada
            adicionar_peca_em_caixa(peca, sistema)

        assert len(sistema['caixas_fechadas']) == 1
        assert len(sistema['caixa_atual']['pecas']) == 0

        relatorio = gerar_relatorio_completo(sistema)
        assert "Caixas fechadas: 1" in relatorio
        assert "vazia" in relatorio.lower()

    @pytest.mark.integration
    def test_limite_inferior_criterios(self):
        """Peças exatamente nos limites inferiores dos critérios."""
        sistema = inicializar_sistema()

        # Peso mínimo, comprimento mínimo, cores válidas
        peca = criar_peca("P001", 95.0, "azul", 10.0)
        aprovada, motivos = validar_peca(peca)
        peca['aprovada'] = aprovada

        assert aprovada is True
        adicionar_peca_em_caixa(peca, sistema)

        assert len(sistema['pecas_aprovadas']) == 1

    @pytest.mark.integration
    def test_limite_superior_criterios(self):
        """Peças exatamente nos limites superiores dos critérios."""
        sistema = inicializar_sistema()

        # Peso máximo, comprimento máximo
        peca = criar_peca("P001", 105.0, "verde", 20.0)
        aprovada, motivos = validar_peca(peca)
        peca['aprovada'] = aprovada

        assert aprovada is True
        adicionar_peca_em_caixa(peca, sistema)

        assert len(sistema['pecas_aprovadas']) == 1

    @pytest.mark.integration
    @pytest.mark.edge_case
    def test_logo_apos_limite_inferior(self):
        """Peças logo abaixo dos limites inferiores devem ser reprovadas."""
        sistema = inicializar_sistema()

        peca = criar_peca("P001", 94.9, "azul", 9.9)
        aprovada, motivos = validar_peca(peca)
        peca['aprovada'] = aprovada
        peca['motivos_reprovacao'] = motivos

        assert aprovada is False
        assert len(motivos) == 2  # Peso e comprimento

    @pytest.mark.integration
    @pytest.mark.edge_case
    def test_logo_apos_limite_superior(self):
        """Peças logo acima dos limites superiores devem ser reprovadas."""
        sistema = inicializar_sistema()

        peca = criar_peca("P001", 105.1, "azul", 20.1)
        aprovada, motivos = validar_peca(peca)
        peca['aprovada'] = aprovada
        peca['motivos_reprovacao'] = motivos

        assert aprovada is False
        assert len(motivos) == 2  # Peso e comprimento


# ========================================
# CENÁRIOS DE VARIAÇÃO DE MOTIVOS
# ========================================

class TestCenariosMotivosVariados:
    """Cenários com diferentes combinações de motivos de reprovação."""

    @pytest.mark.integration
    def test_apenas_reprovacoes_por_peso(self):
        """Todas as reprovações causadas apenas por peso."""
        sistema = inicializar_sistema()

        pesos_invalidos = [80.0, 85.0, 90.0, 110.0, 120.0]

        for i, peso in enumerate(pesos_invalidos):
            peca = criar_peca(f"P{i:03d}", peso, "azul", 15.0)
            aprovada, motivos = validar_peca(peca)
            peca['aprovada'] = aprovada
            peca['motivos_reprovacao'] = motivos
            sistema['pecas_reprovadas'].append(peca)

        relatorio = gerar_relatorio_completo(sistema)
        assert "Por peso inadequado: 5 peças" in relatorio
        assert "Por cor inadequada: 0 peças" in relatorio
        assert "Por comprimento inadequado: 0 peças" in relatorio

    @pytest.mark.integration
    def test_apenas_reprovacoes_por_cor(self):
        """Todas as reprovações causadas apenas por cor."""
        sistema = inicializar_sistema()

        cores_invalidas = ["vermelho", "amarelo", "preto", "branco", "roxo"]

        for i, cor in enumerate(cores_invalidas):
            peca = criar_peca(f"P{i:03d}", 100.0, cor, 15.0)
            aprovada, motivos = validar_peca(peca)
            peca['aprovada'] = aprovada
            peca['motivos_reprovacao'] = motivos
            sistema['pecas_reprovadas'].append(peca)

        relatorio = gerar_relatorio_completo(sistema)
        assert "Por peso inadequado: 0 peças" in relatorio
        assert "Por cor inadequada: 5 peças" in relatorio
        assert "Por comprimento inadequado: 0 peças" in relatorio

    @pytest.mark.integration
    def test_apenas_reprovacoes_por_comprimento(self):
        """Todas as reprovações causadas apenas por comprimento."""
        sistema = inicializar_sistema()

        comprimentos_invalidos = [5.0, 8.0, 9.5, 21.0, 25.0]

        for i, comprimento in enumerate(comprimentos_invalidos):
            peca = criar_peca(f"P{i:03d}", 100.0, "verde", comprimento)
            aprovada, motivos = validar_peca(peca)
            peca['aprovada'] = aprovada
            peca['motivos_reprovacao'] = motivos
            sistema['pecas_reprovadas'].append(peca)

        relatorio = gerar_relatorio_completo(sistema)
        assert "Por peso inadequado: 0 peças" in relatorio
        assert "Por cor inadequada: 0 peças" in relatorio
        assert "Por comprimento inadequado: 5 peças" in relatorio

    @pytest.mark.integration
    def test_mix_todos_tipos_reprovacao(self):
        """Mix com todos os tipos de reprovação."""
        sistema = inicializar_sistema()

        # 3 reprovações de cada tipo
        # Peso
        for i in range(3):
            peca = criar_peca(f"PP{i:03d}", 120.0, "azul", 15.0)
            aprovada, motivos = validar_peca(peca)
            peca['aprovada'] = aprovada
            peca['motivos_reprovacao'] = motivos
            sistema['pecas_reprovadas'].append(peca)

        # Cor
        for i in range(3):
            peca = criar_peca(f"PC{i:03d}", 100.0, "vermelho", 15.0)
            aprovada, motivos = validar_peca(peca)
            peca['aprovada'] = aprovada
            peca['motivos_reprovacao'] = motivos
            sistema['pecas_reprovadas'].append(peca)

        # Comprimento
        for i in range(3):
            peca = criar_peca(f"PL{i:03d}", 100.0, "azul", 25.0)
            aprovada, motivos = validar_peca(peca)
            peca['aprovada'] = aprovada
            peca['motivos_reprovacao'] = motivos
            sistema['pecas_reprovadas'].append(peca)

        relatorio = gerar_relatorio_completo(sistema)
        assert "Por peso inadequado: 3 peças" in relatorio
        assert "Por cor inadequada: 3 peças" in relatorio
        assert "Por comprimento inadequado: 3 peças" in relatorio


# ========================================
# CENÁRIOS DE PERFORMANCE
# ========================================

class TestCenariosPerformance:
    """Testes de performance e estresse (marcados como slow)."""

    @pytest.mark.integration
    @pytest.mark.slow
    def test_processar_500_pecas(self):
        """Processar 500 peças (teste de performance)."""
        sistema = inicializar_sistema()

        for i in range(500):
            # 80% aprovadas, 20% reprovadas
            if i % 5 == 0:
                # Reprovada
                peca = criar_peca(f"P{i:04d}", 120.0, "vermelho", 15.0)
            else:
                # Aprovada
                peca = criar_peca(f"P{i:04d}", 100.0, "azul", 15.0)

            aprovada, motivos = validar_peca(peca)
            peca['aprovada'] = aprovada
            peca['motivos_reprovacao'] = motivos

            if aprovada:
                adicionar_peca_em_caixa(peca, sistema)
            else:
                sistema['pecas_reprovadas'].append(peca)

        # Verificar
        assert len(sistema['pecas_aprovadas']) == 400
        assert len(sistema['pecas_reprovadas']) == 100

        # 40 caixas fechadas
        assert len(sistema['caixas_fechadas']) == 40

        relatorio = gerar_relatorio_completo(sistema)
        assert "Total de peças processadas: 500" in relatorio

    @pytest.mark.integration
    @pytest.mark.slow
    def test_multiplas_caixas_sequenciais(self):
        """Testar fechamento sequencial de muitas caixas."""
        sistema = inicializar_sistema()

        # Processar exatamente 50 peças (5 caixas fechadas)
        for i in range(50):
            peca = criar_peca(f"P{i:03d}", 100.0, "verde", 15.0)
            aprovada, _ = validar_peca(peca)
            peca['aprovada'] = aprovada
            adicionar_peca_em_caixa(peca, sistema)

        # Verificar 5 caixas fechadas, caixa atual vazia
        assert len(sistema['caixas_fechadas']) == 5
        assert len(sistema['caixa_atual']['pecas']) == 0
        assert sistema['contador_caixas'] == 6

        # Todas as caixas devem estar corretamente numeradas
        for i, caixa in enumerate(sistema['caixas_fechadas'], 1):
            assert caixa['id'] == i
            assert len(caixa['pecas']) == 10
