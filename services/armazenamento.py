"""
Serviço de gerenciamento de armazenamento de peças em caixas.
"""

from typing import TypedDict, List, Tuple, Optional
from models.peca import Peca
from models.caixa import Caixa, CAPACIDADE_MAXIMA_CAIXA, criar_caixa


class SistemaArmazenamento(TypedDict):
    """
    Representa o estado do sistema de armazenamento.
    
    Attributes:
        pecas_aprovadas: Lista de todas as peças aprovadas
        pecas_reprovadas: Lista de todas as peças reprovadas
        caixas_fechadas: Lista de caixas que atingiram capacidade máxima
        caixa_atual: Caixa em preenchimento
        contador_caixas: Contador para gerar IDs únicos de caixas
    """
    pecas_aprovadas: List[Peca]
    pecas_reprovadas: List[Peca]
    caixas_fechadas: List[Caixa]
    caixa_atual: Caixa
    contador_caixas: int


def adicionar_peca_em_caixa(
    peca: Peca,
    sistema: SistemaArmazenamento
) -> Tuple[bool, str]:
    """
    Adiciona uma peça aprovada na caixa atual.
    Fecha a caixa automaticamente ao atingir capacidade máxima.
    
    Args:
        peca: Peça aprovada a ser adicionada
        sistema: Estado atual do sistema de armazenamento
    
    Returns:
        Tupla (caixa_fechada, mensagem)
        - caixa_fechada: True se a caixa foi fechada após adicionar a peça
        - mensagem: Mensagem descritiva do resultado
    """
    if not peca['aprovada']:
        return False, "Apenas peças aprovadas podem ser armazenadas em caixas"
    
    # Adiciona peça na caixa atual
    sistema['caixa_atual']['pecas'].append(peca)
    sistema['pecas_aprovadas'].append(peca)
    
    total_pecas_caixa = len(sistema['caixa_atual']['pecas'])
    
    # Verifica se a caixa atingiu capacidade máxima
    if total_pecas_caixa >= CAPACIDADE_MAXIMA_CAIXA:
        # Fecha a caixa atual
        sistema['caixa_atual']['fechada'] = True
        sistema['caixas_fechadas'].append(sistema['caixa_atual'])
        
        # Cria nova caixa
        sistema['contador_caixas'] += 1
        sistema['caixa_atual'] = criar_caixa(sistema['contador_caixas'])
        
        mensagem = (
            f"Peça {peca['id']} adicionada. "
            f"📦 Caixa #{total_pecas_caixa - 1} FECHADA (10 peças completas). "
            f"🆕 Caixa #{sistema['contador_caixas']} iniciada"
        )
        return True, mensagem
    
    mensagem = (
        f"Peça {peca['id']} adicionada à Caixa #{sistema['caixa_atual']['id']} "
        f"({total_pecas_caixa}/{CAPACIDADE_MAXIMA_CAIXA} peças)"
    )
    return False, mensagem


def remover_peca_por_id(
    id_peca: str,
    sistema: SistemaArmazenamento
) -> Tuple[bool, str]:
    """
    Remove uma peça cadastrada do sistema.
    
    Args:
        id_peca: Identificador da peça a ser removida
        sistema: Estado atual do sistema
    
    Returns:
        Tupla (sucesso, mensagem)
        - sucesso: True se a peça foi encontrada e removida
        - mensagem: Mensagem descritiva do resultado
    """
    # Busca em peças aprovadas
    for i, peca in enumerate(sistema['pecas_aprovadas']):
        if peca['id'] == id_peca:
            sistema['pecas_aprovadas'].pop(i)
            
            # Remove da caixa atual se estiver lá
            for j, peca_caixa in enumerate(sistema['caixa_atual']['pecas']):
                if peca_caixa['id'] == id_peca:
                    sistema['caixa_atual']['pecas'].pop(j)
                    return True, f"Peça {id_peca} removida da caixa atual"
            
            # Remove de caixas fechadas (não deve acontecer normalmente)
            for caixa in sistema['caixas_fechadas']:
                for j, peca_caixa in enumerate(caixa['pecas']):
                    if peca_caixa['id'] == id_peca:
                        caixa['pecas'].pop(j)
                        return True, f"Peça {id_peca} removida da Caixa #{caixa['id']}"
            
            return True, f"Peça {id_peca} removida (aprovada)"
    
    # Busca em peças reprovadas
    for i, peca in enumerate(sistema['pecas_reprovadas']):
        if peca['id'] == id_peca:
            sistema['pecas_reprovadas'].pop(i)
            return True, f"Peça {id_peca} removida (reprovada)"
    
    return False, f"Peça {id_peca} não encontrada no sistema"


def inicializar_sistema() -> SistemaArmazenamento:
    """
    Inicializa o sistema de armazenamento com valores padrão.
    
    Returns:
        Instância de SistemaArmazenamento inicializada
    """
    return SistemaArmazenamento(
        pecas_aprovadas=[],
        pecas_reprovadas=[],
        caixas_fechadas=[],
        caixa_atual=criar_caixa(1),
        contador_caixas=1
    )
