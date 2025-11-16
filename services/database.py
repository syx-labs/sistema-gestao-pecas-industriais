"""
Camada de persistência SQLite para o Sistema de Gestão de Peças.

Implementa schema normalizado (3NF) com sincronização automática e transparente,
mantendo total compatibilidade com o código existente.

Autor: Gabriel Falcão
Data: 2025-11-16
"""

import sqlite3
from pathlib import Path
from typing import List, Optional, Tuple, TYPE_CHECKING
from contextlib import contextmanager

from models.peca import Peca, criar_peca
from models.caixa import Caixa, criar_caixa

# Importação condicional para evitar importação circular
if TYPE_CHECKING:
    from services.armazenamento import SistemaArmazenamento


# Caminho do banco de dados na raiz do projeto
DB_PATH = Path(__file__).parent.parent / "sistema_pecas.db"


@contextmanager
def get_connection():
    """
    Context manager para gerenciar conexões com o banco de dados.
    
    Yields:
        sqlite3.Connection: Conexão com o banco de dados
    """
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row  # Permite acessar colunas por nome
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def criar_schema() -> None:
    """
    Cria o schema do banco de dados (tabelas e relacionamentos).
    Usa schema normalizado (3NF) para garantir integridade dos dados.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Tabela de Peças
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pecas (
                id TEXT PRIMARY KEY,
                peso REAL NOT NULL,
                cor TEXT NOT NULL,
                comprimento REAL NOT NULL,
                aprovada BOOLEAN NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabela de Motivos de Reprovação
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS motivos_reprovacao (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                peca_id TEXT NOT NULL,
                motivo TEXT NOT NULL,
                FOREIGN KEY (peca_id) REFERENCES pecas(id) ON DELETE CASCADE
            )
        """)
        
        # Tabela de Caixas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS caixas (
                id INTEGER PRIMARY KEY,
                fechada BOOLEAN NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabela Associativa Caixas-Peças
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS caixas_pecas (
                caixa_id INTEGER NOT NULL,
                peca_id TEXT NOT NULL,
                ordem INTEGER NOT NULL,
                PRIMARY KEY (caixa_id, peca_id),
                FOREIGN KEY (caixa_id) REFERENCES caixas(id) ON DELETE CASCADE,
                FOREIGN KEY (peca_id) REFERENCES pecas(id) ON DELETE CASCADE
            )
        """)
        
        # Tabela de Configuração do Sistema
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sistema_config (
                chave TEXT PRIMARY KEY,
                valor TEXT NOT NULL
            )
        """)
        
        # Habilita foreign keys (desabilitado por padrão no SQLite)
        cursor.execute("PRAGMA foreign_keys = ON")


def inicializar_database() -> None:
    """
    Inicializa o banco de dados criando o schema se necessário.
    Safe para chamar múltiplas vezes (idempotente).
    """
    criar_schema()


def banco_existe() -> bool:
    """
    Verifica se o banco de dados já existe.
    
    Returns:
        True se o arquivo do banco existe, False caso contrário
    """
    return DB_PATH.exists()


def salvar_peca(peca: Peca) -> None:
    """
    Salva ou atualiza uma peça no banco de dados.
    
    Args:
        peca: Peça a ser salva
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Insere ou substitui a peça
        cursor.execute("""
            INSERT OR REPLACE INTO pecas (id, peso, cor, comprimento, aprovada)
            VALUES (?, ?, ?, ?, ?)
        """, (
            peca['id'],
            peca['peso'],
            peca['cor'],
            peca['comprimento'],
            int(peca['aprovada'])  # SQLite não tem boolean nativo
        ))
        
        # Remove motivos antigos (se existirem)
        cursor.execute("DELETE FROM motivos_reprovacao WHERE peca_id = ?", (peca['id'],))
        
        # Insere novos motivos de reprovação
        for motivo in peca['motivos_reprovacao']:
            cursor.execute("""
                INSERT INTO motivos_reprovacao (peca_id, motivo)
                VALUES (?, ?)
            """, (peca['id'], motivo))


def deletar_peca(id_peca: str) -> None:
    """
    Remove uma peça do banco de dados.
    
    Args:
        id_peca: ID da peça a ser removida
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Remove da tabela caixas_pecas primeiro (foreign key)
        cursor.execute("DELETE FROM caixas_pecas WHERE peca_id = ?", (id_peca,))
        
        # Remove motivos de reprovação (CASCADE já faz isso, mas por segurança)
        cursor.execute("DELETE FROM motivos_reprovacao WHERE peca_id = ?", (id_peca,))
        
        # Remove a peça
        cursor.execute("DELETE FROM pecas WHERE id = ?", (id_peca,))


