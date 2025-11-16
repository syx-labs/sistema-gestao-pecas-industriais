"""
Testes unitários para a camada de persistência SQLite.

Autor: Gabriel Falcão
Data: 2025-11-16
"""

import pytest
import tempfile
import shutil
import sqlite3
from pathlib import Path
from typing import Generator
from unittest.mock import patch

from services import database
from services.armazenamento import SistemaArmazenamento
from models.peca import criar_peca
from models.caixa import criar_caixa


@pytest.fixture
def temp_db() -> Generator[Path, None, None]:
    """
    Fixture que cria um banco de dados temporário para testes.
    Remove o banco após cada teste.
    """
    # Salva o caminho original
    original_db_path = database.DB_PATH
    
    # Cria diretório temporário
    temp_dir = Path(tempfile.mkdtemp())
    temp_db_path = temp_dir / "test_sistema_pecas.db"
    
    # Substitui o caminho do banco
    database.DB_PATH = temp_db_path
    
    yield temp_db_path
    
    # Restaura o caminho original
    database.DB_PATH = original_db_path
    
    # Remove diretório temporário
    shutil.rmtree(temp_dir, ignore_errors=True)


class TestSchemaDatabase:
    """Testes de criação e inicialização do schema."""
    
    def test_criar_schema(self, temp_db: Path) -> None:
        """Testa criação do schema do banco de dados."""
        database.criar_schema()
        
        # Verifica se o arquivo foi criado
        assert temp_db.exists()
        
        # Verifica se as tabelas foram criadas
        with database.get_connection() as conn:
            cursor = conn.cursor()
            
            # Lista todas as tabelas
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )
            tabelas = [row[0] for row in cursor.fetchall()]
            
            assert 'pecas' in tabelas
            assert 'motivos_reprovacao' in tabelas
            assert 'caixas' in tabelas
            assert 'caixas_pecas' in tabelas
            assert 'sistema_config' in tabelas
    
    def test_inicializar_database_idempotente(self, temp_db: Path) -> None:
        """Testa que inicializar_database pode ser chamado múltiplas vezes."""
        database.inicializar_database()
        database.inicializar_database()
        database.inicializar_database()
        
        # Não deve gerar erro
        assert temp_db.exists()
    
    def test_banco_existe(self, temp_db: Path) -> None:
        """Testa função banco_existe."""
        # Antes de criar
        assert not database.banco_existe()
        
        # Cria banco
        database.inicializar_database()
        
        # Depois de criar
        assert database.banco_existe()


