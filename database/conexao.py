import sqlite3
import os
import threading

_PASTA_DATABASE = os.path.dirname(os.path.abspath(__file__))
_RAIZ_PROJETO   = os.path.dirname(_PASTA_DATABASE)

SCHEMA_PATH = os.path.join(_PASTA_DATABASE, 'schema.sql')
DB_PATH     = os.path.join(_RAIZ_PROJETO, 'escola.db')

_local = threading.local()

def conectar() -> sqlite3.Connection:
    if not getattr(_local, 'conn', None):
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.execute("PRAGMA journal_mode = WAL;")
        conn.execute("PRAGMA synchronous = NORMAL;")
        conn.execute("PRAGMA cache_size = -8000;")
        conn.execute("PRAGMA temp_store = MEMORY;")
        _local.conn = conn
    return _local.conn

def fechar_conexao():
    conn = getattr(_local, 'conn', None)
    if conn:
        conn.close()
        _local.conn = None

def inicializar_banco():
    conn = conectar()

    with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.commit()

    total = conn.execute("SELECT COUNT(*) FROM alunos").fetchone()[0]
    if total == 0:
        print("  📦 Banco vazio. Carregando dados iniciais...")
        _popular_banco(conn)
        total = conn.execute("SELECT COUNT(*) FROM alunos").fetchone()[0]
        print(f"  ✅ {total} alunos carregados com sucesso!")
    else:
        print(f"  ✅ Banco carregado — {total} aluno(s) cadastrado(s).")