def carregar_pecas() -> Tuple[List[Peca], List[Peca]]:
    """
    Carrega todas as peças do banco de dados.
    
    Returns:
        Tupla (pecas_aprovadas, pecas_reprovadas)
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Carrega todas as peças
        cursor.execute("SELECT * FROM pecas")
        rows = cursor.fetchall()
        
        pecas_aprovadas: List[Peca] = []
        pecas_reprovadas: List[Peca] = []
        
        for row in rows:
            # Carrega motivos de reprovação
            cursor.execute(
                "SELECT motivo FROM motivos_reprovacao WHERE peca_id = ?",
                (row['id'],)
            )
            motivos = [m['motivo'] for m in cursor.fetchall()]
            
            # Cria objeto Peca
            peca = criar_peca(
                id_peca=row['id'],
                peso=row['peso'],
                cor=row['cor'],
                comprimento=row['comprimento'],
                aprovada=bool(row['aprovada']),
                motivos_reprovacao=motivos
            )
            
            # Adiciona na lista apropriada
            if peca['aprovada']:
                pecas_aprovadas.append(peca)
            else:
                pecas_reprovadas.append(peca)
        
        return pecas_aprovadas, pecas_reprovadas


def salvar_caixa(caixa: Caixa) -> None:
    """
    Salva ou atualiza uma caixa no banco de dados.
    
    Args:
        caixa: Caixa a ser salva
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Insere ou substitui a caixa
        cursor.execute("""
            INSERT OR REPLACE INTO caixas (id, fechada)
            VALUES (?, ?)
        """, (caixa['id'], int(caixa['fechada'])))
        
        # Remove associações antigas
        cursor.execute("DELETE FROM caixas_pecas WHERE caixa_id = ?", (caixa['id'],))
        
        # Insere peças da caixa
        for ordem, peca in enumerate(caixa['pecas']):
            cursor.execute("""
                INSERT INTO caixas_pecas (caixa_id, peca_id, ordem)
                VALUES (?, ?, ?)
            """, (caixa['id'], peca['id'], ordem))


def carregar_caixas() -> Tuple[List[Caixa], Caixa, int]:
    """
    Carrega todas as caixas do banco de dados.
    
    Returns:
        Tupla (caixas_fechadas, caixa_atual, contador_caixas)
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Carrega todas as caixas
        cursor.execute("SELECT * FROM caixas ORDER BY id")
        rows = cursor.fetchall()
        
        caixas_fechadas: List[Caixa] = []
        caixa_atual: Optional[Caixa] = None
        contador_caixas = 0
        
        for row in rows:
            # Carrega peças da caixa
            cursor.execute("""
                SELECT p.*, cp.ordem
                FROM pecas p
                JOIN caixas_pecas cp ON p.id = cp.peca_id
                WHERE cp.caixa_id = ?
                ORDER BY cp.ordem
            """, (row['id'],))
            
            pecas_rows = cursor.fetchall()
            pecas: List[Peca] = []
            
            for peca_row in pecas_rows:
                # Carrega motivos (geralmente vazio para aprovadas)
                cursor.execute(
                    "SELECT motivo FROM motivos_reprovacao WHERE peca_id = ?",
                    (peca_row['id'],)
                )
                motivos = [m['motivo'] for m in cursor.fetchall()]
                
                peca = criar_peca(
                    id_peca=peca_row['id'],
                    peso=peca_row['peso'],
                    cor=peca_row['cor'],
                    comprimento=peca_row['comprimento'],
                    aprovada=bool(peca_row['aprovada']),
                    motivos_reprovacao=motivos
                )
                pecas.append(peca)
            
            # Cria objeto Caixa
            caixa = criar_caixa(row['id'])
            caixa['pecas'] = pecas
            caixa['fechada'] = bool(row['fechada'])
            
            # Adiciona na lista apropriada
            if caixa['fechada']:
                caixas_fechadas.append(caixa)
            else:
                caixa_atual = caixa
            
            # Atualiza contador
            if row['id'] > contador_caixas:
                contador_caixas = row['id']
        
        # Se não há caixa atual, cria uma nova
        if caixa_atual is None:
            contador_caixas += 1
            caixa_atual = criar_caixa(contador_caixas)
        
        return caixas_fechadas, caixa_atual, contador_caixas


def salvar_config(chave: str, valor: str) -> None:
    """
    Salva uma configuração do sistema.
    
    Args:
        chave: Nome da configuração
        valor: Valor da configuração
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO sistema_config (chave, valor)
            VALUES (?, ?)
        """, (chave, valor))


def carregar_config(chave: str, default: str = "") -> str:
    """
    Carrega uma configuração do sistema.
    
    Args:
        chave: Nome da configuração
        default: Valor padrão se não existir
    
    Returns:
        Valor da configuração
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT valor FROM sistema_config WHERE chave = ?",
            (chave,)
        )
        row = cursor.fetchone()
        return row['valor'] if row else default


