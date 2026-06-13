import sqlite3
from database.conexao import conectar

MAX_ALUNOS_POR_TURMA = 30

# ── HELPERS ─────────────────────────────────────────────────────────────────

def _calcular_situacao(p1, p2) -> str:
    """Calcula situação com base nas duas notas. Só finaliza se ambas existirem."""
    if p1 is None or p2 is None:
        return 'Cursando'
    return 'Aprovado' if (p1 + p2) / 2 >= 5.0 else 'Reprovado'

def _contar_alunos(serie: int, turma: str) -> int:
    conn = conectar()
    row = conn.execute(
        "SELECT COUNT(*) FROM alunos WHERE serie = ? AND turma = ?",
        (serie, turma)
    ).fetchone()
    return row[0]

# ── CRUD ────────────────────────────────────────────────────────────────────

def adicionar_aluno(nome: str, serie: int, turma: str) -> tuple[bool, str]:
    """Adiciona aluno na turma, respeitando o limite de 30."""
    if _contar_alunos(serie, turma) >= MAX_ALUNOS_POR_TURMA:
        return False, f"Turma {serie}º {turma} está cheia (máx. {MAX_ALUNOS_POR_TURMA} alunos)."
    conn = conectar()
    try:
        cursor = conn.execute(
            "INSERT INTO alunos (nome, serie, turma) VALUES (?, ?, ?)",
            (nome.strip(), serie, turma.upper())
        )
        conn.commit()
        return True, f"Aluno '{nome.strip()}' cadastrado! ID: {cursor.lastrowid}"
    except sqlite3.Error as e:
        conn.rollback()
        return False, f"Erro ao cadastrar aluno: {e}"

def remover_aluno(aluno_id: int) -> tuple[bool, str]:
    """Remove aluno pelo ID."""
    conn = conectar()
    try:
        aluno = conn.execute(
            "SELECT nome FROM alunos WHERE id = ?", (aluno_id,)
        ).fetchone()
        if not aluno:
            return False, f"Aluno com ID #{aluno_id} não encontrado."
        conn.execute("DELETE FROM alunos WHERE id = ?", (aluno_id,))
        conn.commit()
        return True, f"Aluno '{aluno['nome']}' removido com sucesso."
    except sqlite3.Error as e:
        conn.rollback()
        return False, f"Erro ao remover aluno: {e}"

def lancar_notas(aluno_id: int, p1: float, p2: float) -> tuple[bool, str]:
    """Lança P1 e P2 e recalcula a situação do aluno."""
    conn = conectar()
    try:
        aluno = conn.execute(
            "SELECT nome FROM alunos WHERE id = ?", (aluno_id,)
        ).fetchone()
        if not aluno:
            return False, f"Aluno com ID #{aluno_id} não encontrado."
        situacao = _calcular_situacao(p1, p2)
        media = (p1 + p2) / 2
        conn.execute(
            "UPDATE alunos SET p1 = ?, p2 = ?, situacao = ? WHERE id = ?",
            (p1, p2, situacao, aluno_id)
        )
        conn.commit()
        return True, f"Notas lançadas! Média: {media:.1f} → {situacao}"
    except sqlite3.Error as e:
        conn.rollback()
        return False, f"Erro ao lançar notas: {e}"

# ── CONSULTAS ───────────────────────────────────────────────────────────────

def listar_por_turma(serie: int, turma: str) -> list:
    """Lista todos os alunos de uma turma, ordenados por nome."""
    conn = conectar()
    return conn.execute(
        """SELECT id, nome, p1, p2, situacao FROM alunos
           WHERE serie = ? AND turma = ?
           ORDER BY nome""",
        (serie, turma.upper())
    ).fetchall()

def alunos_sem_nota(serie: int, turma: str) -> list:
    """Retorna alunos sem P1 ou P2 lançadas."""
    conn = conectar()
    return conn.execute(
        """SELECT id, nome FROM alunos
           WHERE serie = ? AND turma = ? AND (p1 IS NULL OR p2 IS NULL)
           ORDER BY nome""",
        (serie, turma.upper())
    ).fetchall()

def media_geral_turma(serie: int, turma: str) -> float | None:
    """Calcula a média geral da turma (apenas alunos com ambas as notas)."""
    conn = conectar()
    row = conn.execute(
        """SELECT AVG((p1 + p2) / 2.0) FROM alunos
           WHERE serie = ? AND turma = ? AND p1 IS NOT NULL AND p2 IS NOT NULL""",
        (serie, turma.upper())
    ).fetchone()
    return round(row[0], 2) if row[0] is not None else None

def contar_por_situacao(serie: int, turma: str) -> dict:
    """Retorna contagem de aprovados, reprovados e cursando."""
    conn = conectar()
    rows = conn.execute(
        """SELECT situacao, COUNT(*) FROM alunos
           WHERE serie = ? AND turma = ?
           GROUP BY situacao""",
        (serie, turma.upper())
    ).fetchall()
    resultado = {'Aprovado': 0, 'Reprovado': 0, 'Cursando': 0}
    for row in rows:
        resultado[row['situacao']] = row[1]
    return resultado