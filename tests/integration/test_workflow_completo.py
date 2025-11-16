"""
Testes de integração do workflow completo.

Testa o fluxo end-to-end:
1. Receber dados de peça
2. Validar critérios de qualidade
3. Armazenar em caixas (se aprovada)
4. Fechar caixas automaticamente
5. Gerar relatório consolidado
"""

import pytest
from models.peca import criar_peca
from services.validacao import validar_peca
from services.armazenamento import inicializar_sistema, adicionar_peca_em_caixa
from services.relatorio import gerar_relatorio_completo


# ========================================
# TESTES DE WORKFLOW END-TO-END
# ========================================

class TestWorkflowCompleto:
    """Testes do fluxo completo do sistema."""

    @pytest.mark.integration
    def test_fluxo_peca_aprovada_completo(self):
        """
        Fluxo completo: receber → validar → armazenar → relatorio.
        Caso de sucesso (peça aprovada).
        """
        # 1. Receber dados da peça
        peca = criar_peca("P001", 100.0, "azul", 15.0)

        # 2. Validar qualidade
        aprovada, motivos = validar_peca(peca)
        peca['aprovada'] = aprovada
        peca['motivos_reprovacao'] = motivos

        assert aprovada is True

        # 3. Armazenar em caixa
        sistema = inicializar_sistema()
        caixa_fechada, mensagem = adicionar_peca_em_caixa(peca, sistema)

        assert caixa_fechada is False
        assert peca in sistema['pecas_aprovadas']
        assert peca in sistema['caixa_atual']['pecas']

        # 4. Gerar relatório
        relatorio = gerar_relatorio_completo(sistema)

        assert "Peças aprovadas: 1" in relatorio
        assert "Peças reprovadas: 0" in relatorio

    @pytest.mark.integration
    def test_fluxo_peca_reprovada_completo(self):
        """
        Fluxo completo: receber → validar → rejeitar → relatorio.
        Caso de falha (peça reprovada).
        """
        # 1. Receber dados da peça
        peca = criar_peca("P001", 120.0, "vermelho", 25.0)

        # 2. Validar qualidade
        aprovada, motivos = validar_peca(peca)
        peca['aprovada'] = aprovada
        peca['motivos_reprovacao'] = motivos

        assert aprovada is False
        assert len(motivos) == 3  # Todos os critérios falharam

        # 3. Não armazenar (apenas adicionar à lista de reprovadas)
        sistema = inicializar_sistema()
        sistema['pecas_reprovadas'].append(peca)

        assert peca in sistema['pecas_reprovadas']
        assert peca not in sistema['pecas_aprovadas']

        # 4. Gerar relatório
        relatorio = gerar_relatorio_completo(sistema)

        assert "Peças aprovadas: 0" in relatorio
        assert "Peças reprovadas: 1" in relatorio
        assert "DETALHAMENTO DE REPROVAÇÕES" in relatorio

    @pytest.mark.integration
    def test_processar_10_pecas_fecha_caixa(self):
        """
        Processar exatamente 10 peças aprovadas deve fechar uma caixa.
        """
        sistema = inicializar_sistema()

        for i in range(10):
            # Criar peça
            peca = criar_peca(f"P{i:03d}", 100.0, "azul", 15.0)

            # Validar
            aprovada, motivos = validar_peca(peca)
            peca['aprovada'] = aprovada
            peca['motivos_reprovacao'] = motivos

            assert aprovada is True

            # Armazenar
            caixa_fechada, _ = adicionar_peca_em_caixa(peca, sistema)

            if i < 9:
                assert caixa_fechada is False
            else:
                # 10ª peça deve fechar a caixa
                assert caixa_fechada is True

        # Verificar estado final
        assert len(sistema['caixas_fechadas']) == 1
        assert len(sistema['caixas_fechadas'][0]['pecas']) == 10
        assert sistema['caixas_fechadas'][0]['fechada'] is True

        # Caixa atual deve estar vazia
        assert len(sistema['caixa_atual']['pecas']) == 0
        assert sistema['caixa_atual']['id'] == 2

        # Relatório
        relatorio = gerar_relatorio_completo(sistema)
        assert "Caixas fechadas: 1" in relatorio
        assert "Peças aprovadas: 10" in relatorio

    @pytest.mark.integration
    def test_processar_mix_aprovadas_reprovadas(self):
        """
        Processar mix de peças aprovadas e reprovadas.
        """
        sistema = inicializar_sistema()

        # Criar 15 peças: 10 aprovadas + 5 reprovadas
        dados_pecas = [
            ("P001", 100.0, "azul", 15.0),      # Aprovada
            ("P002", 120.0, "vermelho", 15.0),  # Reprovada (peso, cor)
            ("P003", 98.0, "verde", 18.0),      # Aprovada
            ("P004", 90.0, "azul", 5.0),        # Reprovada (peso, comprimento)
            ("P005", 102.0, "azul", 12.0),      # Aprovada
            ("P006", 100.0, "amarelo", 15.0),   # Reprovada (cor)
            ("P007", 100.0, "azul", 15.0),      # Aprovada
            ("P008", 100.0, "azul", 25.0),      # Reprovada (comprimento)
            ("P009", 95.0, "verde", 10.0),      # Aprovada
            ("P010", 105.0, "azul", 20.0),      # Aprovada
            ("P011", 100.0, "azul", 15.0),      # Aprovada
            ("P012", 150.0, "roxo", 30.0),      # Reprovada (todos)
            ("P013", 100.0, "verde", 15.0),     # Aprovada
            ("P014", 100.0, "azul", 15.0),      # Aprovada
            ("P015", 100.0, "verde", 15.0),     # Aprovada
        ]

        for id_peca, peso, cor, comprimento in dados_pecas:
            # Criar e validar
            peca = criar_peca(id_peca, peso, cor, comprimento)
            aprovada, motivos = validar_peca(peca)
            peca['aprovada'] = aprovada
            peca['motivos_reprovacao'] = motivos

            # Armazenar ou rejeitar
            if aprovada:
                adicionar_peca_em_caixa(peca, sistema)
            else:
                sistema['pecas_reprovadas'].append(peca)

        # Verificar contagens
        assert len(sistema['pecas_aprovadas']) == 10
        assert len(sistema['pecas_reprovadas']) == 5

        # Verificar caixa fechada
        assert len(sistema['caixas_fechadas']) == 1

        # Relatório
        relatorio = gerar_relatorio_completo(sistema)
        assert "Total de peças processadas: 15" in relatorio
        assert "Peças aprovadas: 10" in relatorio
        assert "Peças reprovadas: 5" in relatorio

    @pytest.mark.integration
    def test_processar_25_pecas_cria_multiplas_caixas(self):
        """
        Processar 25 peças aprovadas deve criar 2 caixas fechadas + 1 parcial.
        """
        sistema = inicializar_sistema()

        for i in range(25):
            peca = criar_peca(f"P{i:03d}", 100.0, "azul" if i % 2 == 0 else "verde", 15.0)
            aprovada, motivos = validar_peca(peca)
            peca['aprovada'] = aprovada

            assert aprovada is True
            adicionar_peca_em_caixa(peca, sistema)

        # Verificar: 2 caixas fechadas + 5 na atual
        assert len(sistema['caixas_fechadas']) == 2
        assert len(sistema['caixa_atual']['pecas']) == 5
        assert sistema['caixa_atual']['id'] == 3

        # Relatório
        relatorio = gerar_relatorio_completo(sistema)
        assert "Caixas fechadas: 2" in relatorio
        assert "5/10 peças" in relatorio

    @pytest.mark.integration
    def test_workflow_com_remocao_de_peca(self):
        """
        Workflow incluindo remoção de peça do sistema.
        """
        from services.armazenamento import remover_peca_por_id

        sistema = inicializar_sistema()

        # Adicionar 5 peças
        for i in range(5):
            peca = criar_peca(f"P{i:03d}", 100.0, "azul", 15.0)
            aprovada, _ = validar_peca(peca)
            peca['aprovada'] = aprovada
            adicionar_peca_em_caixa(peca, sistema)

        assert len(sistema['pecas_aprovadas']) == 5

        # Remover uma peça
        sucesso, _ = remover_peca_por_id("P002", sistema)
        assert sucesso is True

        # Verificar remoção
        assert len(sistema['pecas_aprovadas']) == 4
        assert not any(p['id'] == "P002" for p in sistema['pecas_aprovadas'])

        # Relatório
        relatorio = gerar_relatorio_completo(sistema)
        assert "Peças aprovadas: 4" in relatorio


