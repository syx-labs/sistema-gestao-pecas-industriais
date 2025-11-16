# 🏭 Sistema de Automação Digital para Gestão de Peças Industriais

> Desenvolvido por **Gabriel Falcão** como projeto acadêmico da disciplina de Algoritmos e Lógica de Programação

## 📖 Sobre o Projeto

Este sistema nasceu de um desafio real da indústria: **como automatizar o controle de qualidade de peças fabricadas?**

Atualmente, muitas empresas ainda dependem de inspeção manual, o que gera:
- ⏱️ Atrasos na produção
- ❌ Erros humanos na conferência
- 💰 Aumento de custos operacionais
- 📊 Dificuldade em rastrear dados

A solução? Um sistema Python que faz tudo isso automaticamente, em tempo real.

## 🎯 O Problema que Resolvi

Imagine uma linha de montagem produzindo centenas de peças por dia. Cada peça precisa ser:
1. Pesada (deve estar entre 95g e 105g)
2. Verificada a cor (apenas azul ou verde são aceitas)
3. Medida o comprimento (entre 10cm e 20cm)

Se **TODOS** os critérios forem atendidos → ✅ Aprovada  
Se **QUALQUER** critério falhar → ❌ Reprovada (com motivo registrado)

As peças aprovadas são organizadas em caixas de 10 unidades, que fecham automaticamente quando completas.

## 🚀 Como Funciona

### 💾 Persistência de Dados

O sistema agora possui **banco de dados SQLite** com sincronização automática! Todos os dados são salvos e carregados automaticamente entre execuções.

**Características:**
- ✅ Schema normalizado (3NF)
- ✅ Sincronização automática
- ✅ Dados persistem entre sessões
- ✅ Zero configuração necessária

📖 **Documentação completa:** [docs/DATABASE.md](docs/DATABASE.md)

### Menu Principal

```
===== SISTEMA DE GESTÃO DE PEÇAS =====
1. Cadastrar nova peça
2. Listar peças aprovadas/reprovadas
3. Remover peça cadastrada
4. Listar caixas fechadas
5. Gerar relatório final
0. Sair
======================================
```

### Exemplo Prático

**Cadastrando uma peça aprovada:**
```
ID da peça: P001
Peso (g): 100
Cor: azul
Comprimento (cm): 15

✅ Peça P001 APROVADA!
Adicionada à Caixa #1 (1/10 peças)
```

**Cadastrando uma peça reprovada:**
```
ID da peça: P002
Peso (g): 120
Cor: vermelho
Comprimento (cm): 25

❌ Peça P002 REPROVADA!
Motivos:
  - Peso fora do intervalo (95.0-105.0g): 120.0g
  - Cor inadequada (esperado: azul ou verde): vermelho
  - Comprimento fora do intervalo (10.0-20.0cm): 25.0cm
```

**Relatório consolidado:**
```
========================================
           RELATÓRIO FINAL
========================================

📊 RESUMO GERAL:
  Total de peças processadas: 25
  ✅ Peças aprovadas: 18 (72.0%)
  ❌ Peças reprovadas: 7 (28.0%)

📦 ARMAZENAMENTO:
  Caixas fechadas: 1
  Caixa em preenchimento: 1 (8/10 peças)

❌ DETALHAMENTO DE REPROVAÇÕES:
  Por peso inadequado: 3 peças
  Por cor inadequada: 5 peças
  Por comprimento inadequado: 2 peças

========================================
```

## 💻 Como Executar

### Pré-requisitos
- Python 3.8 ou superior
- Bun ou pip para instalar dependências

### Instalação

```bash
# Clone o repositório
git clone https://github.com/ogabrielfalcao/sistema-gestao-pecas-industriais.git
cd sistema-gestao-pecas-industriais

# Instale as dependências
bun install  # ou: pip install -r requirements.txt
```

### Modo Terminal (CLI)

Execute a versão original em linha de comando:

```bash
python3 main.py
```

### Modo Visual (Streamlit) ✨ **NOVO!**

Execute a interface visual moderna com gráficos e dashboards:

```bash
streamlit run streamlit_app.py
# ou
bun run streamlit run streamlit_app.py
```

A aplicação abrirá automaticamente no navegador em `http://localhost:8501`

#### Recursos da Interface Visual:

- 📊 **Dashboard em Tempo Real**: Visualize métricas e gráficos interativos
- 📝 **Cadastro Intuitivo**: Formulário visual para cadastrar peças
- 📈 **Gráficos Dinâmicos**: 
  - Taxa de aprovação (pizza)
  - Motivos de reprovação (barras)
  - Distribuição de peso (histograma)
- 📦 **Monitoramento de Caixas**: Acompanhe o preenchimento em tempo real
- 📋 **Relatórios Completos**: Análises detalhadas e estatísticas
- 🎨 **Design Moderno**: Interface profissional com animações suaves
- 🌙 **Dark Mode**: Tema escuro ativado por padrão

### 🎨 Personalização de Temas

O sistema suporta **Dark Mode** e **Light Mode** com alternância fácil:

