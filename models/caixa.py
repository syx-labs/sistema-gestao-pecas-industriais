"""
Modelo de dados para Caixa.
Define a capacidade máxima de peças por caixa.
"""

from typing import TypedDict, List
from .peca import Peca


# Constante que define a capacidade máxima de peças por caixa
CAPACIDADE_MAXIMA_CAIXA = 10


class Caixa(TypedDict):
    """
    Representa uma caixa de armazenamento de peças aprovadas.
    
    Attributes:
        id: Identificador único da caixa
        pecas: Lista de peças armazenadas
        fechada: Indica se a caixa está fechada (atingiu capacidade máxima)
    """
    id: int
    pecas: List[Peca]
    fechada: bool


def criar_caixa(id_caixa: int) -> Caixa:
    """
    Factory function para criar uma nova caixa vazia.
    
    Args:
        id_caixa: Identificador único da caixa
    
    Returns:
        Instância de Caixa
    """
    return Caixa(
        id=id_caixa,
        pecas=[],
        fechada=False
    )
