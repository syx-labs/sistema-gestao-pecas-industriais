"""
Funções de interface do menu interativo.
"""

import os
from typing import Optional
from models.peca import criar_peca
from services.validacao import validar_peca
from services.armazenamento import SistemaArmazenamento, adicionar_peca_em_caixa, remover_peca_por_id
from services.relatorio import gerar_relatorio_completo
from models.caixa import CAPACIDADE_MAXIMA_CAIXA


def limpar_terminal() -> None:
    """Limpa o terminal de acordo com o sistema operacional."""
    os.system('clear' if os.name == 'posix' else 'cls')


def exibir_menu_principal() -> None:
    """Exibe o menu principal do sistema."""
    print("\n" + "=" * 40)
    print("SISTEMA DE GESTÃO DE PEÇAS".center(40))
    print("=" * 40)
    print("1. Cadastrar nova peça")
    print("2. Listar peças aprovadas/reprovadas")
    print("3. Remover peça cadastrada")
    print("4. Listar caixas fechadas")
    print("5. Gerar relatório final")
    print("0. Sair")
    print("=" * 40)


def solicitar_numero(mensagem: str, tipo_numero: str = "float") -> Optional[float]:
    """
    Solicita um número ao usuário com validação.
    
    Args:
        mensagem: Mensagem a exibir
        tipo_numero: "float" ou "int"
    
    Returns:
        Número digitado ou None se inválido
    """
    try:
        valor = input(mensagem)
        if tipo_numero == "int":
            return int(valor)
        return float(valor)
    except ValueError:
        print(f"❌ Erro: Digite um número válido")
        return None


def cadastrar_peca_interface(sistema: SistemaArmazenamento) -> None:
    """
    Interface para cadastrar uma nova peça.
    
    Args:
        sistema: Estado atual do sistema
    """
    print("\n" + "-" * 40)
    print("CADASTRAR NOVA PEÇA".center(40))
    print("-" * 40)
    
    # Coleta dados da peça
    id_peca = input("ID da peça: ").strip()
    if not id_peca:
        print("❌ Erro: ID não pode ser vazio")
        return
    
    # Verifica se ID já existe
    todas_pecas = sistema['pecas_aprovadas'] + sistema['pecas_reprovadas']
    if any(p['id'] == id_peca for p in todas_pecas):
        print(f"❌ Erro: Já existe uma peça com ID '{id_peca}'")
        return
    
    peso = solicitar_numero("Peso (g): ")
    if peso is None:
        return
    
    cor = input("Cor: ").strip()
    if not cor:
        print("❌ Erro: Cor não pode ser vazia")
        return
    
    comprimento = solicitar_numero("Comprimento (cm): ")
    if comprimento is None:
        return
    
    # Cria peça
    peca = criar_peca(
        id_peca=id_peca,
        peso=peso,
        cor=cor,
        comprimento=comprimento
    )
    
    # Valida peça
    aprovada, motivos = validar_peca(peca)
    peca['aprovada'] = aprovada
    peca['motivos_reprovacao'] = motivos
    
    print()
    if aprovada:
        print(f"✅ Peça {id_peca} APROVADA!")
        _, mensagem = adicionar_peca_em_caixa(peca, sistema)
        print(mensagem)
    else:
        print(f"❌ Peça {id_peca} REPROVADA!")
        print("Motivos:")
        for motivo in motivos:
            print(f"  - {motivo}")
        sistema['pecas_reprovadas'].append(peca)


def listar_pecas_interface(sistema: SistemaArmazenamento) -> None:
    """
    Interface para listar peças aprovadas e/ou reprovadas.
    
    Args:
        sistema: Estado atual do sistema
    """
    print("\n" + "-" * 40)
    print("LISTAR PEÇAS".center(40))
    print("-" * 40)
    print("a) Listar peças aprovadas")
    print("b) Listar peças reprovadas")
    print("c) Listar todas as peças")
    print("-" * 40)
    
    opcao = input("Escolha uma opção: ").strip().lower()
    
    print()
    if opcao == 'a':
        listar_pecas_aprovadas(sistema)
    elif opcao == 'b':
        listar_pecas_reprovadas(sistema)
    elif opcao == 'c':
        listar_pecas_aprovadas(sistema)
        print()
        listar_pecas_reprovadas(sistema)
    else:
        print("❌ Opção inválida")


