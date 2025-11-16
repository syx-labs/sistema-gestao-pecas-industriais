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
from services import database
from models.peca import criar_peca


# Configuração da página
st.set_page_config(
    page_title="Sistema de Gestão de Peças",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)


def aplicar_estilos_customizados() -> None:
    """Aplica CSS customizado para melhorar o design."""
    st.markdown("""
    <style>
        /* Estilos gerais */
        .main {
            padding-top: 2rem;
        }
        
        /* Cards de métricas mais bonitos */
        [data-testid="stMetricValue"] {
            font-size: 2rem;
            font-weight: 700;
        }
        
        [data-testid="stMetricDelta"] {
            font-size: 1rem;
        }
        
        /* Botões mais estilosos */
        .stButton > button {
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.3s ease;
            border: none;
            padding: 0.5rem 2rem;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(76, 175, 80, 0.4);
        }
        
        /* Inputs mais modernos */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stSelectbox > div > div > select {
            border-radius: 8px;
            border: 2px solid rgba(76, 175, 80, 0.3);
            transition: all 0.3s ease;
        }
        
        .stTextInput > div > div > input:focus,
        .stNumberInput > div > div > input:focus,
        .stSelectbox > div > div > select:focus {
            border-color: #4CAF50;
            box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
        }
        
        /* Tabs mais bonitas */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        
        .stTabs [data-baseweb="tab"] {
            border-radius: 8px 8px 0 0;
            padding: 10px 20px;
            font-weight: 600;
        }
        
        /* Expanders com animação */
        .streamlit-expanderHeader {
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .streamlit-expanderHeader:hover {
            background-color: rgba(76, 175, 80, 0.1);
        }
        
        /* Progress bar mais bonita */
        .stProgress > div > div > div > div {
            background: linear-gradient(90deg, #4CAF50 0%, #45a049 100%);
        }
        
        /* Dataframe estilizado */
        [data-testid="stDataFrame"] {
            border-radius: 8px;
            overflow: hidden;
        }
        
        /* Dividers mais sutis */
        hr {
            margin: 2rem 0;
            border: none;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(76, 175, 80, 0.3), transparent);
        }
        
        /* Sidebar com sombra */
        [data-testid="stSidebar"] {
            box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1);
        }
        
        /* Animação suave nos containers */
        .element-container {
            animation: fadeIn 0.3s ease-in;
        }
        
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        /* Cards customizados */
        .custom-card {
            background: rgba(76, 175, 80, 0.05);
            border-left: 4px solid #4CAF50;
            padding: 1.5rem;
            border-radius: 8px;
            margin: 1rem 0;
            transition: all 0.3s ease;
        }
        
        .custom-card:hover {
            transform: translateX(4px);
            box-shadow: 0 4px 12px rgba(76, 175, 80, 0.2);
        }
        
        /* Header gradiente */
        .gradient-header {
            background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
            padding: 2rem;
            border-radius: 12px;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 4px 16px rgba(76, 175, 80, 0.3);
        }
        
        .gradient-header h1 {
            color: white;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
        }
        
        .gradient-header p {
            color: rgba(255, 255, 255, 0.9);
            margin: 0.5rem 0 0 0;
        }
    </style>
    """, unsafe_allow_html=True)


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
        marker_colors=['#4CAF50', '#f44336'],
        hole=0.5,
        textinfo='label+percent',
        textfont_size=14,
        pull=[0.05, 0]
    )])
    
    fig.update_layout(
        title_text="<b>Taxa de Aprovação</b>",
        title_font_size=20,
        height=400,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#FAFAFA', size=12)
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
    
    # Cores gradientes para cada barra
    cores = ['#ff6b6b', '#ffa502', '#ff6348']
    
    fig = go.Figure(data=[
        go.Bar(
            x=motivos,
            y=valores,
            marker=dict(
                color=cores,
                line=dict(color='rgba(255,255,255,0.2)', width=2)
            ),
            text=valores,
            textposition='outside',
            textfont=dict(size=14, color='#FAFAFA')
        )
    ])
    
    fig.update_layout(
        title_text="<b>Motivos de Reprovação</b>",
        title_font_size=20,
        xaxis_title="<b>Motivo</b>",
        yaxis_title="<b>Quantidade</b>",
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#FAFAFA', size=12),
        xaxis=dict(
            showgrid=False,
            showline=True,
            linecolor='rgba(255,255,255,0.2)'
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(255,255,255,0.1)',
            showline=True,
            linecolor='rgba(255,255,255,0.2)'
        )
    )
    
    return fig


def criar_grafico_distribuicao_peso(sistema: SistemaArmazenamento) -> go.Figure:
    """Cria histograma de distribuição de peso das peças."""
    todas_pecas = sistema['pecas_aprovadas'] + sistema['pecas_reprovadas']
    
    if len(todas_pecas) == 0:
        return None
    
    pesos = [peca['peso'] for peca in todas_pecas]
    
    fig = go.Figure()
    
    # Adiciona histograma com gradiente
    fig.add_trace(go.Histogram(
        x=pesos,
        nbinsx=20,
        name='Distribuição de Peso',
        marker=dict(
            color='#4CAF50',
            line=dict(color='rgba(255,255,255,0.2)', width=1),
            opacity=0.8
        ),
        hovertemplate='<b>Peso:</b> %{x}g<br><b>Quantidade:</b> %{y}<extra></extra>'
    ))
    
    # Adiciona linhas de limite com estilo melhorado
    fig.add_vline(
        x=PESO_MINIMO, 
        line_dash="dash", 
        line_color="#4CAF50", 
        line_width=2,
        annotation_text=f"Mín: {PESO_MINIMO}g",
        annotation_position="top",
        annotation=dict(font_size=12, font_color='#4CAF50')
    )
    fig.add_vline(
        x=PESO_MAXIMO, 
        line_dash="dash", 
        line_color="#4CAF50",
        line_width=2,
        annotation_text=f"Máx: {PESO_MAXIMO}g",
        annotation_position="top",
        annotation=dict(font_size=12, font_color='#4CAF50')
    )
    
    fig.update_layout(
        title_text="<b>Distribuição de Peso das Peças</b>",
        title_font_size=20,
        xaxis_title="<b>Peso (g)</b>",
        yaxis_title="<b>Quantidade</b>",
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#FAFAFA', size=12),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(255,255,255,0.1)',
            showline=True,
            linecolor='rgba(255,255,255,0.2)'
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(255,255,255,0.1)',
            showline=True,
            linecolor='rgba(255,255,255,0.2)'
        ),
        bargap=0.1
    )
    
    return fig


