# 💾 Banco de Dados SQLite - Guia Completo

## 📖 Visão Geral

O sistema agora possui **persistência de dados** usando SQLite com schema normalizado (3NF). Todos os dados são salvos automaticamente e carregados entre execuções.

## ✨ Características

- ✅ **Persistência Automática** - Dados salvos após cada operação
- ✅ **Schema Normalizado (3NF)** - Banco de dados profissional
- ✅ **Compatibilidade Total** - Código existente funciona sem mudanças
- ✅ **Sincronização Transparente** - Desenvolvedor não precisa se preocupar
- ✅ **100% Testado** - Testes unitários e de integração completos

## 🚀 Como Usar

### Uso Normal (Automático)

A persistência funciona automaticamente. Basta usar o sistema normalmente:

```python
from services.armazenamento import inicializar_sistema, adicionar_peca_em_caixa
from models.peca import criar_peca

# Primeira execução - cria banco vazio
sistema = inicializar_sistema()

# Adiciona peças
peca = criar_peca("P001", 100.0, "azul", 15.0, True)
adicionar_peca_em_caixa(peca, sistema)
# ↑ Salvo automaticamente no banco!

# Segunda execução - carrega do banco
sistema = inicializar_sistema()
print(len(sistema['pecas_aprovadas']))  # 1 peça carregada!
```

### Script de Demonstração

Execute o script de teste para ver a persistência funcionando:

```bash
# Primeira execução
python3 test_persistencia.py

# Segunda execução - verá os dados anteriores
python3 test_persistencia.py

# Terceira execução - continua acumulando
python3 test_persistencia.py
```

### CLI Interativa

```bash
# CLI mantém dados entre execuções
python3 main.py
```

### Interface Streamlit

```bash
# Streamlit também persiste dados
streamlit run streamlit_app.py
```

## 📊 Schema do Banco

### Tabelas