class TestPersistenciaPecas:
    """Testes de salvamento e carregamento de peças."""
    
    def test_salvar_peca_aprovada(self, temp_db: Path) -> None:
        """Testa salvamento de peça aprovada."""
        database.inicializar_database()
        
        peca = criar_peca(
            id_peca="P001",
            peso=100.0,
            cor="azul",
            comprimento=15.0,
            aprovada=True,
            motivos_reprovacao=[]
        )
        
        database.salvar_peca(peca)
        
        # Verifica no banco
        with database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM pecas WHERE id = ?", ("P001",))
            row = cursor.fetchone()
            
            assert row is not None
            assert row['id'] == "P001"
            assert row['peso'] == 100.0
            assert row['cor'] == "azul"
            assert row['comprimento'] == 15.0
            assert row['aprovada'] == 1
    
    def test_salvar_peca_reprovada_com_motivos(self, temp_db: Path) -> None:
        """Testa salvamento de peça reprovada com motivos."""
        database.inicializar_database()
        
        peca = criar_peca(
            id_peca="P002",
            peso=120.0,
            cor="vermelho",
            comprimento=25.0,
            aprovada=False,
            motivos_reprovacao=[
                "Peso fora do intervalo",
                "Cor inadequada",
                "Comprimento fora do intervalo"
            ]
        )
        
        database.salvar_peca(peca)
        
        # Verifica peça
        with database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM pecas WHERE id = ?", ("P002",))
            row = cursor.fetchone()
            
            assert row is not None
            assert row['aprovada'] == 0
            
            # Verifica motivos
            cursor.execute(
                "SELECT motivo FROM motivos_reprovacao WHERE peca_id = ?",
                ("P002",)
            )
            motivos = [row['motivo'] for row in cursor.fetchall()]
            
            assert len(motivos) == 3
            assert "Peso fora do intervalo" in motivos
            assert "Cor inadequada" in motivos
            assert "Comprimento fora do intervalo" in motivos
    
    def test_carregar_pecas_vazias(self, temp_db: Path) -> None:
        """Testa carregamento quando não há peças."""
        database.inicializar_database()
        
        aprovadas, reprovadas = database.carregar_pecas()
        
        assert len(aprovadas) == 0
        assert len(reprovadas) == 0
    
    def test_carregar_pecas(self, temp_db: Path) -> None:
        """Testa carregamento de peças."""
        database.inicializar_database()
        
        # Salva peças
        peca_aprovada = criar_peca("P001", 100.0, "azul", 15.0, True, [])
        peca_reprovada = criar_peca(
            "P002", 120.0, "vermelho", 25.0, False,
            ["Peso fora do intervalo"]
        )
        
        database.salvar_peca(peca_aprovada)
        database.salvar_peca(peca_reprovada)
        
        # Carrega
        aprovadas, reprovadas = database.carregar_pecas()
        
        assert len(aprovadas) == 1
        assert len(reprovadas) == 1
        
        assert aprovadas[0]['id'] == "P001"
        assert aprovadas[0]['aprovada'] is True
        
        assert reprovadas[0]['id'] == "P002"
        assert reprovadas[0]['aprovada'] is False
        assert len(reprovadas[0]['motivos_reprovacao']) == 1
    
    def test_atualizar_peca(self, temp_db: Path) -> None:
        """Testa atualização de peça existente."""
        database.inicializar_database()
        
        # Salva peça
        peca = criar_peca("P001", 100.0, "azul", 15.0, True, [])
        database.salvar_peca(peca)
        
        # Atualiza peça
        peca['peso'] = 102.0
        peca['cor'] = "verde"
        database.salvar_peca(peca)
        
        # Verifica
        aprovadas, _ = database.carregar_pecas()
        assert len(aprovadas) == 1
        assert aprovadas[0]['peso'] == 102.0
        assert aprovadas[0]['cor'] == "verde"


class TestPersistenciaCaixas:
    """Testes de salvamento e carregamento de caixas."""
    
    def test_salvar_caixa_vazia(self, temp_db: Path) -> None:
        """Testa salvamento de caixa vazia."""
        database.inicializar_database()
        
        caixa = criar_caixa(1)
        database.salvar_caixa(caixa)
        
        # Verifica
        with database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM caixas WHERE id = ?", (1,))
            row = cursor.fetchone()
            
            assert row is not None
            assert row['id'] == 1
            assert row['fechada'] == 0
    
    def test_salvar_caixa_com_pecas(self, temp_db: Path) -> None:
        """Testa salvamento de caixa com peças."""
        database.inicializar_database()
        
        # Cria peças
        peca1 = criar_peca("P001", 100.0, "azul", 15.0, True, [])
        peca2 = criar_peca("P002", 101.0, "verde", 16.0, True, [])
        
        # Salva peças primeiro
        database.salvar_peca(peca1)
        database.salvar_peca(peca2)
        
        # Cria caixa com peças
        caixa = criar_caixa(1)
        caixa['pecas'] = [peca1, peca2]
        caixa['fechada'] = True
        
        database.salvar_caixa(caixa)
        
        # Verifica relacionamento
        with database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM caixas_pecas WHERE caixa_id = ? ORDER BY ordem",
                (1,)
            )
            rows = cursor.fetchall()
            
            assert len(rows) == 2
            assert rows[0]['peca_id'] == "P001"
            assert rows[0]['ordem'] == 0
            assert rows[1]['peca_id'] == "P002"
            assert rows[1]['ordem'] == 1
    
    def test_carregar_caixas_vazias(self, temp_db: Path) -> None:
        """Testa carregamento quando não há caixas."""
        database.inicializar_database()
        
        caixas_fechadas, caixa_atual, contador = database.carregar_caixas()
        
        assert len(caixas_fechadas) == 0
        assert caixa_atual is not None
        assert caixa_atual['id'] == 1
        assert contador == 1
    
    def test_carregar_caixas(self, temp_db: Path) -> None:
        """Testa carregamento de caixas com peças."""
        database.inicializar_database()
        
        # Salva peças
        peca1 = criar_peca("P001", 100.0, "azul", 15.0, True, [])
        peca2 = criar_peca("P002", 101.0, "verde", 16.0, True, [])
        database.salvar_peca(peca1)
        database.salvar_peca(peca2)
        
        # Salva caixa fechada
        caixa_fechada = criar_caixa(1)
        caixa_fechada['pecas'] = [peca1, peca2]
        caixa_fechada['fechada'] = True
        database.salvar_caixa(caixa_fechada)
        
        # Salva caixa atual
        caixa_atual = criar_caixa(2)
        database.salvar_caixa(caixa_atual)
        
        # Carrega
        caixas_fechadas, caixa_atual_carregada, contador = database.carregar_caixas()
        
        assert len(caixas_fechadas) == 1
        assert caixas_fechadas[0]['id'] == 1
        assert caixas_fechadas[0]['fechada'] is True
        assert len(caixas_fechadas[0]['pecas']) == 2
        
        assert caixa_atual_carregada['id'] == 2
        assert caixa_atual_carregada['fechada'] is False
        assert len(caixa_atual_carregada['pecas']) == 0
        
        assert contador == 2


