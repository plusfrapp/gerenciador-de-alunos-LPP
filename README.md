## Sistema de Gestão Escolar (CLI)

**Integrantes:**
* Felipe Gonçalves Vidal
* Rafael José de Souza Marques
* Robert Francisco Taveira
* Paulo de Tarso Rezende Lôbo

---

## Fundamentação Teórica & Decisões de Projeto

Este projeto foi estruturado seguindo rigorosamente os seguintes pilares acadêmicos e técnicos:

* **Paradigma Orientado a Banco de Dados (Database-driven Programming):** A lógica principal do sistema é ditada pela estrutura das informações e operações de persistência (CRUD) via SQL, e não por fluxos lógicos rígidos no código. As regras de negócio (como limites de notas e restrições) são controladas diretamente no banco.
* **Tecnologias (Python + SQLite):** O **Python** atua na orquestração e interface, enquanto o **SQLite** gerencia os dados de forma nativa e sem a necessidade de servidores externos complexos, garantindo máxima portabilidade para esta microaplicação.
* **Conformidade ACID e Integridade:** A escolha do SQLite garante transações robustas baseadas nas propriedades **ACID** (Atomicidade, Consistência, Isolamento e Durabilidade). Isso assegura a integridade referencial do sistema acadêmico, impedindo, por exemplo, inconsistências nos vínculos entre alunos, professores e turmas.

---

## Sobre o Sistema (Gestão Escolar)

Um sistema de gestão escolar via Linha de Comandos (CLI) desenvolvido em Python e SQLite. O projeto permite gerir alunos, professores, turmas, lançar notas e gerar relatórios acadêmicos de forma rápida e eficiente.

### Funcionalidades (Módulos Principais)

**1. Gestão de Alunos**
* **Adicionar Aluno:** Registo de alunos definindo Nome, Ano (1º, 2º ou 3º) e Turma (A ou B).
* **Limite por Turma:** Validação automática que impede o registo de mais de 30 alunos por turma.
* **Remover Aluno:** Exclusão de registos através do ID único do aluno.
* **Listagem:** Visualização rápida de todos os alunos de uma turma específica.

**2. Gestão de Professores**
* **Adicionar/Remover Professor:** Registo e exclusão de docentes no sistema.
* **Vincular a Turmas:** Associação de professores a turmas específicas (relação N:M), permitindo que um professor lecione a várias turmas simultaneamente.
* **Listagem:** Visualização dos professores alocados a uma determinada turma.

**3. Lançamento de Notas**
* Lançamento das notas **P1** e **P2** (valores de 0.0 a 10.0).
* **Cálculo Automático de Situação:** O sistema calcula a média do aluno assim que as duas notas são lançadas. Se a média for >= 5.0, a situação é atualizada para "Aprovado"; caso contrário, "Reprovado". Se faltar alguma nota, permanece como "Cursando".

**4. Relatórios**
* **Notas e Situação:** Exibe o boletim completo da turma, incluindo os professores responsáveis associados a essa turma, e um resumo das aprovações/reprovações.
* **Média Geral:** Calcula e exibe a média geral da turma (considerando apenas alunos com ambas as notas lançadas).
* **Pendências:** Lista rapidamente os alunos que ainda estão sem notas lançadas no sistema.

---

## Arquitetura e Estrutura de Arquivos

* **Paradigma:** Orientado a Base de Dados integrado com o Padrão Repository, separando a lógica de acesso a dados da interface do utilizador.
* **Otimizações:** Transações seguras via `WAL` (Write-Ahead Logging), Chaves Estrangeiras ativadas (`ON DELETE CASCADE`) e Índices de Performance customizados.

```text
├── main.py                  # Ponto de entrada, menus CLI e fluxos do utilizador
├── database/
│   ├── conexao.py           # Gestor de ligação SQLite e criação da base de dados
│   └── schema.sql           # Estrutura DDL (alunos, professores, professor_turma)
├── repository/
│   ├── aluno_repo.py        # Consultas e manipulações CRUD de alunos
│   └── professor_repo.py    # Consultas e manipulações CRUD de professores e vínculos
└── escola.db                # Ficheiro da base de dados local (Gerado automaticamente)

```

## Como Executar o Projeto

Pré-requisitos: Certifique-se de ter o Python 3 instalado no seu computador. O projeto utiliza apenas bibliotecas nativas, dispensando instalações externas.

1. **Clonar o repositório:**

```bash
git clone https://github.com/plusfrapp/gerenciador-de-alunos

```

2. **Entrar na pasta:**

```bash
cd gerenciador-de-alunos-LPP

```

3. **Executar:**

```bash
python3 main.py

```
