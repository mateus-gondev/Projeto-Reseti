# 📄 Configuração do Ambiente

<br>

## 🚀 Projeto Reseti - Guia de Instalação
Este documento detalha como configurar o ambiente de desenvolvimento para o backend do sistema Reseti.

<br>

### 🛠 Como Rodar o Projeto em Outra Máquina
**Pré-requisitos**
- Python 3.10+
- PostgreSQL (PgAdmin)
- Git

---

<br>

### ⚙️ Passo a Passo

1. Clonar o Repositório:
```bash
git clone "Nome do Repositorio"
cd backend
```

2. Criar e Ativar Ambiente Virtual:
```bash
# Criar Ambiente Virtual 
python -m venv .venv

# Ativar No Windows:
.venv\Scripts\activate

# Ativar No Linux/Mac:
source .venv/bin/activate
```

3. Instalar Dependências:
```bash
pip install -r requirements.txt
```

4. Configurar Variáveis de Ambiente (.env)
Crie um arquivo chamado **.env** na raiz seguindo o modelo abaixo:
**IMPORTANTE:** Nunca envie este arquivo para o Git. Por isso ele fica dentro do .gitignore

```bash
DATABASE_URL=postgresql://USUARIO:SENHA@localhost:5432/reseti
SECRET_KEY=sua_chave_secreta_aqui
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=seu_email@gmail.com
MAIL_PASSWORD=sua_senha_de_app_gerada_no_google
MAIL_DEFAULT_SENDER=seu_email@gmail.com
```

O nome do banco que você deve criar é **reseti** As credencias iram mudar, então coloque a suas credencias.

Da mesma forma as configurações de E-mail. 

5. Migrações do Banco
Com esse comando vc criar as tabelas para o banco de dados.
```bash
flask db init 
flask db migrate -m "Criando tabelas iniciais"
flask db upgrade
```

6. Iniciar o Servidor:
```bash
python app.py
```

---

### 🔄 Fluxo de Trabalho (Git)
Para manter o código organizado e evitar conflitos, utilize estes comandos no dia a dia:

<br>

### Garante que você está na branch principal e atualizado
```bash
git pull origin main # Puxa todos as mudanças do repositorio atual para sua máquina

```

**Para Salvar e Publicar Mudanças:**
```bash
# Iniciar Git *Fazer apenas uma vez!
git init

# Adiciona todas as alterações
git add .

# Cria um ponto na história (commit)
git commit -m "Explicação curta do que foi feito"

# Envia para o GitHub pela primeira vez
git push origin "Aqui o nome da branch ex:. main"

```
---

### Opcionais + Importante ⚠️
```bash
# Ver as Branch disponiveis (Listar)
git branch

# Mudar de uma Branch para outra (Trocar)
git checkout <nome-da-branch> 

# Apenas criar (Criar)
git branch <nome-da-branch> 

# Ou 

#Criar e já mudar para ela (Criar e Trocar)
git checkout -b <nome-da-branch>

```