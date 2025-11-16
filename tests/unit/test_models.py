"""
Testes unitários para os modelos de dados.

Testa:
- Criação de Peça via factory function
- Criação de Caixa via factory function
- Estrutura TypedDict correta
- Valores padrão
"""

import pytest
from models.peca import criar_peca, Peca
from models.caixa import criar_caixa, Caixa, CAPACIDADE_MAXIMA_CAIXA


# ========================================
# TESTES DO MODELO PECA
# ========================================

class TestCriarPeca:
    """Testes para a factory function criar_peca()."""

    @pytest.mark.unit
    def test_criar_peca_com_parametros_minimos(self):
        """Criar peça com apenas parâmetros obrigatórios."""
        peca = criar_peca(
            id_peca="P001",
            peso=100.0,
            cor="azul",
            comprimento=15.0
        )

        assert peca['id'] == "P001"
        assert peca['peso'] == 100.0
        assert peca['cor'] == "azul"
        assert peca['comprimento'] == 15.0
        assert peca['aprovada'] is False  # Valor padrão
        assert peca['motivos_reprovacao'] == []  # Valor padrão

    @pytest.mark.unit
    def test_criar_peca_com_todos_parametros(self):
        """Criar peça com todos os parâmetros explícitos."""
        peca = criar_peca(
            id_peca="P002",
            peso=98.5,
            cor="verde",
            comprimento=12.0,
            aprovada=True,
            motivos_reprovacao=[]
        )

        assert peca['id'] == "P002"
        assert peca['peso'] == 98.5
        assert peca['cor'] == "verde"
        assert peca['comprimento'] == 12.0
        assert peca['aprovada'] is True
        assert peca['motivos_reprovacao'] == []

    @pytest.mark.unit
    def test_criar_peca_reprovada_com_motivos(self):
        """Criar peça reprovada com lista de motivos."""
        motivos = ["Peso fora do intervalo", "Cor inadequada"]
        peca = criar_peca(
            id_peca="P003",
            peso=120.0,
            cor="vermelho",
            comprimento=15.0,
            aprovada=False,
            motivos_reprovacao=motivos
        )

        assert peca['aprovada'] is False
        assert peca['motivos_reprovacao'] == motivos
        assert len(peca['motivos_reprovacao']) == 2

    @pytest.mark.unit
    def test_peca_retorna_typed_dict(self):
        """Peça criada deve ser uma TypedDict."""
        peca = criar_peca("P001", 100.0, "azul", 15.0)

        # TypedDict se comporta como dict
        assert isinstance(peca, dict)
        assert 'id' in peca
        assert 'peso' in peca
        assert 'cor' in peca
        assert 'comprimento' in peca
        assert 'aprovada' in peca
        assert 'motivos_reprovacao' in peca

    @pytest.mark.unit
    def test_peca_tem_todas_chaves_obrigatorias(self):
        """Peça deve ter todas as chaves obrigatórias."""
        peca = criar_peca("P001", 100.0, "azul", 15.0)

        chaves_obrigatorias = {'id', 'peso', 'cor', 'comprimento', 'aprovada', 'motivos_reprovacao'}
        assert set(peca.keys()) == chaves_obrigatorias

    @pytest.mark.unit
    def test_valores_defaults_corretos(self):
        """Valores default devem estar corretos."""
        peca = criar_peca("P001", 100.0, "azul", 15.0)

        assert peca['aprovada'] is False
        assert isinstance(peca['motivos_reprovacao'], list)
        assert len(peca['motivos_reprovacao']) == 0

    @pytest.mark.unit
    def test_motivos_none_vira_lista_vazia(self):
        """motivos_reprovacao=None deve virar lista vazia."""
        peca = criar_peca("P001", 100.0, "azul", 15.0, motivos_reprovacao=None)

        assert peca['motivos_reprovacao'] == []

    @pytest.mark.unit
    def test_criar_multiplas_pecas_independentes(self):
        """Múltiplas peças criadas devem ser independentes."""
        peca1 = criar_peca("P001", 100.0, "azul", 15.0)
        peca2 = criar_peca("P002", 102.0, "verde", 17.0)

        # Modificar peca1 não deve afetar peca2
        peca1['aprovada'] = True

        assert peca1['aprovada'] is True
        assert peca2['aprovada'] is False

    @pytest.mark.unit
    @pytest.mark.parametrize("id_peca,peso,cor,comprimento", [
        ("P001", 100.0, "azul", 15.0),
        ("PECA_001", 95.0, "verde", 10.0),
        ("ABC123", 105.0, "AZUL", 20.0),
        ("", 100.0, "azul", 15.0),  # ID vazio (válido na criação)
    ])
    def test_criar_peca_diversos_valores(self, id_peca, peso, cor, comprimento):
        """Criar peças com diversos valores válidos."""
        peca = criar_peca(id_peca, peso, cor, comprimento)

        assert peca['id'] == id_peca
        assert peca['peso'] == peso
        assert peca['cor'] == cor
        assert peca['comprimento'] == comprimento


# ========================================
# TESTES DO MODELO CAIXA
# ========================================