# ========================================
# TESTES DE VALIDAÇÃO E ARMAZENAMENTO INTEGRADOS
# ========================================

class TestValidacaoArmazenamento:
    """Testes da integração entre validação e armazenamento."""

    @pytest.mark.integration
    def test_apenas_pecas_aprovadas_vao_para_caixa(self):
        """Apenas peças aprovadas devem ir para caixas."""
        sistema = inicializar_sistema()

        # 3 aprovadas
        for i in range(3):
            peca = criar_peca(f"PA{i}", 100.0, "azul", 15.0)
            aprovada, _ = validar_peca(peca)
            peca['aprovada'] = aprovada
            if aprovada:
                adicionar_peca_em_caixa(peca, sistema)

        # 2 reprovadas
        for i in range(2):
            peca = criar_peca(f"PR{i}", 120.0, "vermelho", 15.0)
            aprovada, motivos = validar_peca(peca)
            peca['aprovada'] = aprovada
            peca['motivos_reprovacao'] = motivos
            if not aprovada:
                sistema['pecas_reprovadas'].append(peca)

        assert len(sistema['caixa_atual']['pecas']) == 3
        assert len(sistema['pecas_reprovadas']) == 2

    @pytest.mark.integration
    def test_validacao_preserva_dados_originais(self):
        """Validação não deve alterar os dados da peça."""
        peca = criar_peca("P001", 100.0, "azul", 15.0)

        id_original = peca['id']
        peso_original = peca['peso']

        validar_peca(peca)

        assert peca['id'] == id_original
        assert peca['peso'] == peso_original

    @pytest.mark.integration
    def test_criterios_validacao_aplicados_corretamente(self):
        """Todos os critérios de validação devem ser aplicados."""
        # Peça com peso e cor válidos, comprimento inválido
        peca = criar_peca("P001", 100.0, "azul", 25.0)
        aprovada, motivos = validar_peca(peca)

        assert aprovada is False
        assert len(motivos) == 1
        assert "Comprimento" in motivos[0]


