with open('README.md', 'w', encoding='utf-8') as f:
    f.write("""# 🎓 Sistema de Gestão Escolar (CLI)

Um sistema de gestão escolar via Linha de Comandos (CLI) desenvolvido em Python e SQLite. O projeto permite gerir alunos, professores, turmas, lançar notas e gerar relatórios académicos de forma rápida e eficiente.

## ✨ Funcionalidades

O sistema está dividido em quatro módulos principais:

### 1. 👤 Gestão de Alunos
* **Adicionar Aluno:** Registo de alunos definindo Nome, Ano (1º, 2º ou 3º) e Turma (A ou B).
* **Limite por Turma:** Validação automática que impede o registo de mais de 30 alunos por turma.
* **Remover Aluno:** Exclusão de registos através do ID único do aluno.
* **Listagem:** Visualização rápida de todos os alunos de uma turma específica.

### 2. 👨‍🏫 Gestão de Professores
* **Adicionar/Remover Professor:** Registo e exclusão de docentes no sistema.
* **Vincular a Turmas:** Associação de professores a turmas específicas (relação N:M), permitindo que um professor lecione a várias turmas simultaneamente.
* **Listagem:** Visualização dos professores alocados a uma determinada turma.

### 3. 📝 Lançamento de Notas
* Lançamento das notas **P1** e **P2** (valores de 0.0 a 10.0).
* **Cálculo Automático de Situação:** O sistema calcula a média do aluno assim que as duas notas são lançadas. Se a média for $\ge 5.0$, a situação é atualizada para "Aprovado"; caso contrário, "Reprovado". Se faltar alguma nota, permanece como "Cursando".

### 4. 📊 Relatórios
* **Notas e Situação:** Exibe o boletim completo da turma, incluindo os professores responsáveis associados a essa turma, e um resumo das aprovações/reprovações.
* **Média Geral:** Calcula e exibe a média geral da turma (considerando apenas alunos com ambas as notas lançadas).
* **Pendências:** Lista rapidamente os alunos que ainda estão sem notas lançadas no sistema.

## 🛠️ Tecnologias e Arquitetura

* **Linguagem:** Python 3.x
* **Base de Dados:** SQLite3
* **Paradigma:** Orientado a Base de Dados (Database-driven Programming) integrado com o Padrão Repository, separando a lógica de acesso a dados da interface do utilizador.

### Otimizações e Integridade (ACID)
A ligação ao SQLite foi projetada para garantir total fiabilidade:
* **Transações Seguras:** Utilização do modo `WAL` (Write-Ahead Logging).
* **Integridade Referencial:** Chaves estrangeiras (Foreign Keys) ativadas. Se um professor for removido, a regra `ON DELETE CASCADE` garante que os seus vínculos com as turmas também sejam eliminados automaticamente.
* **Índices de Performance:** Criação de índices customizados (ex: `idx_alunos_serie_turma`) para otimizar as pesquisas frequentes.

## 📁 Estrutura de Ficheiros

```text
├── main.py                  # Ponto de entrada, menus CLI e fluxos do utilizador
├── database/
│   ├── conexao.py           # Gestor de ligação SQLite e criação da base de dados
│   └── schema.sql           # Estrutura DDL (alunos, professores, professor_turma)
├── repository/
│   ├── aluno_repo.py        # Consultas e manipulações CRUD de alunos
│   └── professor_repo.py    # Consultas e manipulações CRUD de professores e vínculos
└── escola.db                # Ficheiro da base de dados local (Gerado automaticamente)
