"""
Serviço de validação de qualidade de peças.
Implementa os critérios de aprovação/reprovação.
"""

from typing import Tuple, List
from models.peca import Peca


# Constantes dos critérios de qualidade
PESO_MINIMO = 95.0
PESO_MAXIMO = 105.0
CORES_ACEITAS = ['azul', 'verde']
COMPRIMENTO_MINIMO = 10.0
COMPRIMENTO_MAXIMO = 20.0


def validar_peso(peso: float) -> Tuple[bool, str]:
    """
    Valida se o peso está dentro do intervalo aceitável.
    
    Args:
        peso: Peso da peça em gramas
    
    Returns:
        Tupla (válido, mensagem_erro)
        - válido: True se o peso estiver no intervalo [95g, 105g]
        - mensagem_erro: String vazia se válido, mensagem de erro caso contrário
    """
    if PESO_MINIMO <= peso <= PESO_MAXIMO:
        return True, ""
    return False, f"Peso fora do intervalo ({PESO_MINIMO}-{PESO_MAXIMO}g): {peso}g"


def validar_cor(cor: str) -> Tuple[bool, str]:
    """
    Valida se a cor está entre as cores aceitas.
    
    Args:
        cor: Cor da peça
    
    Returns:
        Tupla (válido, mensagem_erro)
        - válido: True se a cor for azul ou verde (case-insensitive)
        - mensagem_erro: String vazia se válido, mensagem de erro caso contrário
    """
    cor_normalizada = cor.lower().strip()
    if cor_normalizada in CORES_ACEITAS:
        return True, ""
    cores_formatadas = " ou ".join(CORES_ACEITAS)
    return False, f"Cor inadequada (esperado: {cores_formatadas}): {cor}"


def validar_comprimento(comprimento: float) -> Tuple[bool, str]:
    """
    Valida se o comprimento está dentro do intervalo aceitável.
    
    Args:
        comprimento: Comprimento da peça em centímetros
    
    Returns:
        Tupla (válido, mensagem_erro)
        - válido: True se o comprimento estiver no intervalo [10cm, 20cm]
        - mensagem_erro: String vazia se válido, mensagem de erro caso contrário
    """
    if COMPRIMENTO_MINIMO <= comprimento <= COMPRIMENTO_MAXIMO:
        return True, ""
    return False, f"Comprimento fora do intervalo ({COMPRIMENTO_MINIMO}-{COMPRIMENTO_MAXIMO}cm): {comprimento}cm"


def validar_peca(peca: Peca) -> Tuple[bool, List[str]]:
    """
    Valida todos os critérios de qualidade de uma peça.
    
    Uma peça é aprovada apenas se TODOS os critérios forem atendidos:
    - Peso entre 95g e 105g
    - Cor azul ou verde
    - Comprimento entre 10cm e 20cm
    
    Args:
        peca: Instância de Peca a ser validada
    
    Returns:
        Tupla (aprovada, motivos_reprovacao)
        - aprovada: True se todos os critérios forem atendidos
        - motivos_reprovacao: Lista de strings com os motivos de reprovação (vazia se aprovada)
    """
    motivos = []
    
    peso_valido, mensagem_peso = validar_peso(peca['peso'])
    if not peso_valido:
        motivos.append(mensagem_peso)
    
    cor_valida, mensagem_cor = validar_cor(peca['cor'])
    if not cor_valida:
        motivos.append(mensagem_cor)
    
    comprimento_valido, mensagem_comprimento = validar_comprimento(peca['comprimento'])
    if not comprimento_valido:
        motivos.append(mensagem_comprimento)
    
    aprovada = len(motivos) == 0
    return aprovada, motivos
