# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an **Industrial Parts Quality Control System** - an academic project for automating quality validation, storage management, and reporting of manufactured parts in production lines. Built with Python 3.14+, it features both CLI and Streamlit web interfaces with SQLite persistence.

## Development Commands

### Running the Application

```bash
# CLI interface (terminal-based)
python3 main.py

# Web interface (Streamlit)
streamlit run streamlit_app.py
# Opens automatically at http://localhost:8501

# Alternative with bun
bun run streamlit run streamlit_app.py
```

### Testing

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=services --cov=models --cov-report=term-missing

# Run specific test file
pytest tests/unit/test_validacao.py

# Run specific test function
pytest tests/unit/test_validacao.py::test_validar_peso_valido

# Run tests in parallel
pytest -n auto

# Run integration tests only
pytest tests/integration/

# Run unit tests only
pytest tests/unit/

# Generate HTML coverage report
pytest --cov=services --cov=models --cov-report=html
# View at htmlcov/index.html
```

### Database Management

```bash
# Database file location: sistema_pecas.db (auto-created on first run)
# Note: *.db files are gitignored

# To reset the database, simply delete it:
rm sistema_pecas.db

# Test persistence functionality
python3 test_persistencia.py
```

### Development Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux

# Install runtime dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt

# Install all dependencies at once
pip install -r requirements.txt -r requirements-dev.txt
```

## Architecture Overview

The codebase follows **Clean Architecture** principles with strict separation of concerns:

```
┌─────────────────────────────────────────────────────┐
│  INTERFACES (CLI + Web)                             │
│  - main.py: CLI entry point                         │
│  - streamlit_app.py: Web dashboard                  │
│  - utils/menu.py: User interaction helpers          │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│  SERVICES (Business Logic)                          │
│  - validacao.py: Quality control rules              │
│  - armazenamento.py: Box management + DB sync       │
│  - database.py: SQLite persistence layer            │
│  - relatorio.py: Statistics & reports               │
└─────────────────┬───────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────┐
│  MODELS (Data Structures)                           │
│  - peca.py: Part structure (TypedDict)              │
│  - caixa.py: Box structure (TypedDict)              │
└─────────────────────────────────────────────────────┘
```

### Key Design Decisions

1. **TypedDict over Classes**: Uses Python's `TypedDict` for data structures instead of classes for simplicity, type safety, and easy JSON serialization.

2. **Functional Programming**: Pure functions with no hidden state. Each validation function (`validar_peso`, `validar_cor`, `validar_comprimento`) follows Single Responsibility Principle.

3. **Transparent Persistence**: SQLite integration is completely transparent - existing code works unchanged. All database operations are auto-synced through `services/armazenamento.py`.

4. **Normalized Database (3NF)**:
   - `pecas` table (main parts data)
   - `motivos_reprovacao` table (1:N relationship)
   - `caixas` and `caixas_pecas` tables (N:M relationship)
   - Foreign keys with CASCADE for referential integrity

## Critical Business Rules

**Quality Validation Criteria** (defined in `services/validacao.py`):
- Weight: 95.0g - 105.0g
- Color: Only "azul" (blue) or "verde" (green) - case insensitive
- Length: 10.0cm - 20.0cm

A part is **approved** if ALL criteria pass. If ANY criterion fails, it's **rejected** with specific reasons logged.

**Box Management Logic** (in `services/armazenamento.py`):
- Box capacity: 10 parts (constant: `CAPACIDADE_MAXIMA_CAIXA`)
- When 10th part is added:
  1. Current box is marked as `fechada=True`
  2. Box moves to `caixas_fechadas` list
  3. New box auto-created with incremented ID
  4. System state synced to database

**System State Structure** (`SistemaArmazenamento` TypedDict):
```python
{
    'pecas_aprovadas': [],      # All approved parts
    'pecas_reprovadas': [],     # All rejected parts (with reasons)
    'caixas_fechadas': [],      # Completed boxes (10 parts each)
    'caixa_atual': Caixa,       # Currently filling box
    'contador_caixas': int      # Next box ID
}
```

## Testing Strategy

The project has **comprehensive test coverage** with 208+ tests:

**Unit Tests** (`tests/unit/`):
- `test_validacao.py`: Each validation criterion in isolation
- `test_armazenamento.py`: Box logic, system initialization
- `test_database.py`: Database operations (CRUD)
- `test_models.py`: Data structure creation
- `test_relatorio.py`: Statistical calculations

**Integration Tests** (`tests/integration/`):
- `test_workflow_completo.py`: End-to-end workflows
- `test_cenarios_reais.py`: Real production scenarios
- `test_database_integration.py`: Persistence across sessions

**Shared Fixtures** (`tests/conftest.py`):
- Pre-configured parts (valid, invalid weight/color/length)
- Box fixtures (empty, almost full, full)
- System fixtures (empty, with parts, multiple boxes)
- Extensive reusable test data

## Database Persistence

**Auto-Sync Behavior**:
- Database file: `sistema_pecas.db` (created automatically)
- Every state-changing operation triggers `database.sincronizar_sistema()`
- Operations that sync: add part to box, remove part, close box, create box
- First run: Creates schema + empty system
- Subsequent runs: Loads persisted state seamlessly

**Schema Highlights**:
- All tables use appropriate constraints (NOT NULL, FOREIGN KEY)
- `ON DELETE CASCADE` prevents orphaned records
- `created_at` timestamps for audit trail
- `sistema_config` table for system-wide settings

**Key Functions in `services/database.py`**:
- `inicializar_database()`: Creates schema (idempotent)
- `sincronizar_sistema()`: Saves complete system state
- `carregar_sistema_completo()`: Loads complete system state
- `salvar_peca()` / `carregar_pecas()`: Part persistence
- `salvar_caixa()` / `carregar_caixas()`: Box persistence

