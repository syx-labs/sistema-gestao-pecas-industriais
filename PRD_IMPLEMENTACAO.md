# PRD - Sistema de Automação Digital para Gestão de Peças Industriais

## 1. DECLARAÇÃO DO PROBLEMA

### Contexto
Empresas do setor industrial enfrentam desafios críticos no controle de produção e qualidade das peças fabricadas. O processo atual de inspeção manual gera:
- **Atrasos operacionais**: Tempo excessivo na conferência de cada peça
- **Falhas de conferência**: Erro humano na avaliação de critérios de qualidade
- **Aumento de custos**: Overhead operacional e retrabalho
- **Falta de rastreabilidade**: Dificuldade em gerar relatórios consolidados

### Problema a Resolver
Desenvolver um sistema automatizado em Python que elimine a inspeção manual, garantindo:
- Avaliação automática de qualidade baseada em critérios objetivos
- Organização inteligente do armazenamento de peças aprovadas
- Geração de relatórios consolidados em tempo real
- Interface interativa para gestão completa do processo

---

## 2. ESTADO ATUAL DO PROJETO

### Estrutura de Diretórios
```
/Users/ogabrielfalcao/Projects/rocketseat-project-python/
├── Roteiro do Trabalho - Algoritmos e Lógica.docx.pdf  # Especificação do projeto
└── (Projeto não iniciado - nenhum código existente)
```

### Análise
- ✅ Especificação completa do projeto disponível
- ❌ Nenhum código Python desenvolvido
- ❌ Estrutura de diretórios não criada
- ❌ README.md não existente
- ❌ Repositório Git não inicializado

---

## 3. REQUISITOS FUNCIONAIS

### 3.1 Modelo de Dados - Peça
Cada peça deve conter:
- **ID**: Identificador único (string ou número)
- **Peso**: Valor em gramas (float)
- **Cor**: String (azul, verde, vermelho, etc.)
- **Comprimento**: Valor em centímetros (float)
- **Status**: Aprovada/Reprovada (calculado automaticamente)
- **Motivo da Reprovação**: Lista de critérios não atendidos (se aplicável)

### 3.2 Critérios de Qualidade (Regras de Negócio)
Uma peça é **APROVADA** apenas se atender TODOS os critérios:
1. Peso: 95g ≤ peso ≤ 105g
2. Cor: "azul" OU "verde" (case-insensitive)
3. Comprimento: 10cm ≤ comprimento ≤ 20cm

Se QUALQUER critério falhar, a peça é **REPROVADA** e o(s) motivo(s) devem ser registrados.

### 3.3 Sistema de Armazenamento - Caixas
- Capacidade máxima: **10 peças aprovadas por caixa**
- Quando uma caixa atinge 10 peças, ela é **automaticamente fechada**
- Uma nova caixa é **automaticamente iniciada** para as próximas peças
- Apenas peças **APROVADAS** são armazenadas em caixas
- Cada caixa deve ter um identificador único (ex: Caixa #1, Caixa #2, etc.)

### 3.4 Menu Interativo
O sistema deve apresentar um menu com as seguintes opções:

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

#### Opção 1: Cadastrar Nova Peça
- Solicitar ao usuário: ID, peso, cor e comprimento
- Validar automaticamente contra critérios de qualidade
- Se aprovada: adicionar à caixa atual
- Se caixa atingir 10 peças: fechar caixa e criar nova
- Exibir feedback imediato (aprovada/reprovada + motivos)

#### Opção 2: Listar Peças Aprovadas/Reprovadas
- Submenu:
  - a) Listar todas as peças aprovadas
  - b) Listar todas as peças reprovadas (com motivos)
  - c) Listar todas as peças
- Formato de exibição claro e organizado

#### Opção 3: Remover Peça Cadastrada
- Solicitar ID da peça
- Buscar e confirmar remoção
- Se peça estiver em caixa: reorganizar caixa
- Atualizar contadores

#### Opção 4: Listar Caixas Fechadas
- Exibir todas as caixas que atingiram 10 peças
- Mostrar: ID da caixa, quantidade de peças, IDs das peças contidas
- Incluir caixa atual (em preenchimento) se houver peças