def listar_pecas_aprovadas(sistema: SistemaArmazenamento) -> None:
    """Lista todas as peças aprovadas."""
    pecas = sistema['pecas_aprovadas']
    
    if not pecas:
        print("✅ PEÇAS APROVADAS: Nenhuma peça aprovada cadastrada")
        return
    
    print(f"✅ PEÇAS APROVADAS ({len(pecas)}):")
    print("-" * 40)
    for peca in pecas:
        print(f"  ID: {peca['id']}")
        print(f"    Peso: {peca['peso']}g")
        print(f"    Cor: {peca['cor']}")
        print(f"    Comprimento: {peca['comprimento']}cm")
        print()


def listar_pecas_reprovadas(sistema: SistemaArmazenamento) -> None:
    """Lista todas as peças reprovadas com motivos."""
    pecas = sistema['pecas_reprovadas']
    
    if not pecas:
        print("❌ PEÇAS REPROVADAS: Nenhuma peça reprovada cadastrada")
        return
    
    print(f"❌ PEÇAS REPROVADAS ({len(pecas)}):")
    print("-" * 40)
    for peca in pecas:
        print(f"  ID: {peca['id']}")
        print(f"    Peso: {peca['peso']}g")
        print(f"    Cor: {peca['cor']}")
        print(f"    Comprimento: {peca['comprimento']}cm")
        print(f"    Motivos:")
        for motivo in peca['motivos_reprovacao']:
            print(f"      - {motivo}")
        print()


def remover_peca_interface(sistema: SistemaArmazenamento) -> None:
    """
    Interface para remover uma peça cadastrada.
    
    Args:
        sistema: Estado atual do sistema
    """
    print("\n" + "-" * 40)
    print("REMOVER PEÇA".center(40))
    print("-" * 40)
    
    id_peca = input("ID da peça a remover: ").strip()
    if not id_peca:
        print("❌ Erro: ID não pode ser vazio")
        return
    
    confirmacao = input(f"Confirma remoção da peça '{id_peca}'? (s/n): ").strip().lower()
    if confirmacao != 's':
        print("Operação cancelada")
        return
    
    sucesso, mensagem = remover_peca_por_id(id_peca, sistema)
    print()
    if sucesso:
        print(f"✅ {mensagem}")
    else:
        print(f"❌ {mensagem}")


def listar_caixas_interface(sistema: SistemaArmazenamento) -> None:
    """
    Interface para listar todas as caixas (fechadas e atual).
    
    Args:
        sistema: Estado atual do sistema
    """
    print("\n" + "-" * 40)
    print("LISTAGEM DE CAIXAS".center(40))
    print("-" * 40)
    
    caixas_fechadas = sistema['caixas_fechadas']
    caixa_atual = sistema['caixa_atual']
    
    if not caixas_fechadas and len(caixa_atual['pecas']) == 0:
        print("Nenhuma caixa com peças cadastradas")
        return
    
    # Lista caixas fechadas
    if caixas_fechadas:
        print(f"\n📦 CAIXAS FECHADAS ({len(caixas_fechadas)}):")
        print("-" * 40)
        for caixa in caixas_fechadas:
            print(f"\n  Caixa #{caixa['id']} - {len(caixa['pecas'])} peças")
            print(f"  Status: {'🔒 Fechada' if caixa['fechada'] else '🔓 Aberta'}")
            print(f"  IDs das peças: {', '.join(p['id'] for p in caixa['pecas'])}")
    
    # Lista caixa atual (em preenchimento)
    if len(caixa_atual['pecas']) > 0:
        print(f"\n📦 CAIXA EM PREENCHIMENTO:")
        print("-" * 40)
        print(f"  Caixa #{caixa_atual['id']} - {len(caixa_atual['pecas'])}/{CAPACIDADE_MAXIMA_CAIXA} peças")
        print(f"  IDs das peças: {', '.join(p['id'] for p in caixa_atual['pecas'])}")


def gerar_relatorio_interface(sistema: SistemaArmazenamento) -> None:
    """
    Interface para gerar e exibir o relatório final.
    
    Args:
        sistema: Estado atual do sistema
    """
    print()
    relatorio = gerar_relatorio_completo(sistema)
    print(relatorio)
