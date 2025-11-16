# 🧪 Guia de Teste - Exemplos de Uso

Este documento contém cenários de teste para demonstrar todas as funcionalidades do sistema.

## 📝 Cenário de Teste Completo

### Passo 1: Executar o Sistema
```bash
python3 main.py
```

### Passo 2: Cadastrar Peças Aprovadas

**Peça 1 - Aprovada:**
- ID: P001
- Peso: 100
- Cor: azul
- Comprimento: 15

**Peça 2 - Aprovada:**
- ID: P002
- Peso: 98
- Cor: verde
- Comprimento: 12

**Peça 3 - Aprovada:**
- ID: P003
- Peso: 102
- Cor: azul
- Comprimento: 18

### Passo 3: Cadastrar Peças Reprovadas

**Peça 4 - Reprovada (Peso):**
- ID: P004
- Peso: 120
- Cor: azul
- Comprimento: 15
- **Motivo**: Peso fora do intervalo

**Peça 5 - Reprovada (Cor):**
- ID: P005
- Peso: 100
- Cor: vermelho
- Comprimento: 15
- **Motivo**: Cor inadequada

**Peça 6 - Reprovada (Comprimento):**
- ID: P006
- Peso: 100
- Cor: verde
- Comprimento: 25
- **Motivo**: Comprimento fora do intervalo

**Peça 7 - Reprovada (Múltiplos critérios):**
- ID: P007
- Peso: 85
- Cor: preto
- Comprimento: 5
- **Motivos**: Peso, Cor e Comprimento fora dos critérios

### Passo 4: Listar Peças

Escolher opção 2 → opção 'c' (listar todas)

**Resultado esperado:**
- 3 peças aprovadas listadas
- 4 peças reprovadas listadas com motivos

### Passo 5: Remover uma Peça

Escolher opção 3 → digitar 'P007' → confirmar com 's'

**Resultado esperado:**
- Mensagem de sucesso na remoção

### Passo 6: Cadastrar mais peças para fechar caixa

Cadastrar mais 7 peças aprovadas (P008 até P014) para completar 10 peças

**Resultado esperado ao cadastrar P010:**
```
✅ Peça P010 APROVADA!
📦 Caixa #1 FECHADA (10 peças completas)
🆕 Caixa #2 iniciada
```

### Passo 7: Listar Caixas

Escolher opção 4

**Resultado esperado:**
- 1 caixa fechada com 10 peças
- Status de caixa #2 em preenchimento (se houver peças)

### Passo 8: Gerar Relatório Final

Escolher opção 5

**Resultado esperado:**
```
========================================
           RELATÓRIO FINAL
========================================

📊 RESUMO GERAL:
  Total de peças processadas: [número]
  ✅ Peças aprovadas: [número] ([percentual]%)
  ❌ Peças reprovadas: [número] ([percentual]%)

📦 ARMAZENAMENTO:
  Caixas fechadas: [número]
  Caixa em preenchimento: [status]

❌ DETALHAMENTO DE REPROVAÇÕES:
  Por peso inadequado: [número] peças
  Por cor inadequada: [número] peças
  Por comprimento inadequado: [número] peças

========================================
```

## 🎯 Casos de Teste Específicos

### Teste 1: Validação de Peso
| ID | Peso | Esperado |
|----|------|----------|
| T1 | 94.9 | ❌ Reprovada |
| T2 | 95.0 | ✅ Aprovada (se cor e comprimento OK) |
| T3 | 100.0 | ✅ Aprovada (se cor e comprimento OK) |
| T4 | 105.0 | ✅ Aprovada (se cor e comprimento OK) |
| T5 | 105.1 | ❌ Reprovada |

### Teste 2: Validação de Cor
| ID | Cor | Esperado |
|----|-----|----------|
| T6 | azul | ✅ Aprovada (se peso e comprimento OK) |
| T7 | AZUL | ✅ Aprovada (case-insensitive) |
| T8 | verde | ✅ Aprovada (se peso e comprimento OK) |
| T9 | Verde | ✅ Aprovada (case-insensitive) |
| T10 | vermelho | ❌ Reprovada |
| T11 | amarelo | ❌ Reprovada |

### Teste 3: Validação de Comprimento
| ID | Comprimento | Esperado |
|----|-------------|----------|
| T12 | 9.9 | ❌ Reprovada |
| T13 | 10.0 | ✅ Aprovada (se peso e cor OK) |
| T14 | 15.0 | ✅ Aprovada (se peso e cor OK) |
| T15 | 20.0 | ✅ Aprovada (se peso e cor OK) |
| T16 | 20.1 | ❌ Reprovada |

### Teste 4: Validação de IDs Duplicados
1. Cadastrar peça com ID: P999
2. Tentar cadastrar outra peça com ID: P999
3. **Resultado esperado**: Mensagem de erro informando ID duplicado

### Teste 5: Fechamento Automático de Caixa
1. Cadastrar exatamente 10 peças aprovadas
2. **Resultado esperado**: 
   - Na 10ª peça: mensagem de caixa fechada
   - Nova caixa iniciada automaticamente
   - Ao listar caixas: 1 caixa fechada visível

### Teste 6: Tratamento de Entradas Inválidas

**Teste 6.1 - Peso não numérico:**
- ID: T20
- Peso: abc ← **Deve mostrar erro**

**Teste 6.2 - ID vazio:**
- ID: [vazio] ← **Deve mostrar erro**

**Teste 6.3 - Cor vazia:**
- Cor: [vazio] ← **Deve mostrar erro**

## 📊 Checklist de Validação

Após os testes, verificar:

- [ ] Todas as 5 opções do menu funcionam
- [ ] Validação de peso funciona corretamente
- [ ] Validação de cor funciona (case-insensitive)
- [ ] Validação de comprimento funciona
- [ ] Caixas fecham automaticamente ao atingir 10 peças
- [ ] Nova caixa é criada automaticamente
- [ ] Relatório mostra estatísticas corretas
- [ ] Remoção de peças funciona
- [ ] Listagem de peças exibe todas as informações
- [ ] Listagem de caixas mostra caixas fechadas e atual
- [ ] Tratamento de erros em entradas inválidas funciona
- [ ] IDs duplicados são detectados
- [ ] Sistema pode ser encerrado com opção 0

## 🎬 Demonstração para Vídeo Pitch

### Roteiro Sugerido (4 minutos)

**[0:00 - 0:30] Introdução**
- Apresentar o problema industrial
- Explicar o impacto da inspeção manual

**[0:30 - 1:30] Demonstração - Cadastro**
- Cadastrar 2 peças aprovadas
- Cadastrar 1 peça reprovada (mostrar motivos)
- Explicar os critérios de qualidade

**[1:30 - 2:30] Demonstração - Funcionalidades**
- Listar peças (mostrar separação aprovadas/reprovadas)
- Listar caixas (explicar sistema de 10 peças)
- Gerar relatório (mostrar estatísticas)

**[2:30 - 3:30] Explicação Técnica**
- Mostrar estrutura de código (tree)
- Explicar Clean Code aplicado
- Destacar modularidade (models, services, utils)

**[3:30 - 4:00] Conclusão**
- Benefícios da automação
- Possibilidades de expansão futura
- Encerramento

---

**💡 Dica:** Durante o teste, anote os resultados para incluir no documento da parte teórica!
