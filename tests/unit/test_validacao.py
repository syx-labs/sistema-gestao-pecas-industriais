"""
Testes unitários para o módulo de validação de qualidade de peças.

Testa:
- Validação de peso (95g a 105g)
- Validação de cor (azul ou verde)
- Validação de comprimento (10cm a 20cm)
- Validação completa de peça
"""

import pytest
from services.validacao import (
    validar_peso,
    validar_cor,
    validar_comprimento,
    validar_peca,
    PESO_MINIMO,
    PESO_MAXIMO,
    CORES_ACEITAS,
    COMPRIMENTO_MINIMO,
    COMPRIMENTO_MAXIMO
)
from models.peca import criar_peca


# ========================================
# TESTES DE VALIDAÇÃO DE PESO
# ========================================

class TestValidarPeso:
    """Testes para a função validar_peso()."""

    @pytest.mark.unit
    def test_peso_valido_no_minimo(self):
        """Peso exatamente no limite mínimo (95g) deve ser aprovado."""
        valido, mensagem = validar_peso(95.0)
        assert valido is True
        assert mensagem == ""

    @pytest.mark.unit
    def test_peso_valido_no_maximo(self):
        """Peso exatamente no limite máximo (105g) deve ser aprovado."""
        valido, mensagem = validar_peso(105.0)
        assert valido is True
        assert mensagem == ""

    @pytest.mark.unit
    def test_peso_valido_no_meio(self):
        """Peso no meio do intervalo (100g) deve ser aprovado."""
        valido, mensagem = validar_peso(100.0)
        assert valido is True
        assert mensagem == ""

    @pytest.mark.unit
    @pytest.mark.parametrize("peso", [95.0, 96.5, 100.0, 103.7, 105.0])
    def test_pesos_validos_diversos(self, peso):
        """Diversos pesos dentro do intervalo devem ser aprovados."""
        valido, mensagem = validar_peso(peso)
        assert valido is True
        assert mensagem == ""

    @pytest.mark.unit
    @pytest.mark.edge_case
    def test_peso_abaixo_do_minimo(self):
        """Peso abaixo do mínimo (94.9g) deve ser reprovado."""
        valido, mensagem = validar_peso(94.9)
        assert valido is False
        assert "Peso fora do intervalo" in mensagem
        assert "94.9" in mensagem

    @pytest.mark.unit
    @pytest.mark.edge_case
    def test_peso_acima_do_maximo(self):
        """Peso acima do máximo (105.1g) deve ser reprovado."""
        valido, mensagem = validar_peso(105.1)
        assert valido is False
        assert "Peso fora do intervalo" in mensagem
        assert "105.1" in mensagem

    @pytest.mark.unit
    def test_peso_muito_baixo(self):
        """Peso muito baixo (50g) deve ser reprovado."""
        valido, mensagem = validar_peso(50.0)
        assert valido is False
        assert "95.0-105.0" in mensagem

    @pytest.mark.unit
    def test_peso_muito_alto(self):
        """Peso muito alto (200g) deve ser reprovado."""
        valido, mensagem = validar_peso(200.0)
        assert valido is False
        assert "95.0-105.0" in mensagem

    @pytest.mark.unit
    @pytest.mark.edge_case
    def test_peso_zero(self):
        """Peso zero deve ser reprovado."""
        valido, mensagem = validar_peso(0.0)
        assert valido is False

    @pytest.mark.unit
    @pytest.mark.edge_case
    def test_peso_negativo(self):
        """Peso negativo deve ser reprovado."""
        valido, mensagem = validar_peso(-10.0)
        assert valido is False

    @pytest.mark.unit
    @pytest.mark.parametrize("peso", [50.0, 70.0, 94.99, 105.01, 120.0, 500.0])
    def test_pesos_invalidos_diversos(self, peso):
        """Diversos pesos fora do intervalo devem ser reprovados."""
        valido, mensagem = validar_peso(peso)
        assert valido is False
        assert mensagem != ""


# ========================================
# TESTES DE VALIDAÇÃO DE COR
# ========================================

