"""
Fixtures compartilhados para todos os testes.
"""

import pytest
from models.peca import criar_peca
from models.caixa import criar_caixa
from services.armazenamento import inicializar_sistema, SistemaArmazenamento


# ========================================
# FIXTURES DE PEÇAS
# ========================================

@pytest.fixture
def peca_valida():
    """Peça que atende todos os critérios de qualidade."""
    return criar_peca(
        id_peca="P001",
        peso=100.0,
        cor="azul",
        comprimento=15.0,
        aprovada=False
    )


@pytest.fixture
def peca_peso_invalido():
    """Peça com peso fora do intervalo aceitável."""
    return criar_peca(
        id_peca="P002",
        peso=120.0,  # Acima de 105g
        cor="verde",
        comprimento=15.0,
        aprovada=False
    )


@pytest.fixture
def peca_cor_invalida():
    """Peça com cor não aceita."""
    return criar_peca(
        id_peca="P003",
        peso=100.0,
        cor="vermelho",  # Não é azul ou verde
        comprimento=15.0,
        aprovada=False
    )


@pytest.fixture
def peca_comprimento_invalido():
    """Peça com comprimento fora do intervalo aceitável."""
    return criar_peca(
        id_peca="P004",
        peso=100.0,
        cor="azul",
        comprimento=25.0,  # Acima de 20cm
        aprovada=False
    )


@pytest.fixture
def peca_todos_criterios_invalidos():
    """Peça que falha em todos os critérios."""
    return criar_peca(
        id_peca="P005",
        peso=150.0,      # Fora do intervalo
        cor="amarelo",   # Cor inválida
        comprimento=5.0, # Fora do intervalo
        aprovada=False
    )


@pytest.fixture
def peca_aprovada():
    """Peça já validada e aprovada."""
    return criar_peca(
        id_peca="P100",
        peso=100.0,
        cor="azul",
        comprimento=15.0,
        aprovada=True,
        motivos_reprovacao=[]
    )


@pytest.fixture
def peca_reprovada():
    """Peça já validada e reprovada."""
    return criar_peca(
        id_peca="P200",
        peso=120.0,
        cor="vermelho",
        comprimento=15.0,
        aprovada=False,
        motivos_reprovacao=[
            "Peso fora do intervalo (95.0-105.0g): 120.0g",
            "Cor inadequada (esperado: azul ou verde): vermelho"
        ]
    )


# ========================================
# FIXTURES DE CAIXAS
# ========================================

@pytest.fixture
def caixa_vazia():
    """Caixa vazia recém criada."""
    return criar_caixa(id_caixa=1)


@pytest.fixture
def caixa_com_uma_peca(peca_aprovada):
    """Caixa com uma peça."""
    caixa = criar_caixa(id_caixa=1)
    caixa['pecas'].append(peca_aprovada)
    return caixa


@pytest.fixture
def caixa_quase_cheia():
    """Caixa com 9 peças (quase cheia)."""
    caixa = criar_caixa(id_caixa=1)
    for i in range(9):
        peca = criar_peca(
            id_peca=f"P{i:03d}",
            peso=100.0,
            cor="azul",
            comprimento=15.0,
            aprovada=True
        )
        caixa['pecas'].append(peca)
    return caixa


@pytest.fixture
def caixa_cheia():
    """Caixa com capacidade máxima (10 peças)."""
    caixa = criar_caixa(id_caixa=1)
    caixa['fechada'] = True
    for i in range(10):
        peca = criar_peca(
            id_peca=f"P{i:03d}",
            peso=100.0,
            cor="azul",
            comprimento=15.0,
            aprovada=True
        )
        caixa['pecas'].append(peca)
    return caixa


# ========================================
# FIXTURES DE SISTEMA
# ========================================

@pytest.fixture
def sistema_vazio():
    """Sistema de armazenamento vazio recém inicializado."""
    return inicializar_sistema()