#### Dark Mode (Padrão) 🌙
- Fundo escuro para menor cansaço visual
- Alto contraste para melhor legibilidade
- Cores vibrantes (#4CAF50)
- Ideal para ambientes com pouca luz

#### Light Mode ☀️
Para alternar para o tema claro, use o script:

```bash
./toggle_theme.sh light
```

Ou manualmente edite `.streamlit/config.toml`:

```toml
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
```

#### Comandos Úteis:

```bash
# Alternar entre temas automaticamente
./toggle_theme.sh toggle

# Ativar dark mode
./toggle_theme.sh dark

# Ativar light mode
./toggle_theme.sh light

# Ver tema atual
./toggle_theme.sh status
```

📖 Para mais detalhes sobre customização, veja [THEMES.md](THEMES.md)

## 🏭 Arquitetura do Código

Estruturei o projeto seguindo os princípios de **Clean Code** e **Clean Architecture**:

```
sistema-gestao-pecas-industriais/
├── main.py                      # Ponto de entrada (CLI)
├── streamlit_app.py             # Interface visual (Streamlit)
├── models/                      # Modelos de dados
│   ├── peca.py                  # Estrutura de Peça
│   └── caixa.py                 # Estrutura de Caixa
├── services/                    # Lógica de negócio
│   ├── validacao.py             # Validação de qualidade
│   ├── armazenamento.py         # Gestão de caixas
│   └── relatorio.py             # Geração de relatórios
├── utils/                       # Interface do usuário
│   └── menu.py                  # Menu interativo (CLI)
└── .streamlit/                  # Configurações do Streamlit
    └── config.toml              # Tema e configurações
```

### Por que essa estrutura?

- **Separation of Concerns**: Cada camada tem uma responsabilidade única
- **Testabilidade**: Fácil adicionar testes unitários
- **Manutenibilidade**: Código organizado e fácil de entender
- **Escalabilidade**: Simples adicionar novas funcionalidades

## 🎨 Decisões Técnicas

### TypedDict vs Classes
Escolhi `TypedDict` para:
- Type safety sem complexidade de classes
- Simplicidade e clareza no código
- Fácil serialização (preparado para JSON/BD no futuro)

### Constantes Centralizadas
```python
PESO_MINIMO = 95.0
PESO_MAXIMO = 105.0
CORES_ACEITAS = ['azul', 'verde']
CAPACIDADE_MAXIMA_CAIXA = 10
```

Isso torna fácil ajustar os critérios sem mexer na lógica.

### Validação Individual
Cada critério tem sua própria função:
```python
validar_peso(peso)
validar_cor(cor)
validar_comprimento(comprimento)
```

Isso segue o **Single Responsibility Principle** do SOLID.

## 📈 Estatísticas do Projeto

- **2.250+ linhas** de código Python
- **15 arquivos** .py (incluindo database.py)
- **60+ funções** bem documentadas
- **4 camadas** arquiteturais (Models, Services, Database, Interfaces)
- **2 interfaces** (CLI + Visual)
- **31 testes** de persistência (unitários + integração)
- **5 tabelas** no banco de dados normalizado

## 🛠️ Tecnologias Utilizadas

### Core
- **Python 3.9+**: Linguagem principal
- **TypedDict**: Type hints para segurança de tipos
- **SQLite3**: Banco de dados (built-in)

### Interface Visual
- **Streamlit 1.28+**: Framework para interfaces web interativas
- **Plotly 5.17+**: Biblioteca de gráficos interativos
- **Pandas 2.0+**: Manipulação e visualização de dados

### Persistência
- **SQLite**: Banco de dados relacional
- **Schema 3NF**: Normalização profissional
- **Sincronização Automática**: Transparente ao desenvolvedor

### Padrões de Projeto
- **Clean Architecture**: Separação de camadas
- **SOLID Principles**: Single Responsibility em cada função
- **Type Safety**: Tipagem forte em todo o código
- **Factory Pattern**: Funções factory para criação de objetos
- **Repository Pattern**: Camada de persistência isolada

## 🔮 Visão Futura

Este é um protótipo acadêmico, mas pensei em como poderia evoluir para a indústria real:

### 💾 Banco de Dados (✅ IMPLEMENTADO!)
- ✅ SQLite com schema normalizado
- ✅ Persistência automática entre sessões
- ⏳ PostgreSQL para produção
- ⏳ Redis para cache

### 🔌 Hardware & IoT
- Integração com balanças digitais
- Leitores de cor RGB automáticos
- Medidores de comprimento via sensores

### 🤖 Inteligência Artificial
- Visão computacional para detectar defeitos visuais
- Machine learning para prever falhas antes de acontecerem
- Ajuste automático de critérios baseado em histórico


## 🎓 O que Aprendi

Este projeto me ensinou muito sobre:

- **Estruturas de Dados**: Como organizar informações de forma eficiente
- **Lógica de Programação**: Validações condicionais, loops, fluxos de decisão
- **Modularização**: Dividir um problema grande em funções pequenas
- **Clean Code**: Escrever código que outros desenvolvedores conseguem entender
- **Type Safety**: A importância de tipar o código corretamente
- **Documentação**: Um bom README vale ouro

Mas o mais importante: aprendi a **pensar como um programador** - decompor problemas complexos em soluções simples e elegantes.

## 🙏 Agradecimentos

- À disciplina de Algoritmos e Lógica de Programação
- Aos professores que me guiaram nesta jornada
- À documentação oficial do Python (sempre salvando!)

## 📄 Licença

Este projeto foi desenvolvido para fins educacionais como parte do curso de Algoritmos e Lógica de Programação.

---

**Desenvolvido com  💻 por Gabriel Falcão**

*"Código limpo não é escrito seguindo regras. Código limpo é escrito por programadores que se importam."* - Robert C. Martin
