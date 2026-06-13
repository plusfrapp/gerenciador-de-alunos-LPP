import time
from database.conexao import inicializar_banco, fechar_conexao
from repository import aluno_repo

# ── CONSTANTES ──────────────────────────────────────────────────────────────

SERIES = [1, 2, 3]
TURMAS = ['A', 'B']

# ── UTILITÁRIOS DE INPUT ─────────────────────────────────────────────────────

def pedir_texto(mensagem: str) -> str:
    while True:
        v = input(mensagem).strip()
        if v:
            return v
        print("  ❌ Campo obrigatório, não pode ser vazio.")

def pedir_int(mensagem: str, opcoes: list[int]) -> int:
    while True:
        try:
            v = int(input(mensagem))
            if v in opcoes:
                return v
            print(f"  ❌ Digite uma das opções: {opcoes}")
        except ValueError:
            print("  ❌ Digite um número inteiro válido.")

def pedir_id(mensagem: str) -> int:
    while True:
        try:
            v = int(input(mensagem))
            if v > 0:
                return v
            print("  ❌ ID deve ser maior que zero.")
        except ValueError:
            print("  ❌ Digite um número inteiro válido.")

def pedir_nota(mensagem: str) -> float:
    while True:
        try:
            v = float(input(mensagem))
            if 0.0 <= v <= 10.0:
                return v
            print("  ❌ Nota deve estar entre 0.0 e 10.0.")
        except ValueError:
            print("  ❌ Digite um número válido.")

def pedir_turma(mensagem: str) -> str:
    while True:
        v = input(mensagem).strip().upper()
        if v in TURMAS:
            return v
        print(f"  ❌ Turma inválida. Digite A ou B.")

def separador(char='─', largura=50):
    print(f"  {char * largura}")

# ── SELEÇÃO DE SÉRIE/TURMA ───────────────────────────────────────────────────

def selecionar_serie_turma() -> tuple[int, str]:
    serie = pedir_int("  Série (1, 2 ou 3): ", SERIES)
    turma = pedir_turma("  Turma (A ou B): ")
    return serie, turma

# ── MENUS ────────────────────────────────────────────────────────────────────

def menu_principal() -> str:
    print("\n" + "=" * 52)
    print("         SISTEMA DE GESTÃO ESCOLAR")
    print("=" * 52)
    print("  1. 👤  Gerenciar Alunos")
    print("  2. 📝  Lançar Notas")
    print("  3. 📊  Relatórios")
    print("  0. 💾  Sair")
    print("=" * 52)
    return input("  Opção: ").strip()

def submenu_alunos() -> str:
    print("\n" + "─" * 36)
    print("  [ GERENCIAR ALUNOS ]")
    print("─" * 36)
    print("  1. Adicionar Aluno")
    print("  2. Remover Aluno")
    print("  3. Listar Alunos de uma Turma")
    print("  0. ← Voltar")
    print("─" * 36)
    return input("  Opção: ").strip()

def submenu_relatorios() -> str:
    print("\n" + "─" * 36)
    print("  [ RELATÓRIOS ]")
    print("─" * 36)
    print("  1. Notas e Situação da Turma")
    print("  2. Média Geral da Turma")
    print("  3. Alunos Sem Notas Lançadas")
    print("  0. ← Voltar")
    print("─" * 36)
    return input("  Opção: ").strip()

# ── FLUXOS ───────────────────────────────────────────────────────────────────

def fluxo_alunos():
    while True:
        op = submenu_alunos()

        if op == '1':
            print("\n  ── Adicionar Aluno ──")
            nome  = pedir_texto("  Nome do Aluno: ")
            serie, turma = selecionar_serie_turma()
            ok, msg = aluno_repo.adicionar_aluno(nome, serie, turma)
            print(f"  {'✅' if ok else '❌'} {msg}")

        elif op == '2':
            print("\n  ── Remover Aluno ──")
            serie, turma = selecionar_serie_turma()
            alunos = aluno_repo.listar_por_turma(serie, turma)
            if not alunos:
                print(f"  ℹ️  Nenhum aluno em {serie}º {turma}.")
            else:
                _imprimir_lista_simples(alunos, serie, turma)
                aluno_id = pedir_id("  ID do aluno a remover: ")
                ok, msg = aluno_repo.remover_aluno(aluno_id)
                print(f"  {'✅' if ok else '❌'} {msg}")

        elif op == '3':
            print("\n  ── Listar Alunos ──")
            serie, turma = selecionar_serie_turma()
            alunos = aluno_repo.listar_por_turma(serie, turma)
            _imprimir_lista_simples(alunos, serie, turma)

        elif op == '0':
            break
        else:
            print("  ❌ Opção inválida.")

