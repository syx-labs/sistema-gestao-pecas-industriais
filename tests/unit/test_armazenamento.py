"""
Testes unitários para o módulo de armazenamento de peças.

Testa:
- Inicialização do sistema
- Adição de peças em caixas
- Fechamento automático de caixas ao atingir capacidade máxima (10 peças)
- Criação de nova caixa após fechamento
- Remoção de peças por ID
"""

import pytest
from models.peca import criar_peca
from models.caixa import CAPACIDADE_MAXIMA_CAIXA
from services.armazenamento import (
    inicializar_sistema,
    adicionar_peca_em_caixa,
    remover_peca_por_id
)


# ========================================
# TESTES DE INICIALIZAÇÃO DO SISTEMA
# ========================================

class TestInicializarSistema:
    """Testes para a função inicializar_sistema()."""

    @pytest.mark.unit
    def test_sistema_inicia_com_listas_vazias(self):
        """Sistema deve iniciar com listas vazias de peças."""
        sistema = inicializar_sistema()

        assert len(sistema['pecas_aprovadas']) == 0
        assert len(sistema['pecas_reprovadas']) == 0
        assert len(sistema['caixas_fechadas']) == 0

    @pytest.mark.unit
    def test_sistema_inicia_com_caixa_atual(self):
        """Sistema deve iniciar com uma caixa atual vazia."""
        sistema = inicializar_sistema()

        assert sistema['caixa_atual'] is not None
        assert sistema['caixa_atual']['id'] == 1
        assert len(sistema['caixa_atual']['pecas']) == 0
        assert sistema['caixa_atual']['fechada'] is False

    @pytest.mark.unit
    def test_sistema_inicia_contador_em_1(self):
        """Sistema deve iniciar com contador de caixas em 1."""
        sistema = inicializar_sistema()

        assert sistema['contador_caixas'] == 1

    @pytest.mark.unit
    def test_inicializacao_multipla_cria_sistemas_independentes(self):
        """Múltiplas inicializações devem criar sistemas independentes."""
        sistema1 = inicializar_sistema()
        sistema2 = inicializar_sistema()

        # Modificar sistema1 não deve afetar sistema2
        peca = criar_peca("P001", 100.0, "azul", 15.0, True)
        sistema1['pecas_aprovadas'].append(peca)

        assert len(sistema1['pecas_aprovadas']) == 1
        assert len(sistema2['pecas_aprovadas']) == 0


# ========================================
# TESTES DE ADIÇÃO DE PEÇAS EM CAIXAS
# ========================================