def pagina_cadastro() -> None:
    """Interface de cadastro de novas peças."""
    st.markdown("## 📝 Cadastro de Peças")
    st.markdown("*Registre novas peças para controle de qualidade automático*")
    
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
        
        submitted = st.form_submit_button("✅ Cadastrar Peça", width='stretch')
        
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
                # Sincroniza com o banco de dados
                database.sincronizar_sistema(sistema)
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
    st.markdown("## 📊 Dashboard de Visualização")
    st.markdown("*Acompanhe em tempo real as métricas de qualidade da produção*")
    
    sistema = st.session_state.sistema
    
    # Métricas principais
    exibir_metricas_principais(sistema)
    
    st.divider()
    
    # Gráficos em cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='custom-card'>
            <h3 style='margin-top: 0;'>🎯 Taxa de Aprovação</h3>
        </div>
        """, unsafe_allow_html=True)
        
        grafico_aprovacao = criar_grafico_aprovacao(sistema)
        if grafico_aprovacao:
            st.plotly_chart(grafico_aprovacao, use_container_width=True, key='grafico_aprovacao')
        else:
            st.info("📊 Nenhuma peça cadastrada ainda")
    
    with col2:
        st.markdown("""
        <div class='custom-card'>
            <h3 style='margin-top: 0;'>⚠️ Análise de Reprovações</h3>
        </div>
        """, unsafe_allow_html=True)
        
        grafico_motivos = criar_grafico_motivos_reprovacao(sistema)
        if grafico_motivos:
            st.plotly_chart(grafico_motivos, use_container_width=True, key='grafico_motivos')
        else:
            st.info("📊 Nenhuma peça reprovada ainda")
    
    # Distribuição de peso em card separado
    st.divider()
    
    st.markdown("""
    <div class='custom-card'>
        <h3 style='margin-top: 0;'>⚖️ Distribuição de Peso</h3>
    </div>
    """, unsafe_allow_html=True)
    
    grafico_peso = criar_grafico_distribuicao_peso(sistema)
    if grafico_peso:
        st.plotly_chart(grafico_peso, use_container_width=True, key='grafico_peso')
    else:
        st.info("📊 Nenhuma peça cadastrada ainda")


def pagina_pecas() -> None:
    """Interface de listagem de peças."""
    st.markdown("## 📋 Listagem de Peças")
    st.markdown("*Visualize todas as peças processadas pelo sistema*")
    
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
                width='stretch',
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
    st.markdown("## 📦 Gerenciamento de Caixas")
    st.markdown("*Acompanhe o empacotamento e status das caixas de produção*")
    
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
    st.markdown("## 📈 Relatório Completo")
    st.markdown("*Análise detalhada de todas as métricas e indicadores de produção*")
    
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
    
    # Aplica estilos customizados
    aplicar_estilos_customizados()
    
    # Inicializa o estado
    inicializar_session_state()
    
    # Título principal com design moderno
    st.markdown("""
    <div class='gradient-header'>
        <h1>🏭 Sistema de Gestão de Peças Industriais</h1>
        <p>Automação Digital para Controle de Qualidade e Produtividade</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar com menu
    with st.sidebar:
        # Cabeçalho visual da sidebar
        st.markdown("""
        <div style='background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%); 
                    padding: 25px; 
                    border-radius: 12px; 
                    text-align: center;
                    margin-bottom: 20px;
                    box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);'>
            <h2 style='color: white; margin: 0; font-size: 28px; font-weight: 700;'>🏭 QUALIDADE</h2>
            <p style='color: white; margin: 8px 0 0 0; font-size: 15px; opacity: 0.95;'>
                Controle de Produção Industrial
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
        
        # Card estilizado para critérios
        st.markdown("""
        <div style='background: rgba(76, 175, 80, 0.1); 
                    padding: 15px; 
                    border-radius: 8px; 
                    border-left: 4px solid #4CAF50;
                    margin: 10px 0;'>
            <p style='margin: 5px 0;'><strong>⚖️ Peso:</strong><br>{} - {}g</p>
            <p style='margin: 5px 0;'><strong>🎨 Cores:</strong><br>{}</p>
            <p style='margin: 5px 0;'><strong>📏 Comprimento:</strong><br>{} - {}cm</p>
        </div>
        """.format(
            PESO_MINIMO, PESO_MAXIMO,
            ', '.join(CORES_ACEITAS),
            COMPRIMENTO_MINIMO, COMPRIMENTO_MAXIMO
        ), unsafe_allow_html=True)
        
        st.markdown("---")
        
        if st.button("🔄 Recarregar Dados do Banco", type="primary", width='stretch'):
            # Recarrega dados do banco de dados
            st.session_state.sistema = database.carregar_sistema_completo()
            st.success("✅ Dados recarregados do banco de dados!")
            st.rerun()
        
        if st.button("🗑️ Resetar Sistema", type="secondary", width='stretch'):
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
