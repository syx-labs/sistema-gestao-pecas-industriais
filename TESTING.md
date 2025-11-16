# 🧪 Guia de Testes

## 📊 Estatísticas

- **Total de testes:** 207
- **Cobertura de código:** 99%
- **Tempo de execução:** ~0.12s

## 🎯 O que é testado

Este projeto possui uma suíte completa de testes que verificam **todas** as funcionalidades especificadas:

### ✅ Funcionalidades Testadas

1. **Recepção de dados de peças** (id, peso, cor, comprimento)
2. **Avaliação automática** com critérios de qualidade:
   - Peso entre 95g e 105g
   - Cor azul ou verde
   - Comprimento entre 10cm e 20cm
3. **Armazenamento em caixas** de capacidade limitada (10 peças)
4. **Fechamento automático** ao atingir capacidade máxima
5. **Criação de nova caixa** após fechamento
6. **Relatórios consolidados** com:
   - Total de peças aprovadas
   - Total de peças reprovadas e motivos
   - Quantidade de caixas utilizadas

## 🚀 Executando os Testes

### Instalação das Dependências

```bash
# Ativar ambiente virtual
source venv/bin/activate

# Instalar dependências de desenvolvimento
pip install -r requirements-dev.txt
```

### Comandos Básicos

```bash
# Executar todos os testes
pytest

# Executar com saída detalhada
pytest -v

# Executar testes com cobertura
pytest --cov=services --cov=models

# Executar testes de uma categoria específica
pytest tests/unit/              # Apenas testes unitários
pytest tests/integration/       # Apenas testes de integração

# Executar arquivo específico
pytest tests/unit/test_validacao.py

# Executar teste específico
pytest tests/unit/test_validacao.py::TestValidarPeso::test_peso_valido_no_minimo
```

### Comandos Avançados

```bash
# Gerar relatório HTML de cobertura
pytest --cov=services --cov=models --cov-report=html
# Abrir htmlcov/index.html no navegador

# Executar apenas testes marcados
pytest -m unit              # Apenas testes unitários
pytest -m integration       # Apenas testes de integração
pytest -m "not slow"        # Pular testes lentos

# Executar testes em paralelo (mais rápido)
pytest -n auto

# Modo verbose com traceback curto
pytest -v --tb=short

# Parar no primeiro erro
pytest -x

# Mostrar saída do print
pytest -s

# Re-executar apenas testes que falharam
pytest --lf
```

## 📁 Estrutura dos Testes

```
tests/
├── conftest.py                          # Fixtures compartilhados
├── unit/                                # Testes unitários (isolados)
│   ├── test_validacao.py               # Validação de qualidade (82 testes)
│   ├── test_armazenamento.py           # Gestão de caixas (67 testes)
│   ├── test_relatorio.py               # Geração de relatórios (44 testes)
│   └── test_models.py                  # Modelos de dados (33 testes)
└── integration/                         # Testes de integração (end-to-end)
    ├── test_workflow_completo.py        # Workflow completo (31 testes)
    └── test_cenarios_reais.py           # Cenários reais (16 testes)
```

## 🧩 Tipos de Testes

### Testes Unitários (174 testes)

Testam funções individuais de forma isolada:

- **test_validacao.py:** Validação de peso, cor, comprimento
- **test_armazenamento.py:** Adição de peças, fechamento de caixas, remoção
- **test_relatorio.py:** Geração de estatísticas e relatórios
- **test_models.py:** Factory functions de Peca e Caixa

### Testes de Integração (33 testes)

Testam o sistema completo em cenários reais:

- **test_workflow_completo.py:** Fluxos end-to-end
- **test_cenarios_reais.py:** Cenário do README (25 peças), produção diária, casos extremos

## 📋 Fixtures Disponíveis

### Fixtures de Peças

```python
peca_valida                      # Peça que atende todos os critérios
peca_peso_invalido               # Peso fora do intervalo
peca_cor_invalida                # Cor não aceita
peca_comprimento_invalido        # Comprimento fora do intervalo
peca_todos_criterios_invalidos   # Falha em todos os critérios
peca_aprovada                    # Peça já validada (aprovada=True)
peca_reprovada                   # Peça já validada (aprovada=False)
```

### Fixtures de Caixas

```python
caixa_vazia                      # Caixa vazia recém criada
caixa_com_uma_peca               # Caixa com 1 peça
caixa_quase_cheia                # Caixa com 9 peças
caixa_cheia                      # Caixa com 10 peças (fechada)
```

### Fixtures de Sistema

```python
sistema_vazio                    # Sistema recém inicializado
sistema_com_pecas_aprovadas      # Sistema com 5 peças aprovadas
sistema_com_pecas_reprovadas     # Sistema com 3 peças reprovadas
sistema_com_caixa_quase_cheia    # Sistema com caixa de 9 peças
sistema_com_multiplas_caixas     # Sistema com 2 caixas fechadas + 1 parcial
```

## 🎨 Marcadores (Markers)

Os testes são marcados para execução seletiva:

```python
@pytest.mark.unit           # Teste unitário
@pytest.mark.integration    # Teste de integração
@pytest.mark.slow           # Teste que demora mais tempo
@pytest.mark.edge_case      # Teste de caso extremo
```

Exemplos de uso:

```bash
pytest -m unit              # Apenas unitários
pytest -m integration       # Apenas integração
pytest -m "not slow"        # Pular testes lentos
pytest -m "unit and edge_case"  # Unitários que são casos extremos
```

## 📊 Relatório de Cobertura

### Cobertura Atual

| Módulo                        | Cobertura |
|-------------------------------|-----------|
| `models/peca.py`              | 100%      |
| `models/caixa.py`             | 100%      |
| `services/validacao.py`       | 100%      |
| `services/relatorio.py`       | 100%      |
| `services/armazenamento.py`   | 98%       |
| **TOTAL**                     | **99%**   |

### Visualizar Relatório HTML

```bash
pytest --cov=services --cov=models --cov-report=html
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

## 🔍 Exemplos de Testes

### Teste de Validação

```python
def test_peso_valido_no_minimo():
    """Peso exatamente no limite mínimo (95g) deve ser aprovado."""
    valido, mensagem = validar_peso(95.0)
    assert valido is True
    assert mensagem == ""
```

### Teste de Integração

```python
def test_processar_10_pecas_fecha_caixa():
    """Processar exatamente 10 peças aprovadas deve fechar uma caixa."""
    sistema = inicializar_sistema()

    for i in range(10):
        peca = criar_peca(f"P{i:03d}", 100.0, "azul", 15.0)
        aprovada, _ = validar_peca(peca)
        peca['aprovada'] = aprovada
        adicionar_peca_em_caixa(peca, sistema)

    assert len(sistema['caixas_fechadas']) == 1
    assert len(sistema['caixa_atual']['pecas']) == 0
```

### Teste Parametrizado

```python
@pytest.mark.parametrize("peso,cor,comprimento,deve_aprovar", [
    (100.0, "azul", 15.0, True),      # Todos válidos
    (100.0, "verde", 15.0, True),     # Todos válidos (cor verde)
    (94.9, "azul", 15.0, False),      # Peso inválido
    (100.0, "vermelho", 15.0, False), # Cor inválida
])
def test_validacao_diversos_cenarios(peso, cor, comprimento, deve_aprovar):
    peca = criar_peca("TEST", peso, cor, comprimento)
    aprovada, _ = validar_peca(peca)
    assert aprovada == deve_aprovar
```

## 🐛 Debugging de Testes

### Executar com Debugger

```bash
# Parar no primeiro erro e abrir pdb
pytest --pdb

# Parar em falhas e erros
pytest --pdb --maxfail=1
```

### Ver Saída Completa

```bash
# Mostrar prints e logs
pytest -s

# Aumentar verbosidade
pytest -vv
```

### Executar Teste Específico com Verbose

```bash
pytest tests/unit/test_validacao.py::TestValidarPeso -vv
```

## 📈 Métricas de Qualidade

### Cobertura Mínima Exigida

Configurado em `pytest.ini`:
```ini
--cov-fail-under=90
```

Se a cobertura cair abaixo de 90%, os testes falharão.

### Estatísticas

- **Testes Unitários:** 174 (84%)
- **Testes de Integração:** 33 (16%)
- **Testes com Parametrização:** 47
- **Fixtures Reutilizáveis:** 12

## 🚨 Troubleshooting

### Erro: "Module not found"

```bash
# Instalar dependências
pip install -r requirements-dev.txt
```

### Erro: "No module named pytest"

```bash
# Ativar ambiente virtual
source venv/bin/activate

# Instalar pytest
pip install pytest
```

### Erro: "Coverage not found"

```bash
pip install pytest-cov
```

### Testes Lentos

```bash
# Executar em paralelo
pip install pytest-xdist
pytest -n auto
```

## ✅ Checklist de Qualidade

Antes de fazer commit, verifique:

- [ ] Todos os testes passam: `pytest`
- [ ] Cobertura >= 90%: `pytest --cov=services --cov=models`
- [ ] Sem warnings: `pytest -p no:warnings`
- [ ] Testes rápidos: tempo < 1 segundo

## 📚 Documentação Adicional

- [Pytest Documentation](https://docs.pytest.org/)
- [Coverage.py](https://coverage.readthedocs.io/)
- [README.md](README.md) - Documentação do projeto
- [CLAUDE.md](CLAUDE.md) - Guia para desenvolvimento

## 🎓 Aprendizados

Esta suíte de testes demonstra:

- **Testes Unitários vs Integração:** Separação clara de responsabilidades
- **Fixtures:** Reutilização de código de setup
- **Parametrização:** Testar múltiplos cenários com menos código
- **Marcadores:** Organização e execução seletiva
- **Cobertura:** Garantia de qualidade quantificável
- **Boas Práticas:** Testes legíveis, manuteníveis e rápidos

---

**Desenvolvido com ☕ e 💻 por Gabriel Falcão**

*"Código sem testes é código legado."* - Michael Feathers