## Code Patterns to Follow

1. **Constants at Module Level**: All validation thresholds are constants in `services/validacao.py`:
   ```python
   PESO_MINIMO = 95.0
   PESO_MAXIMO = 105.0
   CORES_ACEITAS = ['azul', 'verde']
   ```

2. **Factory Functions**: Use `criar_peca()` and `criar_caixa()` instead of dict literals:
   ```python
   # Good
   peca = criar_peca("P001", 100.0, "azul", 15.0)

   # Avoid
   peca = {'id': 'P001', ...}  # Missing type safety
   ```

3. **Validation Pattern**: All validators return `Tuple[bool, str]`:
   ```python
   def validar_X(valor) -> Tuple[bool, str]:
       if valid:
           return True, ""
       return False, "Reason for failure"
   ```

4. **Database Transparency**: Never call database functions directly from interfaces. Always go through `services/armazenamento.py` which handles sync automatically.

## Common Development Tasks

**Adding a new validation criterion**:
1. Add constant in `services/validacao.py`
2. Create `validar_X()` function returning `Tuple[bool, str]`
3. Call it in `validar_peca()` and collect results
4. Add tests in `tests/unit/test_validacao.py`
5. Update `test_cenarios_reais.py` if needed

**Modifying database schema**:
1. Update table definitions in `services/database.py::inicializar_database()`
2. Add corresponding save/load logic
3. Update `sincronizar_sistema()` and `carregar_sistema_completo()`
4. Add migration logic if changing existing schema
5. Update all tests in `tests/unit/test_database.py`

**Adding a new report metric**:
1. Add calculation function in `services/relatorio.py`
2. Update `gerar_relatorio_completo()` to include new metric
3. Update Streamlit dashboard in `streamlit_app.py` if applicable
4. Add tests in `tests/unit/test_relatorio.py`

## Streamlit UI Structure

The web interface (`streamlit_app.py`) has these main sections:
- **Dashboard**: Real-time metrics, charts (pie, bar, histogram using Plotly)
- **Cadastro**: Part registration form
- **Listagem**: View approved/rejected parts
- **Caixas**: Monitor box filling progress
- **Relatórios**: Comprehensive statistics

**Theme Configuration**: `.streamlit/config.toml` (Dark mode by default)

## Important Files by Line Count

- `services/database.py`: ~420 lines (persistence layer)
- `streamlit_app.py`: ~400 lines (web UI)
- `services/armazenamento.py`: ~208 lines (box management)
- `services/relatorio.py`: ~140 lines (reporting)
- `services/validacao.py`: ~104 lines (quality rules)
- `main.py`: ~78 lines (CLI entry)
- `models/peca.py`: ~58 lines (part structure)
- `models/caixa.py`: ~43 lines (box structure)

## Dependencies

**Runtime** (`requirements.txt`):
- streamlit >= 1.37.0
- plotly >= 5.17.0
- pandas >= 2.0.0
- rich >= 13.7.0

**Development** (`requirements-dev.txt`):
- pytest >= 7.4.0
- pytest-cov >= 4.1.0
- pytest-mock >= 3.11.0
- pytest-xdist >= 3.3.0
- hypothesis >= 6.82.0

## Rich TUI Framework

The CLI interface uses **Rich** - a Python library for beautiful terminal output. Rich provides the "lipgloss quality" styling with:

### Rich Components Used

**Panels** (`rich.panel.Panel`): Bordered boxes for sections and titles
- Menu principal com bordas arredondadas
- Headers de seções (Cadastrar, Listar, etc.)
- Banner de boas-vindas e despedida

**Tables** (`rich.table.Table`): Styled tables with colors
- Listagem de peças aprovadas (border verde)
- Listagem de peças reprovadas com motivos (border vermelha, show_lines=True)
- Opções do menu

**Console** (`rich.console.Console`): Unified output with theme
- Singleton global em `utils/rich_styles.py`
- Tema customizado com cores consistentes
- Funções helper para formatação (formatar_sucesso, formatar_erro, etc.)

**Progress Bars**: Visual progress indicators
- Caixas em preenchimento (X/10 peças)
- Barra visual com caracteres █ e ░

### Styling System

All styles centralized in `utils/rich_styles.py`:
- **SISTEMA_THEME**: Custom theme with semantic colors
- **Box styles**: ROUNDED, DOUBLE, SIMPLE_HEAD for different components
- **Icons**: Emojis for visual consistency (🏭, 📦, ✅, ❌, etc.)
- **Helper functions**: formatar_sucesso(), formatar_erro(), formatar_peca_id(), etc.

### Usage Pattern

```python
from utils.rich_styles import console, formatar_sucesso, ICON_FABRICA

# Print with console (not print())
console.print(formatar_sucesso("Operação concluída!"))

# Create panels
from rich.panel import Panel
panel = Panel("Conteúdo", title="Título", border_style="blue")
console.print(panel)

# Create tables
from rich.table import Table
table = Table(title="Dados")
table.add_column("ID", style="cyan")
table.add_row("P001")
console.print(table)
```

### Important Notes

- **Always use `console.print()`** instead of `print()` for Rich components
- **Styling uses markup**: `[bold red]text[/bold red]`, `[cyan]text[/cyan]`
- **Console is a singleton**: Imported from `utils/rich_styles.py`
- **Fallback safe**: If Rich not available, system still works (inputs use standard input())

## Python Version

Requires **Python 3.8+** (developed with Python 3.14)

## Documentation

For comprehensive architecture details, see:
- `README.md`: User-facing documentation, examples, motivation
- `docs/ARQUITETURA.md`: Deep-dive into architecture decisions, diagrams, design patterns, persistence layer explanation