class TestCriarCaixa:
    """Testes para a factory function criar_caixa()."""

    @pytest.mark.unit
    def test_criar_caixa_com_id(self):
        """Criar caixa com ID fornecido."""
        caixa = criar_caixa(id_caixa=1)

        assert caixa['id'] == 1
        assert caixa['pecas'] == []
        assert caixa['fechada'] is False

    @pytest.mark.unit
    def test_caixa_inicia_vazia(self):
        """Caixa criada deve iniciar com lista de peças vazia."""
        caixa = criar_caixa(id_caixa=1)

        assert len(caixa['pecas']) == 0
        assert isinstance(caixa['pecas'], list)

    @pytest.mark.unit
    def test_caixa_inicia_aberta(self):
        """Caixa criada deve iniciar com status fechada=False."""
        caixa = criar_caixa(id_caixa=1)

        assert caixa['fechada'] is False

    @pytest.mark.unit
    def test_caixa_retorna_typed_dict(self):
        """Caixa criada deve ser uma TypedDict."""
        caixa = criar_caixa(id_caixa=1)

        assert isinstance(caixa, dict)
        assert 'id' in caixa
        assert 'pecas' in caixa
        assert 'fechada' in caixa

    @pytest.mark.unit
    def test_caixa_tem_todas_chaves_obrigatorias(self):
        """Caixa deve ter todas as chaves obrigatórias."""
        caixa = criar_caixa(id_caixa=1)

        chaves_obrigatorias = {'id', 'pecas', 'fechada'}
        assert set(caixa.keys()) == chaves_obrigatorias

    @pytest.mark.unit
    @pytest.mark.parametrize("id_caixa", [1, 2, 10, 100, 999])
    def test_criar_caixas_com_ids_diferentes(self, id_caixa):
        """Criar caixas com IDs diferentes."""
        caixa = criar_caixa(id_caixa=id_caixa)

        assert caixa['id'] == id_caixa

    @pytest.mark.unit
    def test_criar_multiplas_caixas_independentes(self):
        """Múltiplas caixas criadas devem ser independentes."""
        caixa1 = criar_caixa(id_caixa=1)
        caixa2 = criar_caixa(id_caixa=2)

        # Modificar caixa1 não deve afetar caixa2
        peca = criar_peca("P001", 100.0, "azul", 15.0)
        caixa1['pecas'].append(peca)

        assert len(caixa1['pecas']) == 1
        assert len(caixa2['pecas']) == 0

    @pytest.mark.unit
    def test_caixa_pode_ser_modificada(self):
        """Caixa criada pode ter seus atributos modificados."""
        caixa = criar_caixa(id_caixa=1)

        # Adicionar peça
        peca = criar_peca("P001", 100.0, "azul", 15.0)
        caixa['pecas'].append(peca)

        assert len(caixa['pecas']) == 1

        # Fechar caixa
        caixa['fechada'] = True

        assert caixa['fechada'] is True

    @pytest.mark.unit
    def test_capacidade_maxima_caixa_definida(self):
        """Constante CAPACIDADE_MAXIMA_CAIXA deve estar definida."""
        assert CAPACIDADE_MAXIMA_CAIXA == 10

    @pytest.mark.unit
    def test_caixa_pode_ter_10_pecas(self):
        """Caixa deve poder armazenar até 10 peças."""
        caixa = criar_caixa(id_caixa=1)

        for i in range(10):
            peca = criar_peca(f"P{i:03d}", 100.0, "azul", 15.0)
            caixa['pecas'].append(peca)

        assert len(caixa['pecas']) == 10


# ========================================
# TESTES DE INTEGRAÇÃO ENTRE MODELOS
# ========================================

class TestIntegracaoModelos:
    """Testes de integração entre Peca e Caixa."""

    @pytest.mark.unit
    def test_adicionar_peca_em_caixa(self):
        """Peça criada pode ser adicionada em caixa."""
        peca = criar_peca("P001", 100.0, "azul", 15.0, aprovada=True)
        caixa = criar_caixa(id_caixa=1)

        caixa['pecas'].append(peca)

        assert len(caixa['pecas']) == 1
        assert caixa['pecas'][0] == peca

    @pytest.mark.unit
    def test_adicionar_multiplas_pecas_em_caixa(self):
        """Múltiplas peças podem ser adicionadas na mesma caixa."""
        caixa = criar_caixa(id_caixa=1)

        for i in range(5):
            peca = criar_peca(f"P{i:03d}", 100.0, "azul", 15.0, aprovada=True)
            caixa['pecas'].append(peca)

        assert len(caixa['pecas']) == 5

    @pytest.mark.unit
    def test_peca_pode_estar_em_uma_caixa(self):
        """Uma peça pode estar em uma caixa."""
        peca = criar_peca("P001", 100.0, "azul", 15.0, aprovada=True)
        caixa = criar_caixa(id_caixa=1)

        caixa['pecas'].append(peca)

        assert peca in caixa['pecas']

    @pytest.mark.unit
    def test_dados_peca_preservados_na_caixa(self):
        """Dados da peça devem ser preservados ao adicionar na caixa."""
        peca = criar_peca("P001", 100.0, "azul", 15.0, aprovada=True)
        caixa = criar_caixa(id_caixa=1)

        caixa['pecas'].append(peca)
        peca_na_caixa = caixa['pecas'][0]

        assert peca_na_caixa['id'] == "P001"
        assert peca_na_caixa['peso'] == 100.0
        assert peca_na_caixa['cor'] == "azul"
        assert peca_na_caixa['comprimento'] == 15.0
        assert peca_na_caixa['aprovada'] is True
