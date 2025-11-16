#!/usr/bin/env python3
"""
Script de demonstração da persistência SQLite.
Execute este script múltiplas vezes para ver os dados persistindo.

Autor: Gabriel Falcão
Data: 2025-11-16
"""

from services.armazenamento import inicializar_sistema, adicionar_peca_em_caixa
from models.peca import criar_peca
from services.validacao import validar_peca


def main():
    print("=" * 60)
    print("TESTE DE PERSISTÊNCIA - SISTEMA DE GESTÃO DE PEÇAS".center(60))
    print("=" * 60)
    print()
    
    # Inicializa sistema (carrega do banco se existir)
    sistema = inicializar_sistema()
    
    print(f"📊 Estado atual do sistema:")
    print(f"   • Peças aprovadas: {len(sistema['pecas_aprovadas'])}")
    print(f"   • Peças reprovadas: {len(sistema['pecas_reprovadas'])}")
    print(f"   • Caixas fechadas: {len(sistema['caixas_fechadas'])}")
    print(f"   • Peças na caixa atual: {len(sistema['caixa_atual']['pecas'])}/{10}")
    print(f"   • Próxima caixa: #{sistema['contador_caixas']}")
    print()
    
    # Adiciona 3 peças aprovadas
    print("➕ Adicionando 3 peças aprovadas...")
    base_id = len(sistema['pecas_aprovadas'])
    for i in range(3):
        peca = criar_peca(
            f"P{base_id + i:03d}",
            100.0,
            "azul" if i % 2 == 0 else "verde",
            15.0,
            True
        )
        caixa_fechada, msg = adicionar_peca_em_caixa(peca, sistema)
        print(f"   ✓ {msg}")
        if caixa_fechada:
            print()
    
    # Adiciona 1 peça reprovada
    print()
    print("➕ Adicionando 1 peça reprovada...")
    peca_reprovada = criar_peca(
        f"P{base_id + 3:03d}",
        120.0,
        "vermelho",
        25.0
    )
    aprovada, motivos = validar_peca(peca_reprovada)
    peca_reprovada['aprovada'] = aprovada
    peca_reprovada['motivos_reprovacao'] = motivos
    sistema['pecas_reprovadas'].append(peca_reprovada)
    
    # Sincroniza manualmente (normalmente automático)
    from services import database
    database.sincronizar_sistema(sistema)
    
    print(f"   ✗ Peça {peca_reprovada['id']} reprovada")
    for motivo in motivos:
        print(f"     - {motivo}")
    
    print()
    print(f"📊 Estado final:")
    print(f"   • Peças aprovadas: {len(sistema['pecas_aprovadas'])}")
    print(f"   • Peças reprovadas: {len(sistema['pecas_reprovadas'])}")
    print(f"   • Caixas fechadas: {len(sistema['caixas_fechadas'])}")
    print(f"   • Peças na caixa atual: {len(sistema['caixa_atual']['pecas'])}/{10}")
    print()
    print("💾 Dados salvos no banco: sistema_pecas.db")
    print("🔄 Execute este script novamente para ver a persistência!")
    print()


if __name__ == "__main__":
    main()

