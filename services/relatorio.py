"""
Serviço de geração de relatórios consolidados.
"""

from typing import Dict
from services.armazenamento import SistemaArmazenamento


def gerar_relatorio_completo(sistema: SistemaArmazenamento) -> str:
    """
    Gera um relatório consolidado com todas as estatísticas do sistema.
    
    Inclui:
    - Total de peças processadas (aprovadas + reprovadas)
    - Total e percentual de peças aprovadas
    - Total e percentual de peças reprovadas
    - Quantidade de caixas fechadas
    - Status da caixa em preenchimento
    - Detalhamento de reprovações por critério
    
    Args:
        sistema: Estado atual do sistema
    
    Returns:
        String formatada com o relatório completo
    """
    total_aprovadas = len(sistema['pecas_aprovadas'])
    total_reprovadas = len(sistema['pecas_reprovadas'])
    total_processadas = total_aprovadas + total_reprovadas
    
    # Calcula percentuais
    if total_processadas > 0:
        percentual_aprovadas = (total_aprovadas / total_processadas) * 100
        percentual_reprovadas = (total_reprovadas / total_processadas) * 100
    else:
        percentual_aprovadas = 0.0
        percentual_reprovadas = 0.0
    
    # Contabiliza caixas
    total_caixas_fechadas = len(sistema['caixas_fechadas'])
    pecas_caixa_atual = len(sistema['caixa_atual']['pecas'])
    
    # Analisa motivos de reprovação
    contadores_motivos = analisar_motivos_reprovacao(sistema['pecas_reprovadas'])
    
    # Formata relatório
    relatorio = []
    relatorio.append("=" * 40)
    relatorio.append("RELATÓRIO FINAL".center(40))
    relatorio.append("=" * 40)
    relatorio.append("")
    
    relatorio.append("📊 RESUMO GERAL:")
    relatorio.append(f"  Total de peças processadas: {total_processadas}")
    relatorio.append(f"  ✅ Peças aprovadas: {total_aprovadas} ({percentual_aprovadas:.1f}%)")
    relatorio.append(f"  ❌ Peças reprovadas: {total_reprovadas} ({percentual_reprovadas:.1f}%)")
    relatorio.append("")
    
    relatorio.append("📦 ARMAZENAMENTO:")
    relatorio.append(f"  Caixas fechadas: {total_caixas_fechadas}")
    if pecas_caixa_atual > 0:
        relatorio.append(f"  Caixa em preenchimento: 1 ({pecas_caixa_atual}/10 peças)")
    else:
        relatorio.append("  Caixa em preenchimento: vazia")
    relatorio.append("")
    
    if total_reprovadas > 0:
        relatorio.append("❌ DETALHAMENTO DE REPROVAÇÕES:")
        relatorio.append(f"  Por peso inadequado: {contadores_motivos['peso']} peças")
        relatorio.append(f"  Por cor inadequada: {contadores_motivos['cor']} peças")
        relatorio.append(f"  Por comprimento inadequado: {contadores_motivos['comprimento']} peças")
        relatorio.append("")
    
    relatorio.append("=" * 40)
    
    return "\n".join(relatorio)


def analisar_motivos_reprovacao(pecas_reprovadas: list) -> Dict[str, int]:
    """
    Analisa e contabiliza os motivos de reprovação por critério.
    
    Args:
        pecas_reprovadas: Lista de peças reprovadas
    
    Returns:
        Dicionário com contadores por tipo de motivo
    """
    contadores = {
        'peso': 0,
        'cor': 0,
        'comprimento': 0
    }
    
    for peca in pecas_reprovadas:
        for motivo in peca['motivos_reprovacao']:
            motivo_lower = motivo.lower()
            if 'peso' in motivo_lower:
                contadores['peso'] += 1
            elif 'cor' in motivo_lower:
                contadores['cor'] += 1
            elif 'comprimento' in motivo_lower:
                contadores['comprimento'] += 1
    
    return contadores
