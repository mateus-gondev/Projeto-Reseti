## 🔌 Documentação da API - Autenticação
Todas as rotas retornam JSON e esperam o cabeçalho.

---

### 📌 Endpoints
| Método | Rota | Descrição |
|----------|----------|----------|
| POST  | /auth/cadastro  | Cria um novo usuário (Adm ou Comum).  |
| POST  | /auth/login  | Autentica o usuário e retorna dados básicos. |
| POST  | /auth/reset-senha | Envia e-mail com token de recuperação.  |
| POST  | /reset-senha/<token>  | Define uma nova senha usando o token. |

--- 
<br>

### 🧪 Como testar no Postman

1. Cadastro:

URL: http://localhost:5000/auth/cadastro
```bash
Body: {
    "nome": "Nome",   
    "email": "email@teste.com", 
    "senha": "123", 
    "permissao": "Comum"
    }
```

2. Login:

URL: http://localhost:5000/auth/login
```bash
Body: { 
    "email": "email@teste.com", 
    "senha": "123", 
    }
```

3. Recuperação de Senha:

URL: URL: http://localhost:5000/auth/reset-senha/<token-copiado-no-email>

Envie o e-mail via **/auth/reset-senha**
Copie o token enviado para o e-mail.
Use a rota **/reset-senha/<token-copiado-no-email>** com o JSON 
```bash
{
nova_senha": "nova_senha_123"
}
```

---

Em desenvolvimento...