def fluxo_notas():
    print("\n  ── Lançar Notas ──")
    serie, turma = selecionar_serie_turma()
    alunos = aluno_repo.listar_por_turma(serie, turma)

    if not alunos:
        print(f"  ℹ️  Nenhum aluno em {serie}º {turma}.")
        return

    _imprimir_lista_simples(alunos, serie, turma)
    aluno_id = pedir_id("  ID do aluno: ")
    p1 = pedir_nota("  Nota P1 (0.0 a 10.0): ")
    p2 = pedir_nota("  Nota P2 (0.0 a 10.0): ")
    ok, msg = aluno_repo.lancar_notas(aluno_id, p1, p2)
    print(f"  {'✅' if ok else '❌'} {msg}")

def fluxo_relatorios():
    while True:
        op = submenu_relatorios()

        if op == '1':
            print("\n  ── Notas e Situação ──")
            serie, turma = selecionar_serie_turma()
            alunos = aluno_repo.listar_por_turma(serie, turma)
            contagem = aluno_repo.contar_por_situacao(serie, turma)
            _imprimir_relatorio_notas(alunos, serie, turma, contagem)

        elif op == '2':
            print("\n  ── Média Geral ──")
            serie, turma = selecionar_serie_turma()
            media = aluno_repo.media_geral_turma(serie, turma)
            total = len(aluno_repo.listar_por_turma(serie, turma))
            separador()
            print(f"  Turma: {serie}º ano {turma}  |  Total de alunos: {total}")
            if media is not None:
                print(f"  Média geral da turma: {media:.2f}")
            else:
                print("  ℹ️  Nenhuma nota lançada ainda.")
            separador()

        elif op == '3':
            print("\n  ── Alunos Sem Notas ──")
            serie, turma = selecionar_serie_turma()
            pendentes = aluno_repo.alunos_sem_nota(serie, turma)
            separador()
            print(f"  Turma {serie}º {turma} — alunos com notas pendentes:")
            separador()
            if pendentes:
                for a in pendentes:
                    print(f"  ID {a['id']:<6} {a['nome']}")
            else:
                print("  ✅ Todos os alunos têm notas lançadas.")
            separador()

        elif op == '0':
            break
        else:
            print("  ❌ Opção inválida.")

# ── EXIBIÇÃO ─────────────────────────────────────────────────────────────────

def _imprimir_lista_simples(alunos: list, serie: int, turma: str):
    separador()
    print(f"  Turma: {serie}º ano {turma}  |  Alunos: {len(alunos)}/30")
    separador()
    if alunos:
        print(f"  {'ID':<6} Nome")
        separador('·')
        for a in alunos:
            print(f"  {a['id']:<6} {a['nome']}")
    else:
        print("  ℹ️  Nenhum aluno cadastrado nesta turma.")
    separador()

def _imprimir_relatorio_notas(alunos: list, serie: int, turma: str, contagem: dict):
    separador('═')
    print(f"  RELATÓRIO — {serie}º ano | Turma {turma}  |  {len(alunos)}/30 alunos")
    separador('═')
    if alunos:
        print(f"  {'ID':<5} {'Nome':<28} {'P1':>5} {'P2':>5} {'Média':>6}  Situação")
        separador('·')
        for a in alunos:
            p1_s  = f"{a['p1']:.1f}"  if a['p1']  is not None else "  —"
            p2_s  = f"{a['p2']:.1f}"  if a['p2']  is not None else "  —"
            if a['p1'] is not None and a['p2'] is not None:
                med_s = f"{(a['p1']+a['p2'])/2:.1f}"
            else:
                med_s = "  —"
            print(f"  {a['id']:<5} {a['nome']:<28} {p1_s:>5} {p2_s:>5} {med_s:>6}  {a['situacao']}")
        separador('·')
        print(f"  ✅ Aprovados: {contagem['Aprovado']}  "
              f"❌ Reprovados: {contagem['Reprovado']}  "
              f"📖 Cursando: {contagem['Cursando']}")
    else:
        print("  ℹ️  Nenhum aluno cadastrado nesta turma.")
    separador('═')

# ── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    inicializar_banco()

    try:
        while True:
            op = menu_principal()

            if op == '1':
                fluxo_alunos()
            elif op == '2':
                fluxo_notas()
            elif op == '3':
                fluxo_relatorios()
            elif op == '0':
                print("\n  💾 Salvando dados...")
                time.sleep(0.4)
                print("  👋 Sistema encerrado. Até logo!")
                break
            else:
                print("  ❌ Opção inválida.")
    finally:
        fechar_conexao()

if __name__ == "__main__":
    main()