# ========================================
# TESTES DE RELATÓRIOS INTEGRADOS
# ========================================

class TestRelatoriosIntegrados:
    """Testes de relatórios com dados integrados."""

    @pytest.mark.integration
    def test_relatorio_reflete_estado_atual(self):
        """Relatório deve refletir o estado atual do sistema."""
        sistema = inicializar_sistema()

        # Processar 7 peças
        for i in range(7):
            peca = criar_peca(f"P{i:03d}", 100.0, "azul", 15.0)
            aprovada, _ = validar_peca(peca)
            peca['aprovada'] = aprovada
            adicionar_peca_em_caixa(peca, sistema)

        relatorio = gerar_relatorio_completo(sistema)

        assert "Peças aprovadas: 7" in relatorio
        assert "7/10 peças" in relatorio
        assert "Caixas fechadas: 0" in relatorio

    @pytest.mark.integration
    def test_relatorio_com_multiplas_caixas(self):
        """Relatório com múltiplas caixas fechadas."""
        sistema = inicializar_sistema()

        # 23 peças (2 caixas fechadas + 3 na atual)
        for i in range(23):
            peca = criar_peca(f"P{i:03d}", 100.0, "verde", 15.0)
            aprovada, _ = validar_peca(peca)
            peca['aprovada'] = aprovada
            adicionar_peca_em_caixa(peca, sistema)

        relatorio = gerar_relatorio_completo(sistema)

        assert "Caixas fechadas: 2" in relatorio
        assert "3/10 peças" in relatorio

    @pytest.mark.integration
    def test_percentuais_calculados_corretamente(self):
        """Percentuais no relatório devem estar corretos."""
        sistema = inicializar_sistema()

        # 6 aprovadas
        for i in range(6):
            peca = criar_peca(f"PA{i}", 100.0, "azul", 15.0)
            aprovada, _ = validar_peca(peca)
            peca['aprovada'] = aprovada
            adicionar_peca_em_caixa(peca, sistema)

        # 4 reprovadas
        for i in range(4):
            peca = criar_peca(f"PR{i}", 120.0, "vermelho", 15.0)
            aprovada, motivos = validar_peca(peca)
            peca['aprovada'] = aprovada
            peca['motivos_reprovacao'] = motivos
            sistema['pecas_reprovadas'].append(peca)

        relatorio = gerar_relatorio_completo(sistema)

        # 6/10 = 60%, 4/10 = 40%
        assert "60.0%" in relatorio
        assert "40.0%" in relatorio


# ========================================
# TESTES DE CONSISTÊNCIA DO SISTEMA
# ========================================

class TestConsistenciaSistema:
    """Testes de consistência do estado do sistema durante operações."""

    @pytest.mark.integration
    def test_ids_unicos_em_pecas_aprovadas(self):
        """IDs de peças aprovadas devem ser únicos."""
        sistema = inicializar_sistema()

        for i in range(10):
            peca = criar_peca(f"P{i:03d}", 100.0, "azul", 15.0)
            aprovada, _ = validar_peca(peca)
            peca['aprovada'] = aprovada
            adicionar_peca_em_caixa(peca, sistema)

        ids = [p['id'] for p in sistema['pecas_aprovadas']]
        assert len(ids) == len(set(ids))  # Sem duplicatas

    @pytest.mark.integration
    def test_total_pecas_consistente(self):
        """Total de peças deve ser consistente em todo o sistema."""
        sistema = inicializar_sistema()

        # Processar 15 peças
        for i in range(15):
            peca = criar_peca(f"P{i:03d}", 100.0, "azul", 15.0)
            aprovada, _ = validar_peca(peca)
            peca['aprovada'] = aprovada
            adicionar_peca_em_caixa(peca, sistema)

        # Total em caixas fechadas + caixa atual = total aprovadas
        total_em_caixas = sum(len(c['pecas']) for c in sistema['caixas_fechadas'])
        total_em_caixa_atual = len(sistema['caixa_atual']['pecas'])

        assert total_em_caixas + total_em_caixa_atual == len(sistema['pecas_aprovadas'])

    @pytest.mark.integration
    def test_caixas_fechadas_tem_capacidade_maxima(self):
        """Todas as caixas fechadas devem ter exatamente 10 peças."""
        sistema = inicializar_sistema()

        # Processar 22 peças (2 caixas fechadas)
        for i in range(22):
            peca = criar_peca(f"P{i:03d}", 100.0, "verde", 15.0)
            aprovada, _ = validar_peca(peca)
            peca['aprovada'] = aprovada
            adicionar_peca_em_caixa(peca, sistema)

        for caixa in sistema['caixas_fechadas']:
            assert len(caixa['pecas']) == 10
            assert caixa['fechada'] is True