@pytest.fixture
def sistema_com_pecas_aprovadas():
    """Sistema com 5 peças aprovadas na caixa atual."""
    sistema = inicializar_sistema()

    for i in range(5):
        peca = criar_peca(
            id_peca=f"PA{i:03d}",
            peso=100.0,
            cor="azul",
            comprimento=15.0,
            aprovada=True
        )
        sistema['pecas_aprovadas'].append(peca)
        sistema['caixa_atual']['pecas'].append(peca)

    return sistema


@pytest.fixture
def sistema_com_pecas_reprovadas():
    """Sistema com 3 peças reprovadas."""
    sistema = inicializar_sistema()

    motivos = [
        ["Peso fora do intervalo (95.0-105.0g): 120.0g"],
        ["Cor inadequada (esperado: azul ou verde): vermelho"],
        ["Comprimento fora do intervalo (10.0-20.0cm): 25.0cm"]
    ]

    for i, motivo in enumerate(motivos):
        peca = criar_peca(
            id_peca=f"PR{i:03d}",
            peso=120.0 if i == 0 else 100.0,
            cor="vermelho" if i == 1 else "azul",
            comprimento=25.0 if i == 2 else 15.0,
            aprovada=False,
            motivos_reprovacao=motivo
        )
        sistema['pecas_reprovadas'].append(peca)

    return sistema


@pytest.fixture
def sistema_com_caixa_quase_cheia():
    """Sistema com caixa atual contendo 9 peças."""
    sistema = inicializar_sistema()

    for i in range(9):
        peca = criar_peca(
            id_peca=f"P{i:03d}",
            peso=100.0,
            cor="azul",
            comprimento=15.0,
            aprovada=True
        )
        sistema['pecas_aprovadas'].append(peca)
        sistema['caixa_atual']['pecas'].append(peca)

    return sistema


@pytest.fixture
def sistema_com_multiplas_caixas():
    """Sistema com 2 caixas fechadas e uma em preenchimento."""
    sistema = inicializar_sistema()

    # Primeira caixa fechada
    caixa1 = criar_caixa(id_caixa=1)
    caixa1['fechada'] = True
    for i in range(10):
        peca = criar_peca(
            id_peca=f"P1_{i:03d}",
            peso=100.0,
            cor="azul",
            comprimento=15.0,
            aprovada=True
        )
        caixa1['pecas'].append(peca)
        sistema['pecas_aprovadas'].append(peca)
    sistema['caixas_fechadas'].append(caixa1)

    # Segunda caixa fechada
    caixa2 = criar_caixa(id_caixa=2)
    caixa2['fechada'] = True
    for i in range(10):
        peca = criar_peca(
            id_peca=f"P2_{i:03d}",
            peso=100.0,
            cor="verde",
            comprimento=15.0,
            aprovada=True
        )
        caixa2['pecas'].append(peca)
        sistema['pecas_aprovadas'].append(peca)
    sistema['caixas_fechadas'].append(caixa2)

    # Caixa atual (em preenchimento) com 5 peças
    sistema['caixa_atual'] = criar_caixa(id_caixa=3)
    for i in range(5):
        peca = criar_peca(
            id_peca=f"P3_{i:03d}",
            peso=100.0,
            cor="azul",
            comprimento=15.0,
            aprovada=True
        )
        sistema['caixa_atual']['pecas'].append(peca)
        sistema['pecas_aprovadas'].append(peca)

    sistema['contador_caixas'] = 3

    return sistema


# ========================================
# FIXTURES DE DADOS DE TESTE
# ========================================

@pytest.fixture
def dados_peca_valida():
    """Dados brutos para criar uma peça válida."""
    return {
        'id_peca': 'TEST001',
        'peso': 100.0,
        'cor': 'azul',
        'comprimento': 15.0
    }


@pytest.fixture
def lista_pecas_mistas():
    """Lista com mix de peças aprovadas e reprovadas."""
    return [
        criar_peca("P001", 100.0, "azul", 15.0, True),
        criar_peca("P002", 120.0, "vermelho", 15.0, False, ["Peso inválido", "Cor inválida"]),
        criar_peca("P003", 98.0, "verde", 18.0, True),
        criar_peca("P004", 90.0, "azul", 5.0, False, ["Peso inválido", "Comprimento inválido"]),
        criar_peca("P005", 102.0, "azul", 12.0, True),
    ]