class TestConfiguracao:
    """Testes de configuração do sistema."""
    
    def test_salvar_config(self, temp_db: Path) -> None:
        """Testa salvamento de configuração."""
        database.inicializar_database()
        
        database.salvar_config("contador_caixas", "5")
        
        # Verifica
        with database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT valor FROM sistema_config WHERE chave = ?",
                ("contador_caixas",)
            )
            row = cursor.fetchone()
            
            assert row is not None
            assert row['valor'] == "5"
    
    def test_carregar_config(self, temp_db: Path) -> None:
        """Testa carregamento de configuração."""
        database.inicializar_database()
        
        database.salvar_config("contador_caixas", "10")
        
        valor = database.carregar_config("contador_caixas")
        assert valor == "10"
    
    def test_carregar_config_inexistente(self, temp_db: Path) -> None:
        """Testa carregamento de configuração que não existe."""
        database.inicializar_database()
        
        valor = database.carregar_config("inexistente", "default")
        assert valor == "default"


class TestSistemaCompleto:
    """Testes de sincronização do sistema completo."""
    
    def test_sincronizar_sistema(self, temp_db: Path) -> None:
        """Testa sincronização completa do sistema."""
        database.inicializar_database()
        
        # Cria sistema
        peca1 = criar_peca("P001", 100.0, "azul", 15.0, True, [])
        peca2 = criar_peca("P002", 120.0, "vermelho", 25.0, False, ["Peso alto"])
        
        caixa_fechada = criar_caixa(1)
        caixa_fechada['pecas'] = [peca1]
        caixa_fechada['fechada'] = True
        
        caixa_atual = criar_caixa(2)
        
        sistema: SistemaArmazenamento = {
            'pecas_aprovadas': [peca1],
            'pecas_reprovadas': [peca2],
            'caixas_fechadas': [caixa_fechada],
            'caixa_atual': caixa_atual,
            'contador_caixas': 2
        }
        
        # Sincroniza
        database.sincronizar_sistema(sistema)
        
        # Verifica peças
        aprovadas, reprovadas = database.carregar_pecas()
        assert len(aprovadas) == 1
        assert len(reprovadas) == 1
        
        # Verifica caixas
        caixas_fechadas, caixa_atual_carregada, contador = database.carregar_caixas()
        assert len(caixas_fechadas) == 1
        assert caixa_atual_carregada['id'] == 2
        assert contador == 2
    
    def test_carregar_sistema_completo(self, temp_db: Path) -> None:
        """Testa carregamento completo do sistema."""
        database.inicializar_database()
        
        # Prepara dados
        peca1 = criar_peca("P001", 100.0, "azul", 15.0, True, [])
        peca2 = criar_peca("P002", 120.0, "vermelho", 25.0, False, ["Peso alto"])
        
        database.salvar_peca(peca1)
        database.salvar_peca(peca2)
        
        caixa = criar_caixa(1)
        caixa['pecas'] = [peca1]
        caixa['fechada'] = False
        database.salvar_caixa(caixa)
        
        database.salvar_config("contador_caixas", "1")
        
        # Carrega sistema
        sistema = database.carregar_sistema_completo()
        
        assert len(sistema['pecas_aprovadas']) == 1
        assert len(sistema['pecas_reprovadas']) == 1
        assert sistema['caixa_atual']['id'] == 1
        assert len(sistema['caixa_atual']['pecas']) == 1
        assert sistema['contador_caixas'] == 1


