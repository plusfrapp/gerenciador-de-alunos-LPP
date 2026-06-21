import time
import logging
from database.conexao import inicializar_banco, fechar_conexao
from repository import aluno_repo, professor_repo

logger = logging.getLogger(__name__)

# Constantes do sistema

SERIES = [1, 2, 3]
TURMAS = ['A', 'B']

# Funções auxiliares para entrada de dados

def pedir_texto(mensagem: str) -> str:
    while True:
        v = input(mensagem).strip()
        if v:
            return v
        logger.error("  ❌ Campo obrigatório, não pode ser vazio.")

def pedir_int(mensagem: str, opcoes: list[int]) -> int:
    while True:
        try:
            v = int(input(mensagem))
            if v in opcoes:
                return v
            logger.error(f"  ❌ Digite uma das opções: {opcoes}")
        except ValueError:
            logger.error("  ❌ Digite um número inteiro válido.")

def pedir_id(mensagem: str) -> int:
    while True:
        try:
            v = int(input(mensagem))
            if v > 0:
                return v
            logger.error("  ❌ ID deve ser maior que zero.")
        except ValueError:
            logger.error("  ❌ Digite um número inteiro válido.")

def pedir_nota(mensagem: str) -> float:
    while True:
        try:
            v = float(input(mensagem))
            if 0.0 <= v <= 10.0:
                return v
            logger.error("  ❌ Nota deve estar entre 0.0 e 10.0.")
        except ValueError:
            logger.error("  ❌ Digite um número válido.")

def pedir_turma(mensagem: str) -> str:
    while True:
        v = input(mensagem).strip().upper()
        if v in TURMAS:
            return v
        logger.error(f"  ❌ Turma inválida. Digite A ou B.")

def separador(char='─', largura=50):
    print(f"  {char * largura}")

# Seleção de série e turma

def selecionar_serie_turma() -> tuple[int, str]:
    serie = pedir_int("  Série (1, 2 ou 3): ", SERIES)
    turma = pedir_turma("  Turma (A ou B): ")
    return serie, turma

# Menus do sistema

def menu_principal() -> str:
    print("\n" + "=" * 52)
    print("         SISTEMA DE GESTÃO ESCOLAR")
    print("=" * 52)
    print("  1. 👤  Gerenciar Alunos")
    print("  2. 👨‍🏫  Gerenciar Professores")
    print("  3. 📝  Lançar Notas")
    print("  4. 📊  Relatórios")
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

def submenu_professores() -> str:
    print("\n" + "─" * 36)
    print("  [ GERENCIAR PROFESSORES ]")
    print("─" * 36)
    print("  1. Adicionar Professor")
    print("  2. Remover Professor")
    print("  3. Vincular Professor a uma Turma")
    print("  4. Listar Professores por Turma")
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

# Lógica principal e fluxos das telas

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
            logger.error("  ❌ Opção inválida.")

def fluxo_professores():
    while True:
        op = submenu_professores()

        if op == '1':
            print("\n  ── Adicionar Professor ──")
            nome = pedir_texto("  Nome do Professor: ")
            ok, msg = professor_repo.adicionar_professor(nome)
            print(f"  {'✅' if ok else '❌'} {msg}")

        elif op == '2':
            print("\n  ── Remover Professor ──")
            profs = professor_repo.listar_todos()
            if not profs:
                print("  ℹ️  Nenhum professor cadastrado.")
            else:
                _imprimir_lista_professores_simples(profs)
                prof_id = pedir_id("  ID do professor a remover: ")
                ok, msg = professor_repo.remover_professor(prof_id)
                print(f"  {'✅' if ok else '❌'} {msg}")

        elif op == '3':
            print("\n  ── Vincular Professor a uma Turma ──")
            profs = professor_repo.listar_todos()
            if not profs:
                print("  ℹ️  Cadastre um professor primeiro.")
                continue
            _imprimir_lista_professores_simples(profs)
            prof_id = pedir_id("  ID do professor: ")
            serie, turma = selecionar_serie_turma()
            ok, msg = professor_repo.vincular_turma(prof_id, serie, turma)
            print(f"  {'✅' if ok else '❌'} {msg}")

        elif op == '4':
            print("\n  ── Listar Professores por Turma ──")
            serie, turma = selecionar_serie_turma()
            profs = professor_repo.listar_por_turma(serie, turma)
            separador()
            print(f"  Turma: {serie}º ano {turma}  |  Professores vinculados:")
            separador()
            if profs:
                for p in profs:
                    print(f"  ID {p['id']:<6} {p['nome']}")
            else:
                print("  ℹ️  Nenhum professor vinculado a esta turma.")
            separador()

        elif op == '0':
            break
        else:
            logger.error("  ❌ Opção inválida.")

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
            logger.error("  ❌ Opção inválida.")

# Funções de exibição e formatação

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

def _imprimir_lista_professores_simples(professores: list):
    separador()
    print(f"  Professores Cadastrados: {len(professores)}")
    separador()
    print(f"  {'ID':<6} {'Nome':<28} Turmas Lecionadas")
    separador('·')
    for p in professores:
        turmas = professor_repo.listar_turmas_do_professor(p['id'])
        t_str = ", ".join([f"{t['serie']}º{t['turma']}" for t in turmas]) if turmas else "Nenhuma"
        print(f"  {p['id']:<6} {p['nome']:<28} {t_str}")
    separador()

def _imprimir_relatorio_notas(alunos: list, serie: int, turma: str, contagem: dict):
    separador('═')
    profs = professor_repo.listar_por_turma(serie, turma)
    prof_nomes = ", ".join([p['nome'] for p in profs]) if profs else "Nenhum vinculado"
    print(f"  RELATÓRIO — {serie}º ano | Turma {turma}  |  {len(alunos)}/30 alunos")
    print(f"  👨‍🏫 Professor(es): {prof_nomes}")
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

# Ponto de entrada do programa

def main():
    inicializar_banco()

    try:
        while True:
            op = menu_principal()

            if op == '1':
                fluxo_alunos()
            elif op == '2':
                fluxo_professores()
            elif op == '3':
                fluxo_notas()
            elif op == '4':
                fluxo_relatorios()
            elif op == '0':
                print("\n  💾 Salvando dados...")
                time.sleep(0.4)
                print("  👋 Sistema encerrado. Até logo!")
                break
            else:
                logger.error("  ❌ Opção inválida.")
    finally:
        fechar_conexao()

if __name__ == "__main__":
    main()