def carregar_sistema_completo():
    """
    Carrega o sistema completo do banco de dados.
    
    Returns:
        SistemaArmazenamento completo com todas as peças, caixas e configurações
    """
    # Import local para evitar circular import
    from services.armazenamento import SistemaArmazenamento
    
    # Carrega peças
    pecas_aprovadas, pecas_reprovadas = carregar_pecas()
    
    # Carrega caixas
    caixas_fechadas, caixa_atual, contador_caixas = carregar_caixas()
    
    # Reconstrói o SistemaArmazenamento
    sistema = SistemaArmazenamento(
        pecas_aprovadas=pecas_aprovadas,
        pecas_reprovadas=pecas_reprovadas,
        caixas_fechadas=caixas_fechadas,
        caixa_atual=caixa_atual,
        contador_caixas=contador_caixas
    )
    
    return sistema


def sincronizar_sistema(sistema) -> None:
    """
    Sincroniza o estado completo do sistema com o banco de dados.
    Salva todas as peças, caixas e configurações.
    
    Args:
        sistema: Sistema a ser sincronizado (SistemaArmazenamento)
    """
    # Primeiro, identifica peças que existem no sistema
    ids_sistema = set()
    for peca in sistema['pecas_aprovadas']:
        ids_sistema.add(peca['id'])
        salvar_peca(peca)
    
    for peca in sistema['pecas_reprovadas']:
        ids_sistema.add(peca['id'])
        salvar_peca(peca)
    
    # Remove peças do banco que não estão mais no sistema
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM pecas")
        ids_banco = {row['id'] for row in cursor.fetchall()}
        
        ids_para_remover = ids_banco - ids_sistema
        for id_peca in ids_para_remover:
            deletar_peca(id_peca)
    
    # Salva todas as caixas fechadas
    for caixa in sistema['caixas_fechadas']:
        salvar_caixa(caixa)
    
    # Salva a caixa atual
    salvar_caixa(sistema['caixa_atual'])
    
    # Salva configurações do sistema
    salvar_config('contador_caixas', str(sistema['contador_caixas']))


def limpar_banco() -> None:
    """
    Remove todos os dados do banco (útil para testes).
    Mantém o schema intacto.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM caixas_pecas")
        cursor.execute("DELETE FROM motivos_reprovacao")
        cursor.execute("DELETE FROM pecas")
        cursor.execute("DELETE FROM caixas")
        cursor.execute("DELETE FROM sistema_config")


def remover_banco() -> None:
    """
    Remove o arquivo do banco de dados completamente.
    Útil para reset completo do sistema.
    """
    if DB_PATH.exists():
        DB_PATH.unlink()

