#!/usr/bin/env python3
"""
Sistema de Automação Digital para Gestão de Peças Industriais

Desenvolvido para automatizar o controle de produção e qualidade de peças
fabricadas em linha de montagem.

Autor: Gabriel Falcão
Data: 2025-11-15
"""

from services.armazenamento import inicializar_sistema
from utils.menu import (
    exibir_menu_principal,
    cadastrar_peca_interface,
    listar_pecas_interface,
    remover_peca_interface,
    listar_caixas_interface,
    gerar_relatorio_interface,
    limpar_terminal
)


def main() -> None:
    """
    Função principal do sistema.
    Inicializa o sistema e executa o loop do menu interativo.
    """
    # Inicializa o sistema
    sistema = inicializar_sistema()
    
    # Banner de boas-vindas
    limpar_terminal()
    print("=" * 50)
    print("BEM-VINDO AO SISTEMA DE GESTÃO DE PEÇAS".center(50))
    print("=" * 50)
    print()
    print("Sistema de Automação Digital para Controle de Qualidade")
    print()
    input("Pressione ENTER para continuar...")
    
    # Loop principal do menu
    while True:
        exibir_menu_principal()
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == '1':
            cadastrar_peca_interface(sistema)
        
        elif opcao == '2':
            listar_pecas_interface(sistema)
        
        elif opcao == '3':
            remover_peca_interface(sistema)
        
        elif opcao == '4':
            listar_caixas_interface(sistema)
        
        elif opcao == '5':
            gerar_relatorio_interface(sistema)
        
        elif opcao == '0':
            print("\n" + "=" * 40)
            print("Encerrando sistema...".center(40))
            print("Obrigado por utilizar o sistema!".center(40))
            print("=" * 40)
            break
        
        else:
            print("\n❌ Opção inválida! Por favor, escolha uma opção de 0 a 5.")
        
        # Pausa antes de voltar ao menu
        input("\nPressione ENTER para continuar...")


if __name__ == "__main__":
    main()