class TestValidarCor:
    """Testes para a função validar_cor()."""

    @pytest.mark.unit
    def test_cor_azul_lowercase(self):
        """Cor 'azul' em minúsculas deve ser aceita."""
        valido, mensagem = validar_cor("azul")
        assert valido is True
        assert mensagem == ""

    @pytest.mark.unit
    def test_cor_verde_lowercase(self):
        """Cor 'verde' em minúsculas deve ser aceita."""
        valido, mensagem = validar_cor("verde")
        assert valido is True
        assert mensagem == ""

    @pytest.mark.unit
    def test_cor_azul_uppercase(self):
        """Cor 'AZUL' em maiúsculas deve ser aceita (case-insensitive)."""
        valido, mensagem = validar_cor("AZUL")
        assert valido is True
        assert mensagem == ""

    @pytest.mark.unit
    def test_cor_verde_uppercase(self):
        """Cor 'VERDE' em maiúsculas deve ser aceita (case-insensitive)."""
        valido, mensagem = validar_cor("VERDE")
        assert valido is True
        assert mensagem == ""

    @pytest.mark.unit
    @pytest.mark.parametrize("cor", ["Azul", "AzUl", "AZUL", "azul"])
    def test_cor_azul_mixed_case(self, cor):
        """Cor 'azul' em diferentes cases deve ser aceita."""
        valido, mensagem = validar_cor(cor)
        assert valido is True

    @pytest.mark.unit
    @pytest.mark.parametrize("cor", ["Verde", "VeRdE", "VERDE", "verde"])
    def test_cor_verde_mixed_case(self, cor):
        """Cor 'verde' em diferentes cases deve ser aceita."""
        valido, mensagem = validar_cor(cor)
        assert valido is True

    @pytest.mark.unit
    def test_cor_azul_com_espacos(self):
        """Cor com espaços ' azul ' deve ser aceita após strip()."""
        valido, mensagem = validar_cor("  azul  ")
        assert valido is True

    @pytest.mark.unit
    def test_cor_verde_com_espacos(self):
        """Cor com espaços ' verde ' deve ser aceita após strip()."""
        valido, mensagem = validar_cor("  verde  ")
        assert valido is True

    @pytest.mark.unit
    def test_cor_vermelho(self):
        """Cor 'vermelho' não deve ser aceita."""
        valido, mensagem = validar_cor("vermelho")
        assert valido is False
        assert "Cor inadequada" in mensagem
        assert "vermelho" in mensagem

    @pytest.mark.unit
    @pytest.mark.parametrize("cor", ["vermelho", "amarelo", "preto", "branco", "roxo"])
    def test_cores_invalidas(self, cor):
        """Cores não aceitas devem ser reprovadas."""
        valido, mensagem = validar_cor(cor)
        assert valido is False
        assert "azul ou verde" in mensagem

    @pytest.mark.unit
    @pytest.mark.edge_case
    def test_cor_vazia(self):
        """String vazia não deve ser aceita."""
        valido, mensagem = validar_cor("")
        assert valido is False

    @pytest.mark.unit
    @pytest.mark.edge_case
    def test_cor_apenas_espacos(self):
        """String com apenas espaços não deve ser aceita."""
        valido, mensagem = validar_cor("   ")
        assert valido is False

    @pytest.mark.unit
    def test_cor_azul_plural(self):
        """Variação 'azuis' não deve ser aceita."""
        valido, mensagem = validar_cor("azuis")
        assert valido is False

    @pytest.mark.unit
    def test_cor_verde_plural(self):
        """Variação 'verdes' não deve ser aceita."""
        valido, mensagem = validar_cor("verdes")
        assert valido is False

    @pytest.mark.unit
    def test_cor_blue_ingles(self):
        """Cor em inglês 'blue' não deve ser aceita."""
        valido, mensagem = validar_cor("blue")
        assert valido is False

    @pytest.mark.unit
    def test_cor_green_ingles(self):
        """Cor em inglês 'green' não deve ser aceita."""
        valido, mensagem = validar_cor("green")
        assert valido is False

    @pytest.mark.unit
    def test_mensagem_erro_contem_cores_aceitas(self):
        """Mensagem de erro deve listar as cores aceitas."""
        valido, mensagem = validar_cor("roxo")
        assert "azul ou verde" in mensagem


# ========================================
# TESTES DE VALIDAÇÃO DE COMPRIMENTO
# ========================================

