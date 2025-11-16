"""
Modelo de dados para Peça.
"""

from typing import TypedDict, List


class Peca(TypedDict):
    """
    Representa uma peça com suas características e status de aprovação.
    
    Attributes:
        id: Identificador único da peça
        peso: Peso da peça em gramas
        cor: Cor da peça (azul, verde, etc.)
        comprimento: Comprimento da peça em centímetros
        aprovada: Status de aprovação (True/False)
        motivos_reprovacao: Lista de motivos caso seja reprovada
    """
    id: str
    peso: float
    cor: str
    comprimento: float
    aprovada: bool
    motivos_reprovacao: List[str]


def criar_peca(
    id_peca: str,
    peso: float,
    cor: str,
    comprimento: float,
    aprovada: bool = False,
    motivos_reprovacao: List[str] | None = None
) -> Peca:
    """
    Factory function para criar uma instância de Peça.
    
    Args:
        id_peca: Identificador único da peça
        peso: Peso da peça em gramas
        cor: Cor da peça
        comprimento: Comprimento da peça em centímetros
        aprovada: Status de aprovação (default: False)
        motivos_reprovacao: Lista de motivos de reprovação (default: [])
    
    Returns:
        Instância de Peca
    """
    return Peca(
        id=id_peca,
        peso=peso,
        cor=cor,
        comprimento=comprimento,
        aprovada=aprovada,
        motivos_reprovacao=motivos_reprovacao if motivos_reprovacao else []
    )
