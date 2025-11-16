"""
Testes de integração para validar persistência do sistema entre execuções.

Autor: Gabriel Falcão
Data: 2025-11-16
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from typing import Generator

from services import database
from services.armazenamento import (
    inicializar_sistema,
    adicionar_peca_em_caixa,
    remover_peca_por_id,
    SistemaArmazenamento
)
from services.validacao import validar_peca
from models.peca import criar_peca
from models.caixa import CAPACIDADE_MAXIMA_CAIXA


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


class TestPersistenciaEntreExecucoes:
    """Testa que dados persistem entre múltiplas execuções do sistema."""
    
    def test_sistema_vazio_cria_banco(self, temp_db: Path) -> None:
        """Primeira execução cria banco vazio."""
        sistema = inicializar_sistema()
        
        assert temp_db.exists()
        assert len(sistema['pecas_aprovadas']) == 0
        assert len(sistema['pecas_reprovadas']) == 0
        assert len(sistema['caixas_fechadas']) == 0
        assert sistema['caixa_atual']['id'] == 1
        assert sistema['contador_caixas'] == 1
    
    def test_pecas_persistem_entre_execucoes(self, temp_db: Path) -> None:
        """Peças cadastradas devem persistir entre execuções."""
        # Primeira execução - cadastra peças
        sistema1 = inicializar_sistema()
        
        peca1 = criar_peca("P001", 100.0, "azul", 15.0)
        aprovada, motivos = validar_peca(peca1)
        peca1['aprovada'] = aprovada
        peca1['motivos_reprovacao'] = motivos
        
        adicionar_peca_em_caixa(peca1, sistema1)
        
        peca2 = criar_peca("P002", 120.0, "vermelho", 25.0)
        aprovada, motivos = validar_peca(peca2)
        peca2['aprovada'] = aprovada
        peca2['motivos_reprovacao'] = motivos
        sistema1['pecas_reprovadas'].append(peca2)
        database.sincronizar_sistema(sistema1)
        
        # Segunda execução - carrega peças
        sistema2 = inicializar_sistema()
        
        assert len(sistema2['pecas_aprovadas']) == 1
        assert len(sistema2['pecas_reprovadas']) == 1
        assert sistema2['pecas_aprovadas'][0]['id'] == "P001"
        assert sistema2['pecas_reprovadas'][0]['id'] == "P002"
    
    def test_caixas_persistem_entre_execucoes(self, temp_db: Path) -> None:
        """Caixas fechadas devem persistir entre execuções."""
        # Primeira execução - preenche uma caixa
        sistema1 = inicializar_sistema()
        
        # Adiciona 10 peças para fechar uma caixa
        for i in range(CAPACIDADE_MAXIMA_CAIXA):
            peca = criar_peca(f"P{i:03d}", 100.0, "azul", 15.0, True)
            adicionar_peca_em_caixa(peca, sistema1)
        
        assert len(sistema1['caixas_fechadas']) == 1
        assert sistema1['contador_caixas'] == 2
        
        # Segunda execução - verifica caixa fechada
        sistema2 = inicializar_sistema()
        
        assert len(sistema2['caixas_fechadas']) == 1
        assert len(sistema2['caixas_fechadas'][0]['pecas']) == 10
        assert sistema2['caixas_fechadas'][0]['fechada'] is True
        assert sistema2['contador_caixas'] == 2
    
    def test_contador_caixas_persiste(self, temp_db: Path) -> None:
        """Contador de caixas deve persistir entre execuções."""
        # Primeira execução
        sistema1 = inicializar_sistema()
        assert sistema1['contador_caixas'] == 1
        
        # Adiciona 15 peças (fecha 1 caixa e inicia outra)
        for i in range(15):
            peca = criar_peca(f"P{i:03d}", 100.0, "azul", 15.0, True)
            adicionar_peca_em_caixa(peca, sistema1)
        
        assert sistema1['contador_caixas'] == 2
        
        # Segunda execução
        sistema2 = inicializar_sistema()
        assert sistema2['contador_caixas'] == 2
        
        # Adiciona mais 10 peças (fecha segunda caixa)
        for i in range(15, 25):
            peca = criar_peca(f"P{i:03d}", 100.0, "azul", 15.0, True)
            adicionar_peca_em_caixa(peca, sistema2)
        
        assert sistema2['contador_caixas'] == 3
        
        # Terceira execução
        sistema3 = inicializar_sistema()
        assert sistema3['contador_caixas'] == 3


class TestWorkflowCompleto:
    """Testa workflows completos com persistência."""
    
    def test_workflow_producao_completa(self, temp_db: Path) -> None:
        """Simula workflow completo de produção com persistência."""
        # Dia 1 - Produção inicial
        sistema_dia1 = inicializar_sistema()
        
        # Cadastra 5 peças aprovadas
        for i in range(5):
            peca = criar_peca(f"P{i:03d}", 100.0, "azul", 15.0, True)
            adicionar_peca_em_caixa(peca, sistema_dia1)
        
        # Cadastra 2 peças reprovadas
        for i in range(5, 7):
            peca = criar_peca(f"P{i:03d}", 120.0, "vermelho", 25.0, False, ["Fora do padrão"])
            sistema_dia1['pecas_reprovadas'].append(peca)
            database.sincronizar_sistema(sistema_dia1)
        
        # Dia 2 - Continua produção
        sistema_dia2 = inicializar_sistema()
        
        assert len(sistema_dia2['pecas_aprovadas']) == 5
        assert len(sistema_dia2['pecas_reprovadas']) == 2
        assert len(sistema_dia2['caixa_atual']['pecas']) == 5
        
        # Adiciona mais 5 peças (completa primeira caixa)
        for i in range(7, 12):
            peca = criar_peca(f"P{i:03d}", 100.0, "verde", 15.0, True)
            adicionar_peca_em_caixa(peca, sistema_dia2)
        
        assert len(sistema_dia2['caixas_fechadas']) == 1
        assert sistema_dia2['contador_caixas'] == 2
        
        # Dia 3 - Verifica tudo
        sistema_dia3 = inicializar_sistema()
        
        assert len(sistema_dia3['pecas_aprovadas']) == 10
        assert len(sistema_dia3['pecas_reprovadas']) == 2
        assert len(sistema_dia3['caixas_fechadas']) == 1
        assert len(sistema_dia3['caixas_fechadas'][0]['pecas']) == 10
        assert len(sistema_dia3['caixa_atual']['pecas']) == 0
    
    def test_remocao_persiste(self, temp_db: Path) -> None:
        """Testa que remoção de peças persiste."""
        # Primeira execução - adiciona peças
        sistema1 = inicializar_sistema()
        
        peca1 = criar_peca("P001", 100.0, "azul", 15.0, True)
        peca2 = criar_peca("P002", 101.0, "verde", 16.0, True)
        peca3 = criar_peca("P003", 120.0, "vermelho", 25.0, False, ["Reprovada"])
        
        adicionar_peca_em_caixa(peca1, sistema1)
        adicionar_peca_em_caixa(peca2, sistema1)
        sistema1['pecas_reprovadas'].append(peca3)
        database.sincronizar_sistema(sistema1)
        
        # Segunda execução - remove peça
        sistema2 = inicializar_sistema()
        
        assert len(sistema2['pecas_aprovadas']) == 2
        assert len(sistema2['pecas_reprovadas']) == 1
        
        sucesso, msg = remover_peca_por_id("P001", sistema2)
        assert sucesso is True
        
        # Terceira execução - verifica remoção
        sistema3 = inicializar_sistema()
        
        assert len(sistema3['pecas_aprovadas']) == 1
        assert sistema3['pecas_aprovadas'][0]['id'] == "P002"
        assert len(sistema3['pecas_reprovadas']) == 1
    
    def test_multiplas_caixas_fechadas(self, temp_db: Path) -> None:
        """Testa múltiplas caixas fechadas com persistência."""
        # Primeira execução - fecha 2 caixas
        sistema1 = inicializar_sistema()
        
        # Adiciona 25 peças (fecha 2 caixas, sobram 5 na terceira)
        for i in range(25):
            peca = criar_peca(f"P{i:03d}", 100.0, "azul", 15.0, True)
            adicionar_peca_em_caixa(peca, sistema1)
        
        assert len(sistema1['caixas_fechadas']) == 2
        assert len(sistema1['caixa_atual']['pecas']) == 5
        assert sistema1['contador_caixas'] == 3
        
        # Segunda execução - verifica estado
        sistema2 = inicializar_sistema()
        
        assert len(sistema2['caixas_fechadas']) == 2
        assert sistema2['caixas_fechadas'][0]['id'] == 1
        assert sistema2['caixas_fechadas'][1]['id'] == 2
        assert len(sistema2['caixas_fechadas'][0]['pecas']) == 10
        assert len(sistema2['caixas_fechadas'][1]['pecas']) == 10
        assert len(sistema2['caixa_atual']['pecas']) == 5
        assert sistema2['caixa_atual']['id'] == 3
        
        # Completa terceira caixa
        for i in range(25, 30):
            peca = criar_peca(f"P{i:03d}", 100.0, "verde", 15.0, True)
            adicionar_peca_em_caixa(peca, sistema2)
        
        assert len(sistema2['caixas_fechadas']) == 3
        
        # Terceira execução - verifica 3 caixas fechadas
        sistema3 = inicializar_sistema()
        
        assert len(sistema3['caixas_fechadas']) == 3
        assert sistema3['contador_caixas'] == 4


class TestConcorrencia:
    """Testa cenários de concorrência (simulados)."""
    
    def test_leitura_apos_escrita(self, temp_db: Path) -> None:
        """Testa que leitura após escrita retorna dados corretos."""
        sistema1 = inicializar_sistema()
        
        peca = criar_peca("P001", 100.0, "azul", 15.0, True)
        adicionar_peca_em_caixa(peca, sistema1)
        
        # Força sincronização
        database.sincronizar_sistema(sistema1)
        
        # Carrega imediatamente
        sistema2 = database.carregar_sistema_completo()
        
        assert len(sistema2['pecas_aprovadas']) == 1
        assert sistema2['pecas_aprovadas'][0]['id'] == "P001"


class TestRecuperacaoErros:
    """Testa recuperação de erros e estados inconsistentes."""
    
    def test_banco_corrompido_cria_novo(self, temp_db: Path) -> None:
        """Se banco estiver corrompido, deve criar novo."""
        # Cria banco válido
        sistema1 = inicializar_sistema()
        peca = criar_peca("P001", 100.0, "azul", 15.0, True)
        adicionar_peca_em_caixa(peca, sistema1)
        
        # Simula corrupção (esvazia tabelas)
        database.limpar_banco()
        
        # Tenta carregar - deve retornar sistema vazio mas funcional
        sistema2 = inicializar_sistema()
        
        assert len(sistema2['pecas_aprovadas']) == 0
        assert sistema2['caixa_atual'] is not None
        assert sistema2['contador_caixas'] == 1
    
    def test_sistema_se_recupera_de_estado_vazio(self, temp_db: Path) -> None:
        """Sistema vazio deve funcionar normalmente."""
        database.inicializar_database()
        database.limpar_banco()
        
        sistema = inicializar_sistema()
        
        # Deve criar estado inicial
        assert sistema['caixa_atual'] is not None
        assert sistema['contador_caixas'] == 1
        
        # Deve conseguir adicionar peças
        peca = criar_peca("P001", 100.0, "azul", 15.0, True)
        caixa_fechada, msg = adicionar_peca_em_caixa(peca, sistema)
        
        assert caixa_fechada is False
        assert len(sistema['pecas_aprovadas']) == 1


class TestMotivosReprovacao:
    """Testa persistência de motivos de reprovação."""
    
    def test_motivos_multiplos_persistem(self, temp_db: Path) -> None:
        """Múltiplos motivos de reprovação devem persistir."""
        sistema1 = inicializar_sistema()
        
        peca = criar_peca(
            "P001", 120.0, "vermelho", 25.0, False,
            [
                "Peso fora do intervalo (95.0-105.0g): 120.0g",
                "Cor inadequada (esperado: azul ou verde): vermelho",
                "Comprimento fora do intervalo (10.0-20.0cm): 25.0cm"
            ]
        )
        sistema1['pecas_reprovadas'].append(peca)
        database.sincronizar_sistema(sistema1)
        
        # Segunda execução
        sistema2 = inicializar_sistema()
        
        assert len(sistema2['pecas_reprovadas']) == 1
        assert len(sistema2['pecas_reprovadas'][0]['motivos_reprovacao']) == 3
        
        motivos = sistema2['pecas_reprovadas'][0]['motivos_reprovacao']
        assert any("Peso" in m for m in motivos)
        assert any("Cor" in m for m in motivos)
        assert any("Comprimento" in m for m in motivos)
    
    def test_motivo_vazio_persiste(self, temp_db: Path) -> None:
        """Peça aprovada sem motivos deve persistir corretamente."""
        sistema1 = inicializar_sistema()
        
        peca = criar_peca("P001", 100.0, "azul", 15.0, True, [])
        adicionar_peca_em_caixa(peca, sistema1)
        
        # Segunda execução
        sistema2 = inicializar_sistema()
        
        assert len(sistema2['pecas_aprovadas']) == 1
        assert len(sistema2['pecas_aprovadas'][0]['motivos_reprovacao']) == 0