class TestAdicionarPecaEmCaixa:
    """Testes para a função adicionar_peca_em_caixa()."""

    @pytest.mark.unit
    def test_adicionar_peca_aprovada_em_caixa_vazia(self, sistema_vazio):
        """Adicionar primeira peça aprovada em caixa vazia."""
        peca = criar_peca("P001", 100.0, "azul", 15.0, True)

        caixa_fechada, mensagem = adicionar_peca_em_caixa(peca, sistema_vazio)

        assert caixa_fechada is False
        assert peca in sistema_vazio['caixa_atual']['pecas']
        assert peca in sistema_vazio['pecas_aprovadas']
        assert len(sistema_vazio['caixa_atual']['pecas']) == 1
        assert "1/10" in mensagem

    @pytest.mark.unit
    def test_nao_adicionar_peca_reprovada(self, sistema_vazio):
        """Peças reprovadas não devem ser adicionadas em caixas."""
        peca = criar_peca("P001", 120.0, "vermelho", 15.0, False, ["Peso inválido"])

        caixa_fechada, mensagem = adicionar_peca_em_caixa(peca, sistema_vazio)

        assert caixa_fechada is False
        assert peca not in sistema_vazio['caixa_atual']['pecas']
        assert "Apenas peças aprovadas" in mensagem

    @pytest.mark.unit
    def test_adicionar_multiplas_pecas_sem_fechar_caixa(self, sistema_vazio):
        """Adicionar várias peças sem atingir capacidade máxima."""
        for i in range(5):
            peca = criar_peca(f"P{i:03d}", 100.0, "azul", 15.0, True)
            caixa_fechada, _ = adicionar_peca_em_caixa(peca, sistema_vazio)
            assert caixa_fechada is False

        assert len(sistema_vazio['caixa_atual']['pecas']) == 5
        assert len(sistema_vazio['pecas_aprovadas']) == 5
        assert len(sistema_vazio['caixas_fechadas']) == 0

    @pytest.mark.unit
    def test_adicionar_9_pecas_nao_fecha_caixa(self, sistema_vazio):
        """Adicionar 9 peças não deve fechar a caixa."""
        for i in range(9):
            peca = criar_peca(f"P{i:03d}", 100.0, "azul", 15.0, True)
            caixa_fechada, mensagem = adicionar_peca_em_caixa(peca, sistema_vazio)

        assert caixa_fechada is False
        assert len(sistema_vazio['caixa_atual']['pecas']) == 9
        assert sistema_vazio['caixa_atual']['fechada'] is False
        assert "9/10" in mensagem

    @pytest.mark.unit
    def test_adicionar_10a_peca_fecha_caixa(self, sistema_com_caixa_quase_cheia):
        """Adicionar 10ª peça deve fechar a caixa e criar uma nova."""
        sistema = sistema_com_caixa_quase_cheia
        caixa_anterior_id = sistema['caixa_atual']['id']

        peca = criar_peca("P999", 100.0, "azul", 15.0, True)
        caixa_fechada, mensagem = adicionar_peca_em_caixa(peca, sistema)

        assert caixa_fechada is True
        assert "FECHADA" in mensagem
        assert len(sistema['caixas_fechadas']) == 1
        assert sistema['caixas_fechadas'][0]['fechada'] is True
        assert len(sistema['caixas_fechadas'][0]['pecas']) == 10

    @pytest.mark.unit
    def test_nova_caixa_criada_apos_fechamento(self, sistema_com_caixa_quase_cheia):
        """Nova caixa deve ser criada automaticamente após fechamento."""
        sistema = sistema_com_caixa_quase_cheia

        peca = criar_peca("P999", 100.0, "azul", 15.0, True)
        adicionar_peca_em_caixa(peca, sistema)

        assert sistema['caixa_atual']['id'] == 2
        assert len(sistema['caixa_atual']['pecas']) == 0
        assert sistema['caixa_atual']['fechada'] is False
        assert sistema['contador_caixas'] == 2

    @pytest.mark.unit
    def test_contador_incrementa_apos_fechar_caixa(self, sistema_com_caixa_quase_cheia):
        """Contador de caixas deve incrementar ao fechar caixa."""
        sistema = sistema_com_caixa_quase_cheia
        contador_antes = sistema['contador_caixas']

        peca = criar_peca("P999", 100.0, "azul", 15.0, True)
        adicionar_peca_em_caixa(peca, sistema)

        assert sistema['contador_caixas'] == contador_antes + 1

    @pytest.mark.unit
    def test_11a_peca_vai_para_nova_caixa(self, sistema_com_caixa_quase_cheia):
        """11ª peça deve ir para a nova caixa criada."""
        sistema = sistema_com_caixa_quase_cheia

        # 10ª peça - fecha caixa
        peca10 = criar_peca("P010", 100.0, "azul", 15.0, True)
        adicionar_peca_em_caixa(peca10, sistema)

        # 11ª peça - vai para nova caixa
        peca11 = criar_peca("P011", 100.0, "verde", 15.0, True)
        caixa_fechada, mensagem = adicionar_peca_em_caixa(peca11, sistema)

        assert caixa_fechada is False
        assert len(sistema['caixa_atual']['pecas']) == 1
        assert sistema['caixa_atual']['pecas'][0] == peca11
        assert peca11 not in sistema['caixas_fechadas'][0]['pecas']

    @pytest.mark.unit
    def test_multiplas_caixas_fechadas(self, sistema_vazio):
        """Sistema deve permitir múltiplas caixas fechadas."""
        # Adicionar 25 peças (2 caixas cheias + 5 na atual)
        for i in range(25):
            peca = criar_peca(f"P{i:03d}", 100.0, "azul", 15.0, True)
            adicionar_peca_em_caixa(peca, sistema_vazio)

        assert len(sistema_vazio['caixas_fechadas']) == 2
        assert len(sistema_vazio['caixa_atual']['pecas']) == 5
        assert sistema_vazio['contador_caixas'] == 3

    @pytest.mark.unit
    def test_todas_pecas_aprovadas_estao_na_lista(self, sistema_vazio):
        """Todas as peças aprovadas devem estar na lista de aprovadas."""
        for i in range(15):
            peca = criar_peca(f"P{i:03d}", 100.0, "azul", 15.0, True)
            adicionar_peca_em_caixa(peca, sistema_vazio)

        assert len(sistema_vazio['pecas_aprovadas']) == 15

    @pytest.mark.unit
    @pytest.mark.edge_case
    def test_capacidade_maxima_correta(self):
        """Verificar que a capacidade máxima da caixa é 10."""
        assert CAPACIDADE_MAXIMA_CAIXA == 10