#### Opção 5: Gerar Relatório Final
- **Total de peças aprovadas**
- **Total de peças reprovadas** (com breakdown por motivo)
- **Quantidade de caixas fechadas**
- **Caixa em preenchimento** (se houver)
- **Taxa de aprovação** (percentual)
- **Distribuição de reprovações** por critério:
  - Quantas por peso inadequado
  - Quantas por cor inadequada
  - Quantas por comprimento inadequado

---

## 4. REQUISITOS NÃO FUNCIONAIS

### 4.1 Qualidade de Código
- **Linguagem**: Python 3.8+
- **Estrutura**: Modular com funções bem definidas
- **Responsabilidade Única**: Cada função deve ter um propósito claro
- **Nomes Significativos**: Variáveis e funções com nomes autodescritivos
- **Tratamento de Erros**: Validação de entradas do usuário
- **Sem Redundância**: Código DRY (Don't Repeat Yourself)

### 4.2 Boas Práticas Python
- Type hints onde apropriado
- Docstrings em funções principais
- Uso de estruturas de dados adequadas (listas, dicionários)
- Separação de lógica de negócio e interface
- Constantes para valores fixos (capacidade da caixa, limites de qualidade)

### 4.3 Documentação
- **README.md completo** contendo:
  - Descrição do projeto
  - Pré-requisitos (Python 3.8+)
  - Como executar o programa (passo a passo)
  - Exemplos de uso com entradas e saídas esperadas
  - Estrutura do código
  - Decisões técnicas

### 4.4 Controle de Versão
- Repositório Git inicializado
- Commits atômicos e frequentes
- Mensagens de commit descritivas
- `.gitignore` apropriado para Python
- README.md na raiz

---

## 5. ARQUITETURA PROPOSTA

### 5.1 Estrutura de Arquivos
```
rocketseat-project-python/
├── .git/                           # Controle de versão
├── .gitignore                      # Ignora __pycache__, .pyc, etc.
├── README.md                       # Documentação principal
├── main.py                         # Ponto de entrada - menu interativo
├── models/
│   ├── __init__.py
│   ├── peca.py                     # Classe/dicionário Peça
│   └── caixa.py                    # Classe/dicionário Caixa
├── services/
│   ├── __init__.py
│   ├── validacao.py                # Lógica de validação de qualidade
│   ├── armazenamento.py            # Gerenciamento de caixas
│   └── relatorio.py                # Geração de relatórios
├── utils/
│   ├── __init__.py
│   └── menu.py                     # Funções de interface do menu
└── requirements.txt                # Dependências (se houver)
```

### 5.2 Fluxo de Dados
```
[Usuário] → [Menu Interativo (main.py)]
              ↓
         [Escolha de Opção]
              ↓
    ┌─────────┴─────────┐
    ↓                   ↓
[Cadastrar Peça]    [Outras Operações]
    ↓
[Coletar Dados: ID, Peso, Cor, Comprimento]
    ↓
[Validar Qualidade (validacao.py)]
    ↓
┌───┴───┐
↓       ↓
APROVADA  REPROVADA
↓       ↓
[Armazenar em Caixa]  [Registrar Motivo]
↓
[Verificar Capacidade]
↓
[Se 10 peças: Fechar Caixa e Criar Nova]
↓
[Feedback ao Usuário]
```

### 5.3 Estruturas de Dados Principais

#### Peça (Dicionário ou Dataclass)
```python
peca = {
    'id': str,
    'peso': float,
    'cor': str,
    'comprimento': float,
    'aprovada': bool,
    'motivos_reprovacao': list[str]
}
```

#### Caixa (Dicionário ou Dataclass)
```python
caixa = {
    'id': int,
    'pecas': list[dict],  # Lista de peças aprovadas
    'fechada': bool
}
```

#### Estado Global da Aplicação
```python
sistema = {
    'pecas_aprovadas': list[dict],
    'pecas_reprovadas': list[dict],
    'caixas_fechadas': list[dict],
    'caixa_atual': dict,
    'contador_caixas': int
}
```

---

## 6. PLANO DE IMPLEMENTAÇÃO

### Fase 1: Inicialização do Projeto (15 min)
- [ ] Criar estrutura de diretórios
- [ ] Inicializar repositório Git
- [ ] Criar `.gitignore` para Python
- [ ] Criar `requirements.txt` (vazio inicialmente)
- [ ] Commit inicial

### Fase 2: Modelos de Dados (30 min)
- [ ] Criar `models/peca.py` com estrutura de Peça
- [ ] Criar `models/caixa.py` com estrutura de Caixa
- [ ] Definir constantes (CAPACIDADE_CAIXA = 10)
- [ ] Commit: "feat: adiciona modelos de dados (Peça e Caixa)"

### Fase 3: Lógica de Validação (45 min)
- [ ] Criar `services/validacao.py`
- [ ] Implementar função `validar_peso(peso: float) -> tuple[bool, str]`
- [ ] Implementar função `validar_cor(cor: str) -> tuple[bool, str]`
- [ ] Implementar função `validar_comprimento(comprimento: float) -> tuple[bool, str]`
- [ ] Implementar função `validar_peca(peca: dict) -> tuple[bool, list[str]]`
- [ ] Testar manualmente cada função
- [ ] Commit: "feat: implementa lógica de validação de qualidade"

### Fase 4: Gerenciamento de Armazenamento (45 min)
- [ ] Criar `services/armazenamento.py`
- [ ] Implementar função `adicionar_peca_caixa(peca, caixa_atual, caixas_fechadas)`
- [ ] Implementar lógica de fechar caixa quando atingir 10 peças
- [ ] Implementar criação de nova caixa
- [ ] Implementar função `remover_peca(id, sistema)`
- [ ] Commit: "feat: implementa sistema de armazenamento em caixas"

### Fase 5: Sistema de Relatórios (30 min)
- [ ] Criar `services/relatorio.py`
- [ ] Implementar função `gerar_relatorio(sistema)`
- [ ] Calcular estatísticas (total aprovadas, reprovadas, caixas)
- [ ] Formatar saída de forma clara e organizada
- [ ] Commit: "feat: implementa geração de relatórios"

### Fase 6: Interface do Menu (60 min)
- [ ] Criar `utils/menu.py` com funções auxiliares
- [ ] Implementar função `exibir_menu()`
- [ ] Implementar função `cadastrar_peca_interface(sistema)`
- [ ] Implementar função `listar_pecas_interface(sistema)`
- [ ] Implementar função `remover_peca_interface(sistema)`
- [ ] Implementar função `listar_caixas_interface(sistema)`
- [ ] Implementar função `gerar_relatorio_interface(sistema)`
- [ ] Tratamento de erros e validação de entradas
- [ ] Commit: "feat: implementa interface de menu interativo"

### Fase 7: Main - Integração (30 min)
- [ ] Criar `main.py`
- [ ] Inicializar estado do sistema
- [ ] Implementar loop principal do menu
- [ ] Integrar todas as funções
- [ ] Testar fluxo completo
- [ ] Commit: "feat: integra todas as funcionalidades no main.py"

### Fase 8: Documentação (45 min)
- [ ] Criar `README.md` completo
- [ ] Adicionar descrição do projeto
- [ ] Documentar como executar
- [ ] Adicionar exemplos de uso
- [ ] Incluir decisões técnicas
- [ ] Commit: "docs: adiciona README completo"

### Fase 9: Testes e Refinamento (30 min)
- [ ] Testar todos os fluxos do menu
- [ ] Testar casos extremos (entradas inválidas)
- [ ] Testar com múltiplas peças e caixas
- [ ] Refatorar código se necessário
- [ ] Commit: "refactor: melhora tratamento de erros e validações"

### Fase 10: Preparação para Entrega (30 min)
- [ ] Revisar TODO o código
- [ ] Verificar nomenclaturas e clareza
- [ ] Garantir commits frequentes e bem descritos
- [ ] Criar repositório no GitHub
- [ ] Push do código
- [ ] Testar clone e execução do zero
- [ ] Commit final: "chore: prepara projeto para entrega"

**Tempo Total Estimado: ~5h 30min**

---

## 7. CRITÉRIOS DE QUALIDADE DO CÓDIGO

### Princípio da Responsabilidade Única
✅ **BOM EXEMPLO:**
```python
def validar_peso(peso: float) -> tuple[bool, str]:
    """Valida se o peso está dentro do intervalo aceitável."""
    if 95 <= peso <= 105:
        return True, ""
    return False, f"Peso fora do intervalo (95-105g): {peso}g"
```

❌ **EXEMPLO RUIM:**
```python
def validar_peca_e_adicionar_e_gerar_relatorio(peca, caixas):  # Múltiplas responsabilidades!
    # Faz validação, adiciona em caixa E gera relatório - ERRADO!
    pass
```

### Nomes Significativos
✅ **BOM EXEMPLO:**
```python
total_pecas_aprovadas = len(pecas_aprovadas)
CAPACIDADE_MAXIMA_CAIXA = 10
```

❌ **EXEMPLO RUIM:**
```python
x = len(p)  # O que é x? O que é p?
MAX = 10    # MAX de quê?
```

### Estrutura Modular
✅ **BOM EXEMPLO:**
```python
# Em validacao.py
def validar_peca(peca: dict) -> tuple[bool, list[str]]:
    motivos = []
    
    valido_peso, msg_peso = validar_peso(peca['peso'])
    if not valido_peso:
        motivos.append(msg_peso)
    
    valido_cor, msg_cor = validar_cor(peca['cor'])
    if not valido_cor:
        motivos.append(msg_cor)
    
    valido_comp, msg_comp = validar_comprimento(peca['comprimento'])
    if not valido_comp:
        motivos.append(msg_comp)
    
    return len(motivos) == 0, motivos
```

---

## 8. EXEMPLOS DE ENTRADAS E SAÍDAS

### Exemplo 1: Cadastro de Peça Aprovada
```
> Escolha uma opção: 1

ID da peça: P001
Peso (g): 100
Cor: azul
Comprimento (cm): 15

✅ Peça P001 APROVADA!
Adicionada à Caixa #1 (1/10 peças)
```

### Exemplo 2: Cadastro de Peça Reprovada
```
> Escolha uma opção: 1

ID da peça: P002
Peso (g): 120
Cor: vermelho
Comprimento (cm): 25

❌ Peça P002 REPROVADA!
Motivos:
  - Peso fora do intervalo (95-105g): 120.0g
  - Cor inadequada (esperado: azul ou verde): vermelho
  - Comprimento fora do intervalo (10-20cm): 25.0cm
```

### Exemplo 3: Fechamento de Caixa
```
> Escolha uma opção: 1

ID da peça: P010
Peso (g): 98
Cor: verde
Comprimento (cm): 12

✅ Peça P010 APROVADA!
📦 Caixa #1 FECHADA (10 peças completas)
🆕 Caixa #2 iniciada
```

### Exemplo 4: Relatório Final
```
> Escolha uma opção: 5

========== RELATÓRIO FINAL ==========

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

=====================================
```

---

## 9. EXPANSÃO FUTURA (Reflexão)

Este protótipo em Python poderia ser expandido para um cenário industrial real através de:

### 9.1 Integração com Hardware
- **Sensores IoT**: Conexão com balanças digitais, leitores de cor (RGB), medidores de comprimento
- **Protocolo MQTT**: Comunicação em tempo real com dispositivos
- **Raspberry Pi / Arduino**: Controle de linha de produção

### 9.2 Inteligência Artificial
- **Visão Computacional**: Identificação automática de defeitos visuais (arranhões, rachaduras)
- **Machine Learning**: Previsão de falhas baseada em padrões históricos
- **Aprendizado contínuo**: Ajuste automático de critérios de qualidade

### 9.3 Integração Industrial
- **MES (Manufacturing Execution System)**: Sincronização com sistema de gestão fabril
- **ERP**: Integração com SAP, Oracle para rastreabilidade completa
- **Dashboard em tempo real**: Visualização de KPIs (taxa de aprovação, throughput)
- **Banco de Dados**: PostgreSQL/MongoDB para persistência de dados
- **API REST**: Exposição de dados para outros sistemas

### 9.4 Automação Completa
- **Esteira automatizada**: Separação física automática de peças aprovadas/reprovadas
- **Robótica**: Braço robótico para empacotamento
- **Etiquetagem automática**: QR Code/RFID em cada caixa

---

## 10. CHECKLIST DE ENTREGA

### Código (3,5 pontos)
- [ ] Menu interativo com todas as 5 opções funcionais
- [ ] Opção 1: Cadastrar nova peça (com validação)
- [ ] Opção 2: Listar peças aprovadas/reprovadas
- [ ] Opção 3: Remover peça cadastrada
- [ ] Opção 4: Listar caixas fechadas
- [ ] Opção 5: Gerar relatório final
- [ ] Código limpo, modular e bem estruturado
- [ ] Nomes significativos em variáveis e funções
- [ ] Tratamento de erros adequado
- [ ] Repositório GitHub criado e público
- [ ] README.md completo com:
  - [ ] Explicação do funcionamento
  - [ ] Como rodar (passo a passo)
  - [ ] Exemplos de entradas e saídas

### Parte Teórica (1,5 pontos)
- [ ] Contextualização: importância da automação na indústria
- [ ] Explicação da estrutura lógica (decisões, funções, condições, loops)
- [ ] Benefícios da solução
- [ ] Desafios enfrentados no desenvolvimento
- [ ] Reflexão sobre expansão futura (sensores, IA, integração)

### Vídeo Pitch (2,0 pontos)
- [ ] Duração: até 4 minutos
- [ ] Apresentação do problema industrial
- [ ] Explicação da lógica do sistema
- [ ] Técnicas e boas práticas aplicadas
- [ ] Demonstração do programa funcionando
- [ ] Link público ou não listado (YouTube/Loom/Drive)

---

## 11. TECNOLOGIAS E FERRAMENTAS

- **Linguagem**: Python 3.8+
- **Controle de Versão**: Git + GitHub
- **IDE Sugerida**: VSCode, PyCharm ou qualquer editor de preferência
- **Dependências**: Nenhuma biblioteca externa necessária (usa apenas stdlib)
- **Sistema Operacional**: Compatível com macOS, Linux e Windows

---

## 12. CRITÉRIOS DE SUCESSO

O projeto será considerado bem-sucedido se:

1. ✅ Todas as funcionalidades do menu estiverem implementadas e funcionando
2. ✅ Validação automática de qualidade estiver correta (peso, cor, comprimento)
3. ✅ Sistema de caixas fechar automaticamente ao atingir 10 peças
4. ✅ Relatórios forem precisos e completos
5. ✅ Código seguir princípios de Clean Code (nomes claros, funções pequenas, SRP)
6. ✅ README.md permitir que qualquer pessoa clone e execute o projeto
7. ✅ Repositório GitHub estiver organizado com commits bem descritos
8. ✅ Documentação teórica cobrir todos os pontos solicitados
9. ✅ Vídeo pitch demonstrar claramente o valor da solução

---

## 13. RISCOS E MITIGAÇÕES

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| Prazo curto (entrega hoje) | Alta | Alto | Focar no MVP, estrutura modular permite desenvolvimento incremental |
| Complexidade do menu interativo | Média | Médio | Usar funções auxiliares, separar lógica de interface |
| Bugs na lógica de validação | Média | Alto | Testar cada função individualmente antes de integrar |
| Dificuldade em organizar código | Baixa | Médio | Seguir estrutura proposta, commits frequentes |
| Falta de tempo para vídeo | Média | Alto | Preparar script antes, demonstração simples mas efetiva |

---

## PRÓXIMOS PASSOS

Após aprovação deste PRD, iniciar imediatamente a implementação seguindo o plano de 10 fases descrito na Seção 6. Priorizar:

1. **Inicialização rápida** do projeto (Git, estrutura)
2. **Implementação do core** (validação + armazenamento)
3. **Interface funcional** (menu interativo)
4. **Documentação clara** (README)
5. **Testes completos** antes do vídeo
6. **Gravação do pitch** como última etapa

---

**Status do Documento**: ✅ Completo e pronto para aprovação
**Data de Criação**: 2025-11-15
**Prazo de Entrega**: HOJE (2025-11-15)
**Estimativa de Implementação**: 5h 30min

---

*Este PRD fornece uma base sólida para o desenvolvimento do projeto. Aguardando aprovação para iniciar a implementação.*