class TestValidarComprimento:
    """Testes para a função validar_comprimento()."""

    @pytest.mark.unit
    def test_comprimento_valido_no_minimo(self):
        """Comprimento exatamente no limite mínimo (10cm) deve ser aprovado."""
        valido, mensagem = validar_comprimento(10.0)
        assert valido is True
        assert mensagem == ""

    @pytest.mark.unit
    def test_comprimento_valido_no_maximo(self):
        """Comprimento exatamente no limite máximo (20cm) deve ser aprovado."""
        valido, mensagem = validar_comprimento(20.0)
        assert valido is True
        assert mensagem == ""

    @pytest.mark.unit
    def test_comprimento_valido_no_meio(self):
        """Comprimento no meio do intervalo (15cm) deve ser aprovado."""
        valido, mensagem = validar_comprimento(15.0)
        assert valido is True
        assert mensagem == ""

    @pytest.mark.unit
    @pytest.mark.parametrize("comprimento", [10.0, 12.5, 15.0, 17.8, 20.0])
    def test_comprimentos_validos_diversos(self, comprimento):
        """Diversos comprimentos dentro do intervalo devem ser aprovados."""
        valido, mensagem = validar_comprimento(comprimento)
        assert valido is True
        assert mensagem == ""

    @pytest.mark.unit
    @pytest.mark.edge_case
    def test_comprimento_abaixo_do_minimo(self):
        """Comprimento abaixo do mínimo (9.9cm) deve ser reprovado."""
        valido, mensagem = validar_comprimento(9.9)
        assert valido is False
        assert "Comprimento fora do intervalo" in mensagem
        assert "9.9" in mensagem

    @pytest.mark.unit
    @pytest.mark.edge_case
    def test_comprimento_acima_do_maximo(self):
        """Comprimento acima do máximo (20.1cm) deve ser reprovado."""
        valido, mensagem = validar_comprimento(20.1)
        assert valido is False
        assert "Comprimento fora do intervalo" in mensagem
        assert "20.1" in mensagem

    @pytest.mark.unit
    def test_comprimento_muito_baixo(self):
        """Comprimento muito baixo (5cm) deve ser reprovado."""
        valido, mensagem = validar_comprimento(5.0)
        assert valido is False
        assert "10.0-20.0" in mensagem

    @pytest.mark.unit
    def test_comprimento_muito_alto(self):
        """Comprimento muito alto (50cm) deve ser reprovado."""
        valido, mensagem = validar_comprimento(50.0)
        assert valido is False
        assert "10.0-20.0" in mensagem

    @pytest.mark.unit
    @pytest.mark.edge_case
    def test_comprimento_zero(self):
        """Comprimento zero deve ser reprovado."""
        valido, mensagem = validar_comprimento(0.0)
        assert valido is False

    @pytest.mark.unit
    @pytest.mark.edge_case
    def test_comprimento_negativo(self):
        """Comprimento negativo deve ser reprovado."""
        valido, mensagem = validar_comprimento(-5.0)
        assert valido is False

    @pytest.mark.unit
    @pytest.mark.parametrize("comprimento", [5.0, 9.99, 20.01, 25.0, 100.0])
    def test_comprimentos_invalidos_diversos(self, comprimento):
        """Diversos comprimentos fora do intervalo devem ser reprovados."""
        valido, mensagem = validar_comprimento(comprimento)
        assert valido is False
        assert mensagem != ""


# ========================================
# TESTES DE VALIDAÇÃO COMPLETA DE PEÇA
# ========================================

