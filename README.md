# 🎓 Sistema de Gestão Escolar (CLI)

Um sistema de gerenciamento escolar via Linha de Comando (CLI) desenvolvido em Python e SQLite. O projeto permite gerenciar alunos, lançar notas e gerar relatórios acadêmicos de forma rápida e eficiente.

## ✨ Funcionalidades

O sistema está dividido em três módulos principais:

### 1. 👤 Gerenciamento de Alunos
* **Adicionar Aluno:** Cadastro de alunos definindo Nome, Série (1º, 2º ou 3º ano) e Turma (A ou B).
* **Limite por Turma:** Validação automática que impede o cadastro de mais de 30 alunos por turma.
* **Remover Aluno:** Exclusão de registros através do ID único do aluno.
* **Listagem:** Visualização rápida de todos os alunos de uma turma específica.

### 2. 📝 Lançamento de Notas
* Lançamento das notas **P1** e **P2** (valores de 0.0 a 10.0).
* **Cálculo Automático de Situação:** O sistema calcula a média do aluno assim que as duas notas são lançadas. Se a média for $\ge 5.0$, a situação é atualizada para "Aprovado"; caso contrário, "Reprovado". Se faltar alguma nota, permanece como "Cursando".

### 3. 📊 Relatórios
* **Notas e Situação:** Exibe o boletim completo da turma e um resumo das aprovações/reprovações.
* **Média Geral:** Calcula e exibe a média geral da turma (considerando apenas alunos com ambas as notas lançadas).
* **Pendências:** Lista rapidamente os alunos que ainda estão sem notas lançadas no sistema.

## 🛠️ Tecnologias e Arquitetura

* **Linguagem:** Python 3.x
* **Banco de Dados:** SQLite3
* **Padrão de Projeto:** Repository Pattern (`aluno_repo.py`), separando a lógica de acesso a dados da interface do usuário.

### Otimizações de Banco de Dados
A conexão com o SQLite foi otimizada para melhor performance e concorrência:
* Utilização do modo `WAL` (Write-Ahead Logging).
* Chaves estrangeiras (Foreign Keys) ativadas.
* Conexão Thread-safe utilizando `threading.local()`.
* Índices customizados para otimizar as buscas por série e turma (a operação mais frequente).

## 📁 Estrutura de Arquivos

```text
├── main.py                  # Ponto de entrada, menus CLI e fluxos do usuário
├── database/
│   ├── conexao.py           # Gerenciador de conexão SQLite e criação do banco
│   └── schema.sql           # Estrutura das tabelas (DDL) e restrições
├── repository/
│   └── aluno_repo.py        # Consultas e manipulações no banco (CRUD)
└── escola.db                # Arquivo do banco de dados (Gerado automaticamente)