def _popular_banco(conn: sqlite3.Connection):
    PROFESSORES = [
        "Ana Paula Ferreira",
        "Carlos Eduardo Lima",
        "Mariana Costa Souza",
        "Roberto Alves Nunes",
        "Fernanda Oliveira",
        "Thiago Martins",
    ]

    VINCULOS = {
        0: [(1, 'A'), (1, 'B')],
        1: [(2, 'A')],
        2: [(2, 'B'), (3, 'A')],
        3: [(3, 'B')],
        4: [(1, 'A'), (2, 'A')],
        5: [(3, 'A'), (3, 'B')],
    }

    ALUNOS = [
        ("Alice Mendonça",        1, 'A',  8.5,  9.0),
        ("Bruno Carvalho",        1, 'A',  4.0,  5.5),
        ("Camila Rocha",          1, 'A',  7.0,  6.5),
        ("Daniel Fonseca",        1, 'A',  3.0,  4.0),
        ("Eduardo Pires",         1, 'A',  9.0, 10.0),
        ("Fernanda Lima",         1, 'A',  6.0,  6.0),
        ("Gabriel Santos",        1, 'A',  5.5,  5.0),
        ("Helena Cruz",           1, 'A',  8.0,  7.5),
        ("Igor Melo",             1, 'A',  2.0,  3.5),
        ("Juliana Teixeira",      1, 'A',  7.5,  8.0),
        ("Kevin Barbosa",         1, 'A',  6.5,  7.0),
        ("Larissa Dias",          1, 'A', None, None),
        ("Marcos Vieira",         1, 'A',  4.5,  4.0),
        ("Natália Gomes",         1, 'A',  9.5,  9.0),
        ("Otávio Ramos",          1, 'A', None, None),
        ("Paula Freitas",         1, 'B',  7.0,  8.5),
        ("Rafael Corrêa",         1, 'B',  5.0,  5.0),
        ("Sabrina Moura",         1, 'B',  6.5,  7.0),
        ("Tiago Lopes",           1, 'B',  3.5,  4.5),
        ("Úrsula Neves",          1, 'B',  8.0,  8.0),
        ("Víctor Araújo",         1, 'B',  9.0,  8.5),
        ("Wanessa Ribeiro",       1, 'B',  4.0,  5.0),
        ("Xandre Campos",         1, 'B',  7.5,  7.0),
        ("Yasmin Cunha",          1, 'B',  6.0,  6.5),
        ("Zélia Monteiro",        1, 'B', None, None),
        ("André Brito",           1, 'B',  5.5,  6.0),
        ("Beatriz Dantas",        1, 'B',  8.5,  9.0),
        ("Cesar Nogueira",        1, 'B',  2.5,  3.0),
        ("Daniela Sousa",         1, 'B',  7.0,  6.5),
        ("Elias Pereira",         1, 'B', None, None),
        ("Felipe Tavares",        2, 'A',  8.0,  7.5),
        ("Giovana Macedo",        2, 'A',  5.0,  4.5),
        ("Henrique Cardoso",      2, 'A',  9.5,  9.0),
        ("Isabela Fernandes",     2, 'A',  6.5,  7.0),
        ("João Pedro Silva",      2, 'A',  3.0,  2.5),
        ("Karina Batista",        2, 'A',  7.5,  8.0),
        ("Leonardo Pinto",        2, 'A',  6.0,  5.5),
        ("Mayara Cavalcanti",     2, 'A',  8.5,  9.5),
        ("Nicolas Rezende",       2, 'A',  4.0,  5.0),
        ("Olívia Guimarães",      2, 'A',  7.0,  7.5),
        ("Pedro Henrique Assis",  2, 'A', None, None),
        ("Queila Torres",         2, 'A',  6.5,  6.0),
        ("Rodrigo Vasquez",       2, 'A',  5.5,  6.5),
        ("Sara Nascimento",       2, 'A',  9.0,  8.5),
        ("Túlio Brandão",         2, 'A', None, None),
        ("Ubirajara Filho",       2, 'B',  6.0,  6.5),
        ("Valentina Esteves",     2, 'B',  8.0,  8.5),
        ("Wellington Coelho",     2, 'B',  4.5,  4.0),
        ("Ximena Falcão",         2, 'B',  7.5,  7.0),
        ("Yara Vasconcelos",      2, 'B',  9.0,  9.5),
        ("Zilda Marques",         2, 'B',  3.5,  4.0),
        ("Alberto Romero",        2, 'B',  5.0,  5.5),
        ("Bianca Cerqueira",      2, 'B',  7.0,  8.0),
        ("Cláudio Siqueira",      2, 'B',  6.5,  6.0),
        ("Débora Andrade",        2, 'B', None, None),
        ("Emerson Figueiredo",    2, 'B',  8.5,  7.5),
        ("Flávia Queiroz",        2, 'B',  5.5,  6.0),
        ("Gustavo Leite",         2, 'B',  4.0,  3.5),
        ("Hanna Borges",          2, 'B',  9.0,  9.0),
        ("Ivan Medeiros",         2, 'B', None, None),
        ("Joana Silveira",        3, 'A',  7.5,  8.0),
        ("Kleber Azevedo",        3, 'A',  6.0,  5.5),
        ("Letícia Maia",          3, 'A',  9.0,  9.5),
        ("Murilo Pacheco",        3, 'A',  4.5,  5.0),
        ("Nayara Bonfim",         3, 'A',  8.0,  8.5),
        ("Oscar Gadelha",         3, 'A',  3.0,  3.5),
        ("Priscila Moraes",       3, 'A',  7.0,  7.5),
        ("Quirino Amaral",        3, 'A',  5.5,  6.0),
        ("Renata Lucena",         3, 'A',  8.5,  8.0),
        ("Sérgio Machado",        3, 'A',  6.5,  7.0),
        ("Tatiane Fontes",        3, 'A', None, None),
        ("Ulisses Coutinho",      3, 'A',  9.5, 10.0),
        ("Vera Sampaio",          3, 'A',  4.0,  4.5),
        ("Wagner Duarte",         3, 'A',  7.0,  6.5),
        ("Ângela Bastos",         3, 'A', None, None),
        ("Antônio Magalhães",     3, 'B',  6.5,  7.0),
        ("Bruna Paiva",           3, 'B',  8.0,  8.5),
        ("Cícero Holanda",        3, 'B',  5.0,  5.5),
        ("Daiane Roque",          3, 'B',  9.0,  9.5),
        ("Edmilson Correia",      3, 'B',  4.0,  3.5),
        ("Fabíola Drummond",      3, 'B',  7.5,  8.0),
        ("Genilson Abreu",        3, 'B',  6.0,  5.0),
        ("Hilária Ventura",       3, 'B',  8.5,  9.0),
        ("Iracema Gentil",        3, 'B',  3.5,  4.0),
        ("Juvenal Saraiva",       3, 'B',  7.0,  6.5),
        ("Keila Rodrigues",       3, 'B', None, None),
        ("Lúcio Espinosa",        3, 'B',  5.5,  6.5),
        ("Mirela Studart",        3, 'B',  9.0,  8.5),
        ("Nuno Cavalcante",       3, 'B',  4.5,  5.0),
        ("Ofélia Jucá",           3, 'B', None, None),
    ]

    def _situacao(p1, p2):
        if p1 is None or p2 is None:
            return 'Cursando'
        return 'Aprovado' if (p1 + p2) / 2 >= 5.0 else 'Reprovado'

    prof_ids = []
    for nome in PROFESSORES:
        cur = conn.execute("INSERT INTO professores (nome) VALUES (?)", (nome,))
        prof_ids.append(cur.lastrowid)

    for idx, turmas in VINCULOS.items():
        for serie, turma in turmas:
            conn.execute(
                "INSERT OR IGNORE INTO professor_turma VALUES (?, ?, ?)",
                (prof_ids[idx], serie, turma)
            )

    registros = [
        (nome, serie, turma, p1, p2, _situacao(p1, p2))
        for nome, serie, turma, p1, p2 in ALUNOS
    ]
    conn.executemany(
        "INSERT INTO alunos (nome, serie, turma, p1, p2, situacao) VALUES (?,?,?,?,?,?)",
        registros
    )
    conn.commit()