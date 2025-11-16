#!/usr/bin/env python3
"""
Interface Visual do Sistema de Automação Digital para Gestão de Peças Industriais

Desenvolvido para automatizar o controle de produção e qualidade de peças
fabricadas em linha de montagem com visualização em tempo real.

Autor: Gabriel Falcão
Data: 2025-11-15
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Dict, List

from services.armazenamento import (
    inicializar_sistema,
    adicionar_peca_em_caixa,
    remover_peca_por_id,
    SistemaArmazenamento
)
from services.validacao import (
    validar_peca,
    PESO_MINIMO,
    PESO_MAXIMO,
    CORES_ACEITAS,
    COMPRIMENTO_MINIMO,
    COMPRIMENTO_MAXIMO
)
from services.relatorio import gerar_estatisticas_reprovacao
from models.peca import criar_peca


# Configuração da página
st.set_page_config(
    page_title="Sistema de Gestão de Peças",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)


def inicializar_session_state() -> None:
    """Inicializa o estado da sessão do Streamlit."""
    if 'sistema' not in st.session_state:
        st.session_state.sistema = inicializar_sistema()
    if 'historico_cadastros' not in st.session_state:
        st.session_state.historico_cadastros = []


def exibir_metricas_principais(sistema: SistemaArmazenamento) -> None:
    """Exibe as métricas principais do sistema em cards."""
    total_pecas = len(sistema['pecas_aprovadas']) + len(sistema['pecas_reprovadas'])
    total_aprovadas = len(sistema['pecas_aprovadas'])
    total_reprovadas = len(sistema['pecas_reprovadas'])
    
    taxa_aprovacao = (total_aprovadas / total_pecas * 100) if total_pecas > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📊 Total de Peças",
            value=total_pecas,
            delta=None
        )
    
    with col2:
        st.metric(
            label="✅ Peças Aprovadas",
            value=total_aprovadas,
            delta=f"{taxa_aprovacao:.1f}%"
        )
    
    with col3:
        st.metric(
            label="❌ Peças Reprovadas",
            value=total_reprovadas,
            delta=f"{100-taxa_aprovacao:.1f}%"
        )
    
    with col4:
        st.metric(
            label="📦 Caixas Fechadas",
            value=len(sistema['caixas_fechadas']),
            delta=f"{len(sistema['caixa_atual']['pecas'])}/10 em aberto"
        )


def criar_grafico_aprovacao(sistema: SistemaArmazenamento) -> go.Figure:
    """Cria gráfico de pizza para taxa de aprovação."""
    total_aprovadas = len(sistema['pecas_aprovadas'])
    total_reprovadas = len(sistema['pecas_reprovadas'])
    
    if total_aprovadas == 0 and total_reprovadas == 0:
        return None
    
    fig = go.Figure(data=[go.Pie(
        labels=['Aprovadas', 'Reprovadas'],
        values=[total_aprovadas, total_reprovadas],
        marker_colors=['#28a745', '#dc3545'],
        hole=0.4
    )])
    
    fig.update_layout(
        title_text="Taxa de Aprovação",
        height=400,
        showlegend=True
    )
    
    return fig


def criar_grafico_motivos_reprovacao(sistema: SistemaArmazenamento) -> go.Figure:
    """Cria gráfico de barras para motivos de reprovação."""
    if len(sistema['pecas_reprovadas']) == 0:
        return None
    
    stats = gerar_estatisticas_reprovacao(sistema['pecas_reprovadas'])
    
    motivos = ['Peso Inadequado', 'Cor Inadequada', 'Comprimento Inadequado']
    valores = [
        stats['peso_inadequado'],
        stats['cor_inadequada'],
        stats['comprimento_inadequado']
    ]
    
    fig = go.Figure(data=[
        go.Bar(
            x=motivos,
            y=valores,
            marker_color=['#ff6b6b', '#4ecdc4', '#ffe66d']
        )
    ])
    
    fig.update_layout(
        title_text="Motivos de Reprovação",
        xaxis_title="Motivo",
        yaxis_title="Quantidade de Peças",
        height=400
    )
    
    return fig


def criar_grafico_distribuicao_peso(sistema: SistemaArmazenamento) -> go.Figure:
    """Cria histograma de distribuição de peso das peças."""
    todas_pecas = sistema['pecas_aprovadas'] + sistema['pecas_reprovadas']
    
    if len(todas_pecas) == 0:
        return None
    
    pesos = [peca['peso'] for peca in todas_pecas]
    cores_status = ['green' if peca['aprovada'] else 'red' for peca in todas_pecas]
    
    fig = go.Figure()
    
    # Adiciona histograma
    fig.add_trace(go.Histogram(
        x=pesos,
        nbinsx=20,
        name='Distribuição de Peso',
        marker_color='lightblue'
    ))
    
    # Adiciona linhas de limite
    fig.add_vline(x=PESO_MINIMO, line_dash="dash", line_color="green", 
                  annotation_text=f"Mín: {PESO_MINIMO}g")
    fig.add_vline(x=PESO_MAXIMO, line_dash="dash", line_color="green",
                  annotation_text=f"Máx: {PESO_MAXIMO}g")
    
    fig.update_layout(
        title_text="Distribuição de Peso das Peças",
        xaxis_title="Peso (g)",
        yaxis_title="Quantidade",
        height=400
    )
    
    return fig


def pagina_cadastro() -> None:
    """Interface de cadastro de novas peças."""
    st.header("📝 Cadastrar Nova Peça")
    
    with st.form("form_cadastro", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            id_peca = st.text_input(
                "ID da Peça",
                placeholder="Ex: P001",
                help="Identificador único da peça"
            )
            
            peso = st.number_input(
                f"Peso (g) - Faixa aceita: {PESO_MINIMO}g a {PESO_MAXIMO}g",
                min_value=0.0,
                max_value=500.0,
                value=100.0,
                step=0.1,
                format="%.1f"
            )
        
        with col2:
            cor = st.selectbox(
                "Cor",
                options=[''] + CORES_ACEITAS + ['vermelho', 'amarelo', 'preto'],
                help=f"Cores aceitas: {', '.join(CORES_ACEITAS)}"
            )
            
            comprimento = st.number_input(
                f"Comprimento (cm) - Faixa aceita: {COMPRIMENTO_MINIMO}cm a {COMPRIMENTO_MAXIMO}cm",
                min_value=0.0,
                max_value=100.0,
                value=15.0,
                step=0.1,
                format="%.1f"
            )
        
        submitted = st.form_submit_button("✅ Cadastrar Peça", use_container_width=True)
        
        if submitted:
            if not id_peca:
                st.error("❌ Por favor, informe o ID da peça!")
                return
            
            if not cor:
                st.error("❌ Por favor, selecione uma cor!")
                return
            
            # Verifica se ID já existe
            sistema = st.session_state.sistema
            todas_pecas = sistema['pecas_aprovadas'] + sistema['pecas_reprovadas']
            
            if any(p['id'] == id_peca for p in todas_pecas):
                st.error(f"❌ Já existe uma peça cadastrada com o ID '{id_peca}'!")
                return
            
            # Cria a peça
            peca = criar_peca(
                id_peca=id_peca,
                peso=peso,
                cor=cor,
                comprimento=comprimento
            )
            
            # Valida a peça
            aprovada, motivos = validar_peca(peca)
            peca['aprovada'] = aprovada
            peca['motivos_reprovacao'] = motivos
            
            # Processa o resultado
            if aprovada:
                caixa_fechada, mensagem = adicionar_peca_em_caixa(peca, sistema)
                st.success(f"✅ Peça {id_peca} APROVADA!")
                st.info(f"📦 {mensagem}")
                
                if caixa_fechada:
                    st.balloons()
            else:
                sistema['pecas_reprovadas'].append(peca)
                st.error(f"❌ Peça {id_peca} REPROVADA!")
                
                with st.expander("📋 Ver motivos da reprovação"):
                    for motivo in motivos:
                        st.write(f"• {motivo}")
            
            # Adiciona ao histórico
            st.session_state.historico_cadastros.append({
                'id': id_peca,
                'aprovada': aprovada,
                'timestamp': pd.Timestamp.now()
            })


def pagina_visualizacao() -> None:
    """Interface de visualização de dados e gráficos."""
    st.header("📊 Visualização de Dados")
    
    sistema = st.session_state.sistema
    
    # Métricas principais
    exibir_metricas_principais(sistema)
    
    st.divider()
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        grafico_aprovacao = criar_grafico_aprovacao(sistema)
        if grafico_aprovacao:
            st.plotly_chart(grafico_aprovacao, use_container_width=True)
        else:
            st.info("📊 Nenhuma peça cadastrada ainda")
    
    with col2:
        grafico_motivos = criar_grafico_motivos_reprovacao(sistema)
        if grafico_motivos:
            st.plotly_chart(grafico_motivos, use_container_width=True)
        else:
            st.info("📊 Nenhuma peça reprovada ainda")
    
    # Distribuição de peso
    st.divider()
    grafico_peso = criar_grafico_distribuicao_peso(sistema)
    if grafico_peso:
        st.plotly_chart(grafico_peso, use_container_width=True)
    else:
        st.info("📊 Nenhuma peça cadastrada ainda")


def pagina_pecas() -> None:
    """Interface de listagem de peças."""
    st.header("📋 Listagem de Peças")
    
    sistema = st.session_state.sistema
    
    tab1, tab2 = st.tabs(["✅ Aprovadas", "❌ Reprovadas"])
    
    with tab1:
        if len(sistema['pecas_aprovadas']) == 0:
            st.info("Nenhuma peça aprovada cadastrada")
        else:
            df_aprovadas = pd.DataFrame(sistema['pecas_aprovadas'])
            df_aprovadas = df_aprovadas[['id', 'peso', 'cor', 'comprimento']]
            
            st.dataframe(
                df_aprovadas,
                use_container_width=True,
                hide_index=True
            )
    
    with tab2:
        if len(sistema['pecas_reprovadas']) == 0:
            st.info("Nenhuma peça reprovada cadastrada")
        else:
            for peca in sistema['pecas_reprovadas']:
                with st.expander(f"🔴 {peca['id']} - {peca['cor']}"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Peso:** {peca['peso']}g")
                        st.write(f"**Cor:** {peca['cor']}")
                    
                    with col2:
                        st.write(f"**Comprimento:** {peca['comprimento']}cm")
                    
                    st.write("**Motivos de reprovação:**")
                    for motivo in peca['motivos_reprovacao']:
                        st.write(f"• {motivo}")


def pagina_caixas() -> None:
    """Interface de visualização de caixas."""
    st.header("📦 Gerenciamento de Caixas")
    
    sistema = st.session_state.sistema
    
    # Caixa atual
    st.subheader("🆕 Caixa em Preenchimento")
    
    caixa_atual = sistema['caixa_atual']
    total_pecas_atual = len(caixa_atual['pecas'])
    
    progress = total_pecas_atual / 10
    st.progress(progress, text=f"Caixa #{caixa_atual['id']}: {total_pecas_atual}/10 peças")
    
    if total_pecas_atual > 0:
        with st.expander(f"Ver peças na Caixa #{caixa_atual['id']}"):
            for peca in caixa_atual['pecas']:
                st.write(f"• {peca['id']} - {peca['peso']}g - {peca['cor']} - {peca['comprimento']}cm")
    
    st.divider()
    
    # Caixas fechadas
    st.subheader("✅ Caixas Fechadas")
    
    if len(sistema['caixas_fechadas']) == 0:
        st.info("Nenhuma caixa fechada ainda")
    else:
        for caixa in sistema['caixas_fechadas']:
            with st.expander(f"📦 Caixa #{caixa['id']} - {len(caixa['pecas'])} peças"):
                for peca in caixa['pecas']:
                    st.write(f"• {peca['id']} - {peca['peso']}g - {peca['cor']} - {peca['comprimento']}cm")


def pagina_relatorio() -> None:
    """Interface de relatório completo."""
    st.header("📈 Relatório Completo")
    
    sistema = st.session_state.sistema
    
    total_pecas = len(sistema['pecas_aprovadas']) + len(sistema['pecas_reprovadas'])
    total_aprovadas = len(sistema['pecas_aprovadas'])
    total_reprovadas = len(sistema['pecas_reprovadas'])
    
    if total_pecas == 0:
        st.info("Nenhuma peça cadastrada ainda. Cadastre peças para gerar relatórios.")
        return
    
    # Resumo geral
    st.subheader("📊 Resumo Geral")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Processado", total_pecas)
    
    with col2:
        taxa_aprovacao = (total_aprovadas / total_pecas * 100)
        st.metric("Taxa de Aprovação", f"{taxa_aprovacao:.1f}%")
    
    with col3:
        taxa_reprovacao = (total_reprovadas / total_pecas * 100)
        st.metric("Taxa de Reprovação", f"{taxa_reprovacao:.1f}%")
    
    st.divider()
    
    # Armazenamento
    st.subheader("📦 Status de Armazenamento")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Caixas Fechadas", len(sistema['caixas_fechadas']))
    
    with col2:
        pecas_caixa_atual = len(sistema['caixa_atual']['pecas'])
        st.metric("Caixa Atual", f"{pecas_caixa_atual}/10 peças")
    
    st.divider()
    
    # Estatísticas de reprovação
    if total_reprovadas > 0:
        st.subheader("❌ Análise de Reprovações")
        
        stats = gerar_estatisticas_reprovacao(sistema['pecas_reprovadas'])
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Por Peso", stats['peso_inadequado'])
        
        with col2:
            st.metric("Por Cor", stats['cor_inadequada'])
        
        with col3:
            st.metric("Por Comprimento", stats['comprimento_inadequado'])


def main() -> None:
    """Função principal da aplicação Streamlit."""
    
    # Inicializa o estado
    inicializar_session_state()
    
    # Título principal
    st.title("🏭 Sistema de Gestão de Peças Industriais")
    st.markdown("### Automação Digital para Controle de Qualidade")
    
    # Sidebar com menu
    with st.sidebar:
        # Cabeçalho visual da sidebar
        st.markdown("""
        <div style='background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%); 
                    padding: 20px; 
                    border-radius: 10px; 
                    text-align: center;
                    margin-bottom: 20px;'>
            <h2 style='color: white; margin: 0; font-size: 24px;'>🏭 QUALIDADE</h2>
            <p style='color: white; margin: 5px 0 0 0; font-size: 14px; opacity: 0.9;'>
                Controle de Produção
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        pagina = st.radio(
            "Navegação",
            options=[
                "📝 Cadastrar Peça",
                "📊 Dashboard",
                "📋 Listar Peças",
                "📦 Caixas",
                "📈 Relatório"
            ],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        st.markdown("### ⚙️ Critérios de Qualidade")
        st.markdown(f"""
        - **Peso:** {PESO_MINIMO}g - {PESO_MAXIMO}g
        - **Cores:** {', '.join(CORES_ACEITAS)}
        - **Comprimento:** {COMPRIMENTO_MINIMO}cm - {COMPRIMENTO_MAXIMO}cm
        """)
        
        st.markdown("---")
        
        if st.button("🔄 Resetar Sistema", type="secondary", use_container_width=True):
            st.session_state.sistema = inicializar_sistema()
            st.session_state.historico_cadastros = []
            st.success("Sistema resetado!")
            st.rerun()
    
    # Roteamento de páginas
    if pagina == "📝 Cadastrar Peça":
        pagina_cadastro()
    elif pagina == "📊 Dashboard":
        pagina_visualizacao()
    elif pagina == "📋 Listar Peças":
        pagina_pecas()
    elif pagina == "📦 Caixas":
        pagina_caixas()
    elif pagina == "📈 Relatório":
        pagina_relatorio()


if __name__ == "__main__":
    main()