# ========================================
# TESTES DE REMOÇÃO DE PEÇAS
# ========================================

class TestRemoverPeca:
    """Testes para a função remover_peca_por_id()."""

    @pytest.mark.unit
    def test_remover_peca_aprovada_da_caixa_atual(self, sistema_com_pecas_aprovadas):
        """Remover peça aprovada que está na caixa atual."""
        sistema = sistema_com_pecas_aprovadas
        id_para_remover = sistema['pecas_aprovadas'][0]['id']

        sucesso, mensagem = remover_peca_por_id(id_para_remover, sistema)

        assert sucesso is True
        assert "removida" in mensagem
        assert not any(p['id'] == id_para_remover for p in sistema['pecas_aprovadas'])
        assert not any(p['id'] == id_para_remover for p in sistema['caixa_atual']['pecas'])

    @pytest.mark.unit
    def test_remover_peca_reprovada(self, sistema_com_pecas_reprovadas):
        """Remover peça reprovada da lista."""
        sistema = sistema_com_pecas_reprovadas
        id_para_remover = sistema['pecas_reprovadas'][0]['id']

        sucesso, mensagem = remover_peca_por_id(id_para_remover, sistema)

        assert sucesso is True
        assert "removida" in mensagem
        assert not any(p['id'] == id_para_remover for p in sistema['pecas_reprovadas'])

    @pytest.mark.unit
    def test_remover_peca_inexistente(self, sistema_vazio):
        """Tentar remover peça que não existe deve falhar."""
        sucesso, mensagem = remover_peca_por_id("ID_INEXISTENTE", sistema_vazio)

        assert sucesso is False
        assert "não encontrada" in mensagem

    @pytest.mark.unit
    def test_remover_peca_de_sistema_vazio(self, sistema_vazio):
        """Remover de sistema vazio deve falhar graciosamente."""
        sucesso, mensagem = remover_peca_por_id("P001", sistema_vazio)

        assert sucesso is False

    @pytest.mark.unit
    def test_remover_peca_de_caixa_fechada(self, sistema_com_multiplas_caixas):
        """Remover peça que está em caixa fechada."""
        sistema = sistema_com_multiplas_caixas
        # Pegar ID de uma peça na primeira caixa fechada
        id_para_remover = sistema['caixas_fechadas'][0]['pecas'][0]['id']

        sucesso, mensagem = remover_peca_por_id(id_para_remover, sistema)

        assert sucesso is True
        assert not any(
            p['id'] == id_para_remover
            for caixa in sistema['caixas_fechadas']
            for p in caixa['pecas']
        )

    @pytest.mark.unit
    def test_remover_atualiza_contagem_de_pecas(self, sistema_com_pecas_aprovadas):
        """Remover peça deve atualizar as contagens corretamente."""
        sistema = sistema_com_pecas_aprovadas
        total_antes = len(sistema['pecas_aprovadas'])
        id_para_remover = sistema['pecas_aprovadas'][0]['id']

        remover_peca_por_id(id_para_remover, sistema)

        assert len(sistema['pecas_aprovadas']) == total_antes - 1

    @pytest.mark.unit
    def test_remover_peca_especifica_nao_afeta_outras(self, sistema_com_pecas_aprovadas):
        """Remover uma peça não deve afetar outras peças."""
        sistema = sistema_com_pecas_aprovadas
        ids_originais = {p['id'] for p in sistema['pecas_aprovadas']}
        id_para_remover = list(ids_originais)[0]
        ids_restantes = ids_originais - {id_para_remover}

        remover_peca_por_id(id_para_remover, sistema)

        ids_atuais = {p['id'] for p in sistema['pecas_aprovadas']}
        assert ids_atuais == ids_restantes

    @pytest.mark.unit
    def test_remover_todas_pecas_uma_por_uma(self, sistema_com_pecas_aprovadas):
        """Remover todas as peças uma por uma."""
        sistema = sistema_com_pecas_aprovadas
        ids = [p['id'] for p in sistema['pecas_aprovadas'].copy()]

        for id_peca in ids:
            sucesso, _ = remover_peca_por_id(id_peca, sistema)
            assert sucesso is True

        assert len(sistema['pecas_aprovadas']) == 0
        assert len(sistema['caixa_atual']['pecas']) == 0

    @pytest.mark.unit
    @pytest.mark.edge_case
    def test_remover_com_id_vazio(self, sistema_com_pecas_aprovadas):
        """Tentar remover com ID vazio."""
        sucesso, mensagem = remover_peca_por_id("", sistema_com_pecas_aprovadas)

        assert sucesso is False

    @pytest.mark.unit
    def test_mensagem_indica_tipo_de_peca_removida(self, sistema_com_pecas_aprovadas):
        """Mensagem de sucesso deve indicar se era aprovada ou reprovada."""
        sistema = sistema_com_pecas_aprovadas
        id_aprovada = sistema['pecas_aprovadas'][0]['id']

        sucesso, mensagem = remover_peca_por_id(id_aprovada, sistema)

        assert sucesso is True
        assert mensagem != ""
        assert "removida" in mensagem.lower()

    @pytest.mark.unit
    @pytest.mark.edge_case
    def test_remover_peca_aprovada_nao_em_caixa(self, sistema_vazio):
        """Remover peça que está em aprovadas mas não em nenhuma caixa (inconsistência)."""
        # Criar cenário de inconsistência: peça na lista mas não em caixa
        peca = criar_peca("P999", 100.0, "azul", 15.0, aprovada=True)
        sistema_vazio['pecas_aprovadas'].append(peca)
        # NÃO adicionar em caixa_atual

        sucesso, mensagem = remover_peca_por_id("P999", sistema_vazio)

        assert sucesso is True
        assert "aprovada" in mensagem.lower()
        assert "P999" in mensagem
        assert len(sistema_vazio['pecas_aprovadas']) == 0


