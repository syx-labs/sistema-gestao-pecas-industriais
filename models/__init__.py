"""
Módulo de modelos de dados.
Contém as estruturas de Peça e Caixa.
"""

from .peca import Peca, criar_peca
from .caixa import Caixa, criar_caixa

__all__ = ['Peca', 'criar_peca', 'Caixa', 'criar_caixa']