**pecas** - Armazena todas as peças
```sql
CREATE TABLE pecas (
    id TEXT PRIMARY KEY,
    peso REAL NOT NULL,
    cor TEXT NOT NULL,
    comprimento REAL NOT NULL,
    aprovada BOOLEAN NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**motivos_reprovacao** - Motivos de peças reprovadas (1:N)
```sql
CREATE TABLE motivos_reprovacao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    peca_id TEXT NOT NULL,
    motivo TEXT NOT NULL,
    FOREIGN KEY (peca_id) REFERENCES pecas(id) ON DELETE CASCADE
);
```

**caixas** - Caixas de armazenamento
```sql
CREATE TABLE caixas (
    id INTEGER PRIMARY KEY,
    fechada BOOLEAN NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**caixas_pecas** - Relacionamento caixas-peças (N:M)
```sql
CREATE TABLE caixas_pecas (
    caixa_id INTEGER NOT NULL,
    peca_id TEXT NOT NULL,
    ordem INTEGER NOT NULL,
    PRIMARY KEY (caixa_id, peca_id),
    FOREIGN KEY (caixa_id) REFERENCES caixas(id) ON DELETE CASCADE,
    FOREIGN KEY (peca_id) REFERENCES pecas(id) ON DELETE CASCADE
);
```

**sistema_config** - Configurações do sistema
```sql
CREATE TABLE sistema_config (
    chave TEXT PRIMARY KEY,
    valor TEXT NOT NULL
);
```

## 🔧 Funções Disponíveis

### Módulo `services/database.py`

```python
from services import database

# Inicialização
database.inicializar_database()  # Cria schema se não existir
database.banco_existe()          # Verifica se banco existe

# Peças
database.salvar_peca(peca)       # Salva/atualiza peça
database.deletar_peca(id_peca)   # Remove peça do banco
database.carregar_pecas()        # Retorna (aprovadas, reprovadas)

# Caixas
database.salvar_caixa(caixa)     # Salva caixa + peças
database.carregar_caixas()       # Retorna (fechadas, atual, contador)

# Sistema Completo
database.carregar_sistema_completo()  # Carrega tudo
database.sincronizar_sistema(sistema) # Salva tudo

# Configuração
database.salvar_config(chave, valor)
database.carregar_config(chave, default)

# Utilidades
database.limpar_banco()          # Remove dados (mantém schema)
database.remover_banco()         # Deleta arquivo .db
```

## 📁 Localização do Banco

```
rocketseat-project-python/
├── sistema_pecas.db  ← Banco SQLite (criado automaticamente)
└── services/
    └── database.py   ← Camada de persistência
```

**Importante:** O arquivo `sistema_pecas.db` está no `.gitignore` e não será versionado.

## 🧪 Testes

### Executar Testes Unitários

```bash
pytest tests/unit/test_database.py -v
```

**Cobertura:** 19 testes, 98% de cobertura

### Executar Testes de Integração

```bash
pytest tests/integration/test_database_integration.py -v
```

**Cobertura:** 12 testes validando persistência end-to-end

### Executar Todos os Testes

```bash
pytest tests/ -v --cov=services --cov=models
```

## 🔍 Inspeção do Banco

### Ver Tabelas

```bash
sqlite3 sistema_pecas.db "SELECT name FROM sqlite_master WHERE type='table';"
```

### Contar Peças

```bash
sqlite3 sistema_pecas.db "SELECT COUNT(*) FROM pecas;"
```

### Ver Peças Aprovadas

```bash
sqlite3 sistema_pecas.db "SELECT * FROM pecas WHERE aprovada = 1;"
```

### Ver Caixas

```bash
sqlite3 sistema_pecas.db "SELECT * FROM caixas;"
```

### Ver Relacionamento Caixas-Peças

```bash
sqlite3 sistema_pecas.db "
SELECT c.id as caixa_id, c.fechada, p.id as peca_id, p.cor
FROM caixas c
JOIN caixas_pecas cp ON c.id = cp.caixa_id
JOIN pecas p ON cp.peca_id = p.id
ORDER BY c.id, cp.ordem;
"
```

## 🔄 Resetar Sistema

Para começar do zero:

```bash
# Remove o banco de dados
rm sistema_pecas.db

# Próxima execução criará banco novo
python3 main.py
```

Ou via código:

```python
from services import database

# Opção 1: Limpa dados (mantém schema)
database.limpar_banco()

# Opção 2: Remove arquivo completamente
database.remover_banco()
```

## 🎯 Casos de Uso

### Backup dos Dados

```bash
# Fazer backup
cp sistema_pecas.db sistema_pecas_backup.db

# Restaurar backup
cp sistema_pecas_backup.db sistema_pecas.db
```

### Migrar Dados

```python
from services import database

# Exportar para outro formato
sistema = database.carregar_sistema_completo()

import json
with open('backup.json', 'w') as f:
    json.dump({
        'pecas_aprovadas': sistema['pecas_aprovadas'],
        'pecas_reprovadas': sistema['pecas_reprovadas'],
        # ... outros dados
    }, f, indent=2)
```

### Análise de Dados

```python
import sqlite3
import pandas as pd

# Carregar em DataFrame
conn = sqlite3.connect('sistema_pecas.db')
df_pecas = pd.read_sql_query("SELECT * FROM pecas", conn)

# Análise
print(df_pecas.describe())
print(df_pecas.groupby('cor').size())
```

## ⚠️ Importante

1. **Sessão Única Global** - Todos usuários/execuções compartilham o mesmo banco
2. **Não Versionar** - O `.db` está no `.gitignore` por design
3. **Backup Regular** - Faça backups do `sistema_pecas.db` se necessário
4. **Não Editar Manualmente** - Use sempre as funções do `database.py`

## 🚀 Performance

- **Inserção:** ~0.001s por peça
- **Carregamento:** ~0.01s para sistema completo
- **Sincronização:** ~0.05s para 100 peças
- **Queries:** Índices automáticos em PRIMARY KEYs

## 📚 Documentação Adicional

- **Arquitetura completa:** [docs/ARQUITETURA.md](ARQUITETURA.md) (Seção "Camada de Persistência SQLite")
- **Testes:** [docs/TESTING.md](TESTING.md)
- **Código:** [services/database.py](../services/database.py)

## 🤝 Contribuindo

Ao adicionar novas features:

1. Atualize o schema se necessário
2. Adicione sincronização automática
3. Escreva testes de persistência
4. Documente mudanças no schema

---

**Desenvolvido por Gabriel Falcão**  
**Data:** 2025-11-16

