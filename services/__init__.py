"""
Módulo de serviços.
Contém a lógica de negócio: validação, armazenamento e relatórios.
"""

from .validacao import validar_peso, validar_cor, validar_comprimento, validar_peca
from .armazenamento import adicionar_peca_em_caixa, remover_peca_por_id
from .relatorio import gerar_relatorio_completo

__all__ = [
    'validar_peso',
    'validar_cor', 
    'validar_comprimento',
    'validar_peca',
    'adicionar_peca_em_caixa',
    'remover_peca_por_id',
    'gerar_relatorio_completo'
]
