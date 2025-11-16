# 🏭 Sistema de Automação Digital para Gestão de Peças Industriais

Sistema desenvolvido em Python para automatizar o controle de produção e qualidade de peças fabricadas em linha de montagem industrial.

## 📋 Descrição do Projeto

Este sistema resolve o problema crítico da inspeção manual de peças, que gera atrasos, falhas de conferência e aumento de custos operacionais. Através de uma solução automatizada, o sistema:

- ✅ Avalia automaticamente a qualidade de cada peça produzida
- 📦 Organiza peças aprovadas em caixas de capacidade controlada
- 📊 Gera relatórios consolidados em tempo real
- 🎯 Rastreia motivos de reprovação para análise de qualidade

## 🎯 Critérios de Qualidade

Uma peça é **APROVADA** apenas se atender **TODOS** os critérios:

| Critério | Valor Aceito |
|----------|--------------|
| **Peso** | Entre 95g e 105g |
| **Cor** | Azul ou Verde |
| **Comprimento** | Entre 10cm e 20cm |

Qualquer desvio desses critérios resulta em **REPROVAÇÃO** automática.

## 🚀 Como Executar

### Pré-requisitos

- Python 3.8 ou superior
- Sistema operacional: Windows, macOS ou Linux

### Instalação

1. Clone ou baixe este repositório:
```bash
git clone <url-do-repositorio>
cd rocketseat-project-python
```

2. Nenhuma dependência externa é necessária! O projeto usa apenas a biblioteca padrão do Python.

### Executando o Programa

**Opção 1 - Via Python:**
```bash
python3 main.py
```

**Opção 2 - Executável direto (Linux/macOS):**
```bash
./main.py
```

**Opção 3 - Windows:**
```bash
python main.py
```

## 📱 Funcionalidades

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

### 1️⃣ Cadastrar Nova Peça

Permite inserir os dados de uma peça (ID, peso, cor, comprimento) e:
- Valida automaticamente contra os critérios de qualidade
- Exibe imediatamente se foi aprovada ou reprovada
- Se aprovada: adiciona na caixa atual
- Se a caixa atingir 10 peças: fecha automaticamente e cria nova caixa

**Exemplo de uso:**
```
ID da peça: P001
Peso (g): 100
Cor: azul
Comprimento (cm): 15

✅ Peça P001 APROVADA!
Adicionada à Caixa #1 (1/10 peças)
```

### 2️⃣ Listar Peças

Oferece três opções:
- **a)** Listar apenas peças aprovadas
- **b)** Listar apenas peças reprovadas (com motivos)
- **c)** Listar todas as peças

**Exemplo de saída (peça reprovada):**
```
❌ PEÇAS REPROVADAS (1):
  ID: P002
    Peso: 120.0g
    Cor: vermelho
    Comprimento: 25.0cm
    Motivos:
      - Peso fora do intervalo (95.0-105.0g): 120.0g
      - Cor inadequada (esperado: azul ou verde): vermelho
      - Comprimento fora do intervalo (10.0-20.0cm): 25.0cm
```

### 3️⃣ Remover Peça

Permite remover uma peça cadastrada (aprovada ou reprovada) pelo seu ID.
Solicita confirmação antes de executar a remoção.

### 4️⃣ Listar Caixas

Exibe:
- **Caixas fechadas**: que atingiram 10 peças
- **Caixa em preenchimento**: atual, com quantidade de peças
- IDs de todas as peças em cada caixa

**Exemplo:**
```
📦 CAIXAS FECHADAS (1):
  Caixa #1 - 10 peças
  Status: 🔒 Fechada
  IDs das peças: P001, P003, P005, P007, P009, P011, P013, P015, P017, P019

📦 CAIXA EM PREENCHIMENTO:
  Caixa #2 - 3/10 peças
  IDs das peças: P021, P023, P025
```

### 5️⃣ Gerar Relatório Final

Gera relatório completo com:
- Total de peças processadas
- Percentual de aprovação/reprovação
- Quantidade de caixas fechadas
- Detalhamento de reprovações por critério (peso, cor, comprimento)

**Exemplo:**
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

## 🏗️ Estrutura do Código

O projeto segue os princípios de **Clean Code** e **Clean Architecture**:

```
rocketseat-project-python/
├── main.py                     # Ponto de entrada - loop principal
├── models/                     # Camada de Domínio
│   ├── __init__.py
│   ├── peca.py                 # Modelo de Peça
│   └── caixa.py                # Modelo de Caixa + Constantes
├── services/                   # Camada de Lógica de Negócio
│   ├── __init__.py
│   ├── validacao.py            # Validação de qualidade
│   ├── armazenamento.py        # Gerenciamento de caixas
│   └── relatorio.py            # Geração de relatórios
├── utils/                      # Camada de Apresentação
│   ├── __init__.py
│   └── menu.py                 # Interface do usuário
├── .gitignore
├── requirements.txt
├── README.md
└── PRD_IMPLEMENTACAO.md        # Documento de especificação
```

## 🎨 Decisões Técnicas

### Princípios Aplicados

1. **Single Responsibility Principle (SRP)**
   - Cada módulo tem uma responsabilidade única e bem definida
   - `validacao.py`: apenas valida critérios
   - `armazenamento.py`: apenas gerencia caixas
   - `relatorio.py`: apenas gera relatórios

2. **Clean Code**
   - Nomes de variáveis e funções autodescritivos
   - Funções pequenas e focadas
   - Comentários apenas onde necessário (código auto-explicativo)
   - Type hints para clareza de tipos

3. **Separation of Concerns**
   - Modelos: estrutura de dados
   - Services: lógica de negócio
   - Utils: interface com usuário
   - Main: orquestração

4. **DRY (Don't Repeat Yourself)**
   - Constantes centralizadas (`CAPACIDADE_MAXIMA_CAIXA`, `PESO_MINIMO`, etc.)
   - Funções reutilizáveis para validação
   - Factory functions para criação de objetos

### Estruturas de Dados

**TypedDict** foi escolhido para:
- Type safety sem complexidade de classes
- Simplicidade e clareza
- Fácil serialização (futuro: JSON/BD)

### Validação de Entrada

- Tratamento de erros em inputs numéricos
- Validação de campos vazios
- Verificação de IDs duplicados
- Confirmação em operações destrutivas (remoção)

## 🔄 Fluxo de Execução

```
Usuário → Menu → Opção Escolhida
                      ↓
                [Cadastrar Peça]
                      ↓
         Coleta: ID, Peso, Cor, Comprimento
                      ↓
            [Validar Qualidade]
                      ↓
              ┌───────┴───────┐
              ↓               ↓
          APROVADA        REPROVADA
              ↓               ↓
      [Adicionar na      [Registrar
         Caixa]           Motivos]
              ↓
      [Verificar se
       caixa lotou]
              ↓
      [Fechar e criar
        nova se sim]
              ↓
      [Feedback ao
         Usuário]
```

## 📈 Possíveis Expansões Futuras

Este protótipo poderia ser expandido para um cenário industrial real:

### 🔌 Integração com Hardware
- **Sensores IoT**: Balanças digitais, leitores de cor RGB, medidores de comprimento
- **Protocolo MQTT**: Comunicação em tempo real com dispositivos
- **Raspberry Pi**: Controle embarcado da linha de produção

### 🤖 Inteligência Artificial
- **Visão Computacional**: Detecção automática de defeitos visuais
- **Machine Learning**: Previsão de falhas baseada em padrões históricos
- **Ajuste Dinâmico**: Otimização automática de critérios de qualidade

### 🏢 Integração Industrial
- **MES (Manufacturing Execution System)**: Sincronização com gestão fabril
- **ERP**: Integração com SAP/Oracle para rastreabilidade completa
- **Dashboard**: Visualização em tempo real de KPIs
- **Banco de Dados**: PostgreSQL/MongoDB para persistência
- **API REST**: Exposição de dados para outros sistemas

### ⚙️ Automação Completa
- **Esteira Automatizada**: Separação física automática de peças
- **Robótica**: Braço robótico para empacotamento
- **Etiquetagem**: QR Code/RFID em cada caixa

## 👨‍💻 Autor

**Gabriel Falcão**  
Projeto Acadêmico - Algoritmos e Lógica de Programação  
Data: Novembro 2025

## 📄 Licença

Este projeto foi desenvolvido para fins educacionais.

---

**💡 Dica:** Para uma experiência melhor, use um terminal com suporte a emojis e cores.
