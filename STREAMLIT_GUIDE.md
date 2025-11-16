# 🎨 Guia da Interface Visual (Streamlit)

## 📖 Visão Geral

A interface visual do Sistema de Gestão de Peças foi desenvolvida com **Streamlit**, oferecendo uma experiência moderna e interativa para gerenciar a produção de peças industriais.

## 🚀 Como Executar

### Método 1: Usando o script
```bash
./run_visual.sh
```

### Método 2: Comando direto
```bash
streamlit run streamlit_app.py
```

### Método 3: Com Bun
```bash
bun run streamlit run streamlit_app.py
```

A aplicação abrirá automaticamente em `http://localhost:8501`

## 🎯 Funcionalidades

### 1. 📝 Cadastrar Peça

Interface amigável para cadastrar novas peças com:

- **ID da Peça**: Campo de texto para identificador único
- **Peso**: Slider numérico (0-500g) com faixa aceita destacada
- **Cor**: Dropdown com cores disponíveis
- **Comprimento**: Slider numérico (0-100cm) com faixa aceita destacada

**Validação em Tempo Real:**
- ✅ Peças aprovadas são automaticamente adicionadas às caixas
- ❌ Peças reprovadas mostram motivos detalhados
- 🎈 Animação especial quando uma caixa é fechada

### 2. 📊 Dashboard

Painel com visualizações em tempo real:

**Métricas Principais:**
- Total de peças processadas
- Peças aprovadas (com taxa de aprovação)
- Peças reprovadas (com taxa de reprovação)
- Caixas fechadas (com progresso da caixa atual)

**Gráficos Interativos:**

#### Gráfico de Pizza - Taxa de Aprovação
- Visualização rápida da proporção aprovadas/reprovadas
- Cores: Verde (aprovadas) e Vermelho (reprovadas)
- Design tipo "donut" moderno

#### Gráfico de Barras - Motivos de Reprovação
- Mostra quantas peças foram reprovadas por cada motivo:
  - Peso inadequado
  - Cor inadequada
  - Comprimento inadequado
- Cores distintas para cada categoria

#### Histograma - Distribuição de Peso
- Mostra a distribuição de pesos de todas as peças
- Linhas tracejadas indicam limites mínimo e máximo aceitos
- Identifica facilmente padrões de produção

### 3. 📋 Listar Peças

Visualização organizada em abas:

**Aba "Aprovadas":**
- Tabela interativa com todas as peças aprovadas
- Colunas: ID, Peso, Cor, Comprimento
- Ordenação e filtros disponíveis

**Aba "Reprovadas":**
- Lista expansível de peças reprovadas
- Cada item mostra:
  - Informações completas da peça
  - Motivos detalhados da reprovação
- Código de cor visual (🔴) para identificação rápida

### 4. 📦 Caixas

Gerenciamento visual das caixas de armazenamento:

**Caixa em Preenchimento:**
- Barra de progresso mostrando quantas peças já foram adicionadas
- Lista expansível com todas as peças da caixa atual
- Atualização em tempo real

**Caixas Fechadas:**
- Lista de todas as caixas completadas
- Cada caixa pode ser expandida para ver seu conteúdo
- Histórico completo de armazenamento

### 5. 📈 Relatório

Relatório consolidado com análises completas:

**Resumo Geral:**
- Total de peças processadas
- Taxa de aprovação percentual
- Taxa de reprovação percentual

**Status de Armazenamento:**
- Quantidade de caixas fechadas
- Status da caixa em preenchimento

**Análise de Reprovações:**
- Estatísticas detalhadas por motivo
- Métricas individuais para cada critério

## 🎨 Design e UX

### Paleta de Cores

- **Primária**: `#4CAF50` (Verde) - Sucesso e aprovação
- **Fundo**: `#FFFFFF` (Branco) - Clareza e limpeza
- **Fundo Secundário**: `#F5F7FA` (Cinza claro) - Separação visual
- **Texto**: `#262730` (Cinza escuro) - Legibilidade

### Ícones e Emojis

O sistema usa emojis para comunicação visual rápida:

- 🏭 Sistema/Indústria
- 📝 Cadastro
- 📊 Dashboard/Gráficos
- 📋 Listagem
- 📦 Caixas/Armazenamento
- 📈 Relatórios
- ✅ Aprovado
- ❌ Reprovado
- ⚙️ Configurações

### Layout Responsivo

- **Sidebar**: Menu de navegação sempre visível
- **Wide Mode**: Aproveitamento máximo da largura da tela
- **Grid System**: Colunas flexíveis para diferentes resoluções

## 🔧 Recursos Técnicos

### Bibliotecas Utilizadas

```python
streamlit >= 1.28.0    # Framework web interativo
plotly >= 5.17.0       # Gráficos interativos
pandas >= 2.0.0        # Manipulação de dados
```

### Gerenciamento de Estado

O Streamlit usa `st.session_state` para manter:
- Estado do sistema de armazenamento
- Histórico de cadastros
- Dados persistentes entre interações

### Performance

- **Caching**: Funções otimizadas para reuso
- **Lazy Loading**: Gráficos carregam apenas quando necessário
- **Estado Persistente**: Dados mantidos durante a sessão

## 🎓 Dicas de Uso

### Para Demonstrações

1. Inicie com o Dashboard para mostrar as métricas
2. Cadastre algumas peças (aprovadas e reprovadas)
3. Volte ao Dashboard para ver gráficos atualizando
4. Mostre as caixas sendo preenchidas
5. Finalize com o relatório completo

### Para Testes

1. Use o botão "🔄 Resetar Sistema" na sidebar para limpar dados
2. Teste casos extremos (peças nos limites de tolerância)
3. Cadastre 10 peças aprovadas para ver uma caixa fechar
4. Mix de aprovadas/reprovadas para visualizar gráficos diversos

### Atalhos

- **R**: Recarregar aplicação
- **Ctrl/Cmd + R**: Recarregar página do navegador
- **Ctrl/Cmd + W**: Fechar aba

## 📊 Comparação: CLI vs Streamlit

| Aspecto | Terminal (CLI) | Streamlit |
|---------|---------------|-----------|
| Interface | Texto | Visual/Gráfica |
| Gráficos | Não | Sim, interativos |
| Métricas | Texto simples | Cards e indicadores |
| UX | Comandos | Cliques e forms |
| Curva de Aprendizado | Baixa | Muito baixa |
| Exportação | Texto | Screenshots/PDF |
| Histórico | Limitado | Visual completo |

## 🚨 Solução de Problemas

### Porta já em uso

```bash
# Se a porta 8501 estiver ocupada
streamlit run streamlit_app.py --server.port 8502
```

### Erro de importação

```bash
# Reinstale as dependências
pip3 install -r requirements.txt --force-reinstall
```

### Browser não abre automaticamente

```bash
# Desabilite auto-open e acesse manualmente
streamlit run streamlit_app.py --server.headless=true
# Depois abra: http://localhost:8501
```

### Gráficos não carregam

- Verifique se plotly está instalado: `pip3 show plotly`
- Limpe o cache: Ctrl+C e reinicie a aplicação
- Use o botão de recarregar no canto superior direito

## 🎯 Próximos Passos

Possíveis melhorias futuras:

- 📥 Exportação de relatórios em PDF
- 📊 Gráficos de linha mostrando produção ao longo do tempo
- 🔔 Alertas quando taxa de reprovação ultrapassar threshold
- 📱 Layout mobile-first
- 🌙 Modo escuro
- 🌍 Internacionalização (i18n)
- 💾 Persistência de dados em banco de dados
- 📊 Dashboard de comparação entre períodos

## 📝 Observações

- O sistema funciona completamente offline (exceto placeholder de imagem)
- Dados são mantidos apenas na sessão (não há persistência entre reinicializações)
- Ideal para demonstrações e protótipos
- Performance otimizada para até 10.000 peças cadastradas

---

**Desenvolvido com ☕ e 💻 por Gabriel Falcão**

*"Dados visuais contam histórias que números não conseguem."*