class TestValidarPeca:
    """Testes para a função validar_peca() que combina todas as validações."""

    @pytest.mark.unit
    def test_peca_todos_criterios_validos(self, peca_valida):
        """Peça com todos os critérios válidos deve ser aprovada."""
        aprovada, motivos = validar_peca(peca_valida)
        assert aprovada is True
        assert len(motivos) == 0

    @pytest.mark.unit
    def test_peca_apenas_peso_invalido(self):
        """Peça com apenas peso inválido deve ser reprovada com 1 motivo."""
        peca = criar_peca("P001", 120.0, "azul", 15.0)
        aprovada, motivos = validar_peca(peca)
        assert aprovada is False
        assert len(motivos) == 1
        assert "Peso fora do intervalo" in motivos[0]

    @pytest.mark.unit
    def test_peca_apenas_cor_invalida(self):
        """Peça com apenas cor inválida deve ser reprovada com 1 motivo."""
        peca = criar_peca("P001", 100.0, "vermelho", 15.0)
        aprovada, motivos = validar_peca(peca)
        assert aprovada is False
        assert len(motivos) == 1
        assert "Cor inadequada" in motivos[0]

    @pytest.mark.unit
    def test_peca_apenas_comprimento_invalido(self):
        """Peça com apenas comprimento inválido deve ser reprovada com 1 motivo."""
        peca = criar_peca("P001", 100.0, "azul", 25.0)
        aprovada, motivos = validar_peca(peca)
        assert aprovada is False
        assert len(motivos) == 1
        assert "Comprimento fora do intervalo" in motivos[0]

    @pytest.mark.unit
    def test_peca_peso_e_cor_invalidos(self):
        """Peça com peso e cor inválidos deve ter 2 motivos de reprovação."""
        peca = criar_peca("P001", 120.0, "vermelho", 15.0)
        aprovada, motivos = validar_peca(peca)
        assert aprovada is False
        assert len(motivos) == 2
        assert any("Peso" in m for m in motivos)
        assert any("Cor" in m for m in motivos)

    @pytest.mark.unit
    def test_peca_peso_e_comprimento_invalidos(self):
        """Peça com peso e comprimento inválidos deve ter 2 motivos de reprovação."""
        peca = criar_peca("P001", 120.0, "azul", 25.0)
        aprovada, motivos = validar_peca(peca)
        assert aprovada is False
        assert len(motivos) == 2
        assert any("Peso" in m for m in motivos)
        assert any("Comprimento" in m for m in motivos)

    @pytest.mark.unit
    def test_peca_cor_e_comprimento_invalidos(self):
        """Peça com cor e comprimento inválidos deve ter 2 motivos de reprovação."""
        peca = criar_peca("P001", 100.0, "vermelho", 25.0)
        aprovada, motivos = validar_peca(peca)
        assert aprovada is False
        assert len(motivos) == 2
        assert any("Cor" in m for m in motivos)
        assert any("Comprimento" in m for m in motivos)

    @pytest.mark.unit
    def test_peca_todos_criterios_invalidos(self, peca_todos_criterios_invalidos):
        """Peça com todos os critérios inválidos deve ter 3 motivos de reprovação."""
        aprovada, motivos = validar_peca(peca_todos_criterios_invalidos)
        assert aprovada is False
        assert len(motivos) == 3
        assert any("Peso" in m for m in motivos)
        assert any("Cor" in m for m in motivos)
        assert any("Comprimento" in m for m in motivos)

    @pytest.mark.unit
    @pytest.mark.parametrize("peso,cor,comprimento,deve_aprovar", [
        (100.0, "azul", 15.0, True),      # Todos válidos
        (100.0, "verde", 15.0, True),     # Todos válidos (cor verde)
        (95.0, "azul", 10.0, True),       # Limites mínimos
        (105.0, "verde", 20.0, True),     # Limites máximos
        (94.9, "azul", 15.0, False),      # Peso inválido
        (100.0, "vermelho", 15.0, False), # Cor inválida
        (100.0, "azul", 9.9, False),      # Comprimento inválido
    ])
    def test_validacao_diversos_cenarios(self, peso, cor, comprimento, deve_aprovar):
        """Teste parametrizado com diversos cenários de validação."""
        peca = criar_peca("TEST", peso, cor, comprimento)
        aprovada, motivos = validar_peca(peca)
        assert aprovada == deve_aprovar

    @pytest.mark.unit
    def test_validacao_preserva_dados_originais_da_peca(self):
        """Validação não deve alterar os dados originais da peça."""
        peca = criar_peca("P001", 100.0, "azul", 15.0)
        peca_original = peca.copy()

        validar_peca(peca)

        assert peca['id'] == peca_original['id']
        assert peca['peso'] == peca_original['peso']
        assert peca['cor'] == peca_original['cor']
        assert peca['comprimento'] == peca_original['comprimento']

    @pytest.mark.unit
    def test_motivos_reprovacao_sao_strings(self):
        """Motivos de reprovação devem ser strings."""
        peca = criar_peca("P001", 120.0, "vermelho", 25.0)
        aprovada, motivos = validar_peca(peca)

        assert all(isinstance(m, str) for m in motivos)
        assert all(len(m) > 0 for m in motivos)