# ========================================
# TESTES DE CONSISTÊNCIA DE ESTADO
# ========================================

class TestConsistenciaEstado:
    """Testes para garantir consistência do estado do sistema."""

    @pytest.mark.unit
    def test_pecas_na_caixa_atual_estao_em_aprovadas(self, sistema_com_pecas_aprovadas):
        """Todas as peças na caixa atual devem estar na lista de aprovadas."""
        sistema = sistema_com_pecas_aprovadas

        ids_caixa = {p['id'] for p in sistema['caixa_atual']['pecas']}
        ids_aprovadas = {p['id'] for p in sistema['pecas_aprovadas']}

        assert ids_caixa.issubset(ids_aprovadas)

    @pytest.mark.unit
    def test_pecas_em_caixas_fechadas_estao_em_aprovadas(self, sistema_com_multiplas_caixas):
        """Todas as peças em caixas fechadas devem estar na lista de aprovadas."""
        sistema = sistema_com_multiplas_caixas

        ids_caixas_fechadas = {
            p['id']
            for caixa in sistema['caixas_fechadas']
            for p in caixa['pecas']
        }
        ids_aprovadas = {p['id'] for p in sistema['pecas_aprovadas']}

        assert ids_caixas_fechadas.issubset(ids_aprovadas)

    @pytest.mark.unit
    def test_caixas_fechadas_tem_exatamente_10_pecas(self, sistema_com_multiplas_caixas):
        """Todas as caixas fechadas devem ter exatamente 10 peças."""
        sistema = sistema_com_multiplas_caixas

        for caixa in sistema['caixas_fechadas']:
            assert len(caixa['pecas']) == 10
            assert caixa['fechada'] is True

    @pytest.mark.unit
    def test_caixa_atual_tem_menos_de_10_pecas(self, sistema_com_pecas_aprovadas):
        """Caixa atual deve ter menos de 10 peças (não fechada)."""
        sistema = sistema_com_pecas_aprovadas

        assert len(sistema['caixa_atual']['pecas']) < 10
        assert sistema['caixa_atual']['fechada'] is False

    @pytest.mark.unit
    def test_contador_caixas_maior_ou_igual_id_caixa_atual(self, sistema_com_multiplas_caixas):
        """Contador de caixas deve ser >= ID da caixa atual."""
        sistema = sistema_com_multiplas_caixas

        assert sistema['contador_caixas'] >= sistema['caixa_atual']['id']

    @pytest.mark.unit
    def test_nao_ha_duplicatas_em_pecas_aprovadas(self, sistema_com_multiplas_caixas):
        """Não deve haver IDs duplicados na lista de peças aprovadas."""
        sistema = sistema_com_multiplas_caixas

        ids = [p['id'] for p in sistema['pecas_aprovadas']]
        assert len(ids) == len(set(ids))

    @pytest.mark.unit
    def test_nao_ha_duplicatas_em_pecas_reprovadas(self, sistema_com_pecas_reprovadas):
        """Não deve haver IDs duplicados na lista de peças reprovadas."""
        sistema = sistema_com_pecas_reprovadas

        ids = [p['id'] for p in sistema['pecas_reprovadas']]
        assert len(ids) == len(set(ids))
