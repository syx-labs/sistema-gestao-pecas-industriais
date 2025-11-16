#!/usr/bin/env python3
"""
Script de teste para validar sincronização entre CLI e Streamlit via banco de dados.
"""

from services.armazenamento import inicializar_sistema, adicionar_peca_em_caixa
from services.validacao import validar_peca
from services.database import carregar_sistema_completo, sincronizar_sistema
from models.peca import criar_peca

def test_cadastrar_peca_reprovada():
    """Testa cadastro de peça reprovada via código (simulando CLI)."""
    print("=" * 70)
    print("TESTE 1: Cadastrar peça reprovada via código (simulando CLI)")
    print("=" * 70)
    
    # Inicializa sistema
    sistema = inicializar_sistema()
    
    # Cria peça reprovada (peso muito baixo)
    peca_reprovada = criar_peca(
        id_peca="P002",
        peso=50.0,  # Abaixo do mínimo (80g)
        cor="azul",
        comprimento=15.0
    )
    
    # Valida
    aprovada, motivos = validar_peca(peca_reprovada)
    peca_reprovada['aprovada'] = aprovada
    peca_reprovada['motivos_reprovacao'] = motivos
    
    # Adiciona ao sistema
    if not aprovada:
        sistema['pecas_reprovadas'].append(peca_reprovada)
        sincronizar_sistema(sistema)
        print(f"✅ Peça {peca_reprovada['id']} REPROVADA cadastrada!")
        print(f"   Motivos: {motivos}")
    
    return peca_reprovada


def test_cadastrar_peca_aprovada():
    """Testa cadastro de peça aprovada via código (simulando CLI)."""
    print("\n" + "=" * 70)
    print("TESTE 2: Cadastrar peça aprovada via código (simulando CLI)")
    print("=" * 70)
    
    # Inicializa sistema
    sistema = inicializar_sistema()
    
    # Cria peça aprovada
    peca_aprovada = criar_peca(
        id_peca="P003",
        peso=100.0,
        cor="verde",
        comprimento=15.0
    )
    
    # Valida
    aprovada, motivos = validar_peca(peca_aprovada)
    peca_aprovada['aprovada'] = aprovada
    peca_aprovada['motivos_reprovacao'] = motivos
    
    # Adiciona ao sistema
    if aprovada:
        caixa_fechada, mensagem = adicionar_peca_em_caixa(peca_aprovada, sistema)
        print(f"✅ Peça {peca_aprovada['id']} APROVADA cadastrada!")
        print(f"   {mensagem}")
    
    return peca_aprovada


def test_recarregar_do_banco():
    """Testa se é possível recarregar dados do banco."""
    print("\n" + "=" * 70)
    print("TESTE 3: Recarregar dados do banco (simulando Streamlit)")
    print("=" * 70)
    
    # Recarrega do banco
    sistema = carregar_sistema_completo()
    
    print(f"\n📊 Estatísticas do banco de dados:")
    print(f"   - Peças aprovadas: {len(sistema['pecas_aprovadas'])}")
    print(f"   - Peças reprovadas: {len(sistema['pecas_reprovadas'])}")
    print(f"   - Caixas fechadas: {len(sistema['caixas_fechadas'])}")
    print(f"   - Caixa atual: {len(sistema['caixa_atual']['pecas'])} peças")
    
    print(f"\n✅ Peças Aprovadas:")
    for peca in sistema['pecas_aprovadas']:
        print(f"   - {peca['id']}: {peca['peso']}g, {peca['cor']}, {peca['comprimento']}cm")
    
    print(f"\n❌ Peças Reprovadas:")
    for peca in sistema['pecas_reprovadas']:
        print(f"   - {peca['id']}: {peca['peso']}g, {peca['cor']}, {peca['comprimento']}cm")
        print(f"      Motivos: {', '.join(peca['motivos_reprovacao'])}")
    
    return sistema


def main():
    """Executa todos os testes."""
    print("\n🧪 INICIANDO TESTES DE SINCRONIZAÇÃO\n")
    
    # Teste 1: Cadastrar peça reprovada
    peca_reprovada = test_cadastrar_peca_reprovada()
    
    # Teste 2: Cadastrar peça aprovada
    peca_aprovada = test_cadastrar_peca_aprovada()
    
    # Teste 3: Recarregar do banco
    sistema_recarregado = test_recarregar_do_banco()
    
    # Validações
    print("\n" + "=" * 70)
    print("VALIDAÇÃO FINAL")
    print("=" * 70)
    
    sucesso = True
    
    # Verifica se P002 (reprovada) está no sistema recarregado
    ids_reprovadas = [p['id'] for p in sistema_recarregado['pecas_reprovadas']]
    if 'P002' in ids_reprovadas:
        print("✅ P002 (reprovada) encontrada no sistema recarregado")
    else:
        print("❌ P002 (reprovada) NÃO encontrada no sistema recarregado")
        sucesso = False
    
    # Verifica se P003 (aprovada) está no sistema recarregado
    ids_aprovadas = [p['id'] for p in sistema_recarregado['pecas_aprovadas']]
    if 'P003' in ids_aprovadas:
        print("✅ P003 (aprovada) encontrada no sistema recarregado")
    else:
        print("❌ P003 (aprovada) NÃO encontrada no sistema recarregado")
        sucesso = False
    
    # Verifica se P001 (do teste anterior) ainda está lá
    if 'P001' in ids_aprovadas:
        print("✅ P001 (aprovada anterior) ainda presente no sistema")
    else:
        print("⚠️  P001 (aprovada anterior) não encontrada")
    
    print("\n" + "=" * 70)
    if sucesso:
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("\nPróximos passos:")
        print("1. Abra o Streamlit: streamlit run streamlit_app.py")
        print("2. Clique no botão '🔄 Recarregar Dados do Banco'")
        print("3. Verifique se as peças P001, P002 e P003 aparecem corretamente")
    else:
        print("❌ ALGUNS TESTES FALHARAM")
    print("=" * 70)


if __name__ == "__main__":
    main()

