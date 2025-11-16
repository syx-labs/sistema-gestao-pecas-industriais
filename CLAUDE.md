# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Sistema de Automação Digital para Gestão de Peças Industriais - An industrial parts quality control system with both CLI and web interfaces. Developed as an academic project demonstrating clean architecture principles, type safety, and modern Python development practices.

## Development Commands

### Running the Application

**CLI Interface:**
```bash
python3 main.py
```

**Web Interface (Streamlit):**
```bash
streamlit run streamlit_app.py
# or using the convenience script
./run_visual.sh
```

The Streamlit app runs on `http://localhost:8501` by default.

### Environment Setup

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

### Dependencies

Core dependencies are minimal:
- `streamlit>=1.28.0` - Web interface framework
- `plotly>=5.17.0` - Interactive charts
- `pandas>=2.0.0` - Data manipulation

The CLI interface has no external dependencies - uses Python stdlib only.

### Testing

**Run Tests:**
```bash
# Activate virtual environment
source venv/bin/activate

# Install test dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run with coverage report
pytest --cov=services --cov=models --cov-report=term-missing

# Run only unit tests
pytest tests/unit/

# Run only integration tests
pytest tests/integration/
```

**Test Statistics:**
- Total tests: 207
- Code coverage: 99%
- Execution time: ~0.12s

See [TESTING.md](TESTING.md) for detailed testing guide.

## Architecture

The codebase follows **Clean Architecture** with clear separation of concerns:

```
models/          # Data structures (TypedDict-based)
├── peca.py      # Peca (piece) model with factory function
└── caixa.py     # Caixa (box) model with capacity management

services/        # Business logic layer
├── validacao.py       # Quality validation rules (weight, color, length)
├── armazenamento.py   # Storage system with box management
└── relatorio.py       # Report generation and statistics

utils/           # User interface layer
└── menu.py      # CLI menu and interaction handlers

main.py              # CLI entry point
streamlit_app.py     # Web UI entry point
```

### Key Architectural Decisions

**TypedDict over Classes:**
- Uses `TypedDict` for type safety without class complexity
- Easier serialization (prepared for JSON/database integration)
- Clear type hints throughout the codebase

**Factory Functions:**
- `criar_peca()` in models/peca.py
- `criar_caixa()` in models/caixa.py
- Centralized object creation with defaults

**Single Responsibility:**
- Each validation function handles one criterion
- Validation rules centralized as constants in services/validacao.py

## Business Logic

### Quality Criteria (services/validacao.py)

Peças (pieces) are validated against three criteria - ALL must pass:

```python
PESO_MINIMO = 95.0          # grams
PESO_MAXIMO = 105.0         # grams
CORES_ACEITAS = ['azul', 'verde']
COMPRIMENTO_MINIMO = 10.0   # cm
COMPRIMENTO_MAXIMO = 20.0   # cm
```

### Storage System (services/armazenamento.py)

- Approved pieces are added to boxes (caixas)
- Box capacity: `CAPACIDADE_MAXIMA_CAIXA = 10` pieces
- Boxes automatically close when full
- New box is created immediately after closing

**System State Structure:**
```python
SistemaArmazenamento = {
    'pecas_aprovadas': List[Peca],
    'pecas_reprovadas': List[Peca],
    'caixas_fechadas': List[Caixa],
    'caixa_atual': Caixa,
    'contador_caixas': int
}
```

### Validation Flow

1. Piece is created with `criar_peca()`
2. `validar_peca()` checks all three criteria
3. Returns tuple: `(aprovada: bool, motivos: List[str])`
4. If approved → added to box via `adicionar_peca_em_caixa()`
5. If rejected → added to `pecas_reprovadas` with reasons

## Type Safety

All data structures use `TypedDict` with full type annotations:
- Function signatures have complete type hints
- Return types are explicit (including tuples)
- Uses modern Python union syntax: `List[str] | None`

## State Management

**CLI (main.py):**
- Single `sistema` object passed through all interface functions
- State managed imperatively in memory

**Streamlit (streamlit_app.py):**
- Uses `st.session_state` for persistence
- State initialized on first run
- Reset functionality available via sidebar

## Interface Layers

### CLI (utils/menu.py)
Functions follow pattern: `*_interface(sistema: SistemaArmazenamento)`
- `cadastrar_peca_interface()` - Input validation and piece registration
- `listar_pecas_interface()` - Display approved/rejected pieces
- `remover_peca_interface()` - Remove by ID
- `listar_caixas_interface()` - Show current and closed boxes
- `gerar_relatorio_interface()` - Generate statistics report

### Web (streamlit_app.py)
- Sidebar navigation with emoji icons
- Real-time dashboard with Plotly charts
- Form-based piece registration with sliders
- Interactive tables with pandas
- Reset system button in sidebar

## Code Style

- Docstrings follow Google style with Args/Returns sections
- Functions are small and focused (SRP)
- Constants in UPPER_CASE at module level
- Type hints on all functions
- No global mutable state (except Streamlit session_state)

## Testing

The project has comprehensive test coverage (99%) with 207 tests:

**Test Structure:**
```
tests/
├── unit/                    # 174 tests (84%)
│   ├── test_validacao.py   # Quality validation
│   ├── test_armazenamento.py # Box management
│   ├── test_relatorio.py   # Report generation
│   └── test_models.py      # Data models
└── integration/             # 33 tests (16%)
    ├── test_workflow_completo.py   # End-to-end workflows
    └── test_cenarios_reais.py      # Real-world scenarios
```

**What's Tested:**
- All quality criteria (weight, color, length)
- Box closure at capacity (10 pieces)
- Automatic new box creation
- Report generation with statistics
- Edge cases and boundary values
- Real-world production scenarios

**Key Fixtures:**
- `sistema_vazio` - Empty system
- `sistema_com_pecas_aprovadas` - System with approved pieces
- `sistema_com_multiplas_caixas` - System with multiple closed boxes
- `peca_valida`, `peca_peso_invalido`, etc. - Various piece states

Run `pytest -v` for detailed test output.

## Notes for Future Development

- System currently has no persistence (in-memory only)
- IDs are strings - no uniqueness enforcement in code
- No authentication/authorization (designed for single user)
- Streamlit state resets on server restart
- Color validation is case-insensitive but preserves original input