class TestUtilidades:
    """Testes de funções utilitárias."""
    
    def test_limpar_banco(self, temp_db: Path) -> None:
        """Testa limpeza do banco."""
        database.inicializar_database()
        
        # Adiciona dados
        peca = criar_peca("P001", 100.0, "azul", 15.0, True, [])
        database.salvar_peca(peca)
        
        # Limpa
        database.limpar_banco()
        
        # Verifica que está vazio
        aprovadas, reprovadas = database.carregar_pecas()
        assert len(aprovadas) == 0
        assert len(reprovadas) == 0
    
    def test_remover_banco(self, temp_db: Path) -> None:
        """Testa remoção do arquivo do banco."""
        database.inicializar_database()
        
        assert temp_db.exists()
        
        database.remover_banco()
        
        assert not temp_db.exists()


class TestTransacaoRollback:
    """Testes para cobertura do bloco de rollback em get_connection (linhas 41-43)."""
    
    def test_rollback_em_excecao(self, temp_db: Path) -> None:
        """
        Testa que o rollback é executado quando ocorre exceção durante transação.
        
        Cobre as linhas 41-43 de database.py:
        - except Exception as e:
        -     conn.rollback()
        -     raise e
        """
        database.inicializar_database()
        
        # Força um erro de constraint violation
        with pytest.raises(sqlite3.IntegrityError):
            with database.get_connection() as conn:
                cursor = conn.cursor()
                
                # Insere uma peça
                cursor.execute("""
                    INSERT INTO pecas (id, peso, cor, comprimento, aprovada)
                    VALUES ('P001', 100.0, 'azul', 15.0, 1)
                """)
                
                # Tenta inserir peça com mesmo ID (viola PRIMARY KEY)
                cursor.execute("""
                    INSERT INTO pecas (id, peso, cor, comprimento, aprovada)
                    VALUES ('P001', 101.0, 'verde', 16.0, 1)
                """)
        
        # Verifica que o rollback foi executado
        # A primeira peça NÃO deve estar no banco (foi revertida)
        with database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM pecas")
            count = cursor.fetchone()[0]
            assert count == 0  # Nenhuma peça foi salva devido ao rollback
    
    def test_rollback_preserva_dados_anteriores(self, temp_db: Path) -> None:
        """
        Testa que rollback não afeta transações já commitadas.
        """
        database.inicializar_database()
        
        # Salva uma peça com sucesso
        peca1 = criar_peca("P001", 100.0, "azul", 15.0, True, [])
        database.salvar_peca(peca1)
        
        # Tenta operação que falha
        with pytest.raises(sqlite3.IntegrityError):
            with database.get_connection() as conn:
                cursor = conn.cursor()
                
                # Insere peça que conflita com P001
                cursor.execute("""
                    INSERT INTO pecas (id, peso, cor, comprimento, aprovada)
                    VALUES ('P001', 102.0, 'verde', 17.0, 1)
                """)
        
        # Verifica que a primeira peça ainda existe
        aprovadas, _ = database.carregar_pecas()
        assert len(aprovadas) == 1
        assert aprovadas[0]['id'] == "P001"
        assert aprovadas[0]['peso'] == 100.0  # Dados originais preservados
    
    def test_rollback_com_foreign_key_violation(self, temp_db: Path) -> None:
        """
        Testa rollback quando há violação de foreign key.
        """
        database.inicializar_database()
        
        # Tenta inserir motivo de reprovação para peça inexistente
        with pytest.raises(sqlite3.IntegrityError):
            with database.get_connection() as conn:
                cursor = conn.cursor()
                
                # Habilita foreign keys
                cursor.execute("PRAGMA foreign_keys = ON")
                
                # Tenta inserir motivo para peça que não existe
                cursor.execute("""
                    INSERT INTO motivos_reprovacao (peca_id, motivo)
                    VALUES ('P999', 'Motivo qualquer')
                """)
        
        # Verifica que nada foi inserido
        with database.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM motivos_reprovacao")
            count = cursor.fetchone()[0]
            assert count == 0

