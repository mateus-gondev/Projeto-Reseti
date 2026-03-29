# 🚀 Reseti - Sistema de Gerenciamento e Reservas

O **Reseti** é um ecossistema que esta sendo desenvolvido para otimizar o controle de ativos e suporte técnico. O foco do projeto é centralizar a gestão de usuários, facilitar a reserva de equipamentos e organizar a abertura e acompanhamento de Ordens de Serviço (OS).

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)

---

## 📋 Sobre o Projeto

O sistema esta sendo construído pensando em escalabilidade e segurança, utilizando uma arquitetura baseada em **Blueprints** no Flask. Os três pilares principais são:

1.  **Usuários:** Controle de permissões (Adm/Comum), autenticação segura com Hash de senha e recuperação via e-mail.
2.  **Reservas:** Gerenciamento de empréstimos de equipamentos com controle de datas e status.
3.  **Ordens de Serviço (OS):** Fluxo de suporte técnico para manutenção e organização de demandas.

---

## 📖 Documentação Adicional

Para facilitar a colaboração, dividimos a documentação técnica em dois guias específicos:

* **[⚙️ Guia de Configuração e Ambiente](https://github.com/mateus-gondev/Projeto-Reseti/blob/main/backend/Configuracao_Ambiente.md):** Aprenda a configurar o `.venv`, instalar dependências, configurar o banco de dados PostgreSQL e as variáveis do `.env`.
* **[🔌 Guia de Rotas e Testes (API)](https://github.com/mateus-gondev/Projeto-Reseti/blob/main/backend/Guia_de_Teste.md):** Detalhamento de todos os endpoints disponíveis, tipos de requisição (JSON) e como realizar os testes utilizando o **Postman**.

---

## 🛠 Tecnologias Utilizadas

* **Linguagem:** Python 3.x
* **Framework:** Flask
* **Banco de Dados:** PostgreSQL (SQLAlchemy ORM)
* **Migrações:** Flask-Migrate (Alembic)
* **Segurança:** Werkzeug Security & ItsDangerous (Tokens)
* **E-mail:** Flask-Mail

---

Obs* Projeto ainda em **Desenvolvimento**

