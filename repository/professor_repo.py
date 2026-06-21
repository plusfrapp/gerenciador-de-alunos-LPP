import sqlite3
import logging
from database.conexao import conectar

logger = logging.getLogger(__name__)

def adicionar_professor(nome: str) -> tuple[bool, str]:
    conn = conectar()
    try:
        cursor = conn.execute(
            "INSERT INTO professores (nome) VALUES (?)",
            (nome.strip(),)
        )
        conn.commit()
        return True, f"Professor '{nome.strip()}' cadastrado! ID: {cursor.lastrowid}"
    except sqlite3.Error as e:
        conn.rollback()
        return False, f"Erro ao cadastrar professor: {e}"

def remover_professor(professor_id: int) -> tuple[bool, str]:
    conn = conectar()
    try:
        prof = conn.execute(
            "SELECT nome FROM professores WHERE id = ?", (professor_id,)
        ).fetchone()
        if not prof:
            return False, f"Professor com ID #{professor_id} não encontrado."
        conn.execute("DELETE FROM professores WHERE id = ?", (professor_id,))
        conn.commit()
        return True, f"Professor '{prof['nome']}' removido com sucesso."
    except sqlite3.Error as e:
        conn.rollback()
        return False, f"Erro ao remover professor: {e}"

def vincular_turma(professor_id: int, serie: int, turma: str) -> tuple[bool, str]:
    conn = conectar()
    try:
        prof = conn.execute(
            "SELECT nome FROM professores WHERE id = ?", (professor_id,)
        ).fetchone()
        if not prof:
            return False, f"Professor com ID #{professor_id} não encontrado."
        
        # Verificar se o vínculo já existe
        ja_vinculado = conn.execute(
            "SELECT 1 FROM professor_turma WHERE professor_id = ? AND serie = ? AND turma = ?",
            (professor_id, serie, turma.upper())
        ).fetchone()
        
        if ja_vinculado:
            return False, f"O professor '{prof['nome']}' já está vinculado a essa turma."

        conn.execute(
            "INSERT INTO professor_turma (professor_id, serie, turma) VALUES (?, ?, ?)",
            (professor_id, serie, turma.upper())
        )
        conn.commit()
        return True, f"Professor '{prof['nome']}' vinculado à turma {serie}º {turma} com sucesso!"
    except sqlite3.Error as e:
        conn.rollback()
        return False, f"Erro ao vincular professor: {e}"

def listar_todos() -> list:
    conn = conectar()
    return conn.execute("SELECT id, nome FROM professores ORDER BY nome").fetchall()

def listar_por_turma(serie: int, turma: str) -> list:
    conn = conectar()
    return conn.execute(
        """SELECT p.id, p.nome FROM professores p
           JOIN professor_turma pt ON p.id = pt.professor_id
           WHERE pt.serie = ? AND pt.turma = ?
           ORDER BY p.nome""",
        (serie, turma.upper())
    ).fetchall()

def listar_turmas_do_professor(professor_id: int) -> list:
    conn = conectar()
    return conn.execute(
        "SELECT serie, turma FROM professor_turma WHERE professor_id = ? ORDER BY serie, turma",
        (professor_id,)
    ).fetchall()