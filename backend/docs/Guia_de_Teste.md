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

### 🔐 1. Autenticação & Usuários

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

URL: http://localhost:5000/auth/reset-senha/<token-copiado-no-email>

Envie o e-mail via **/auth/reset-senha**
Copie o token enviado para o e-mail.
Use a rota **/reset-senha/<token-copiado-no-email>** com o JSON 
```bash
{
nova_senha": "nova_senha_123"
}
```

---

### 📝 2. Ordens de Serviço (OS)
Fluxo de suporte técnico para usuários solicitarem auxílio.

| Método | Rota | Descrição |
|----------|----------|----------|
| POST  | /os/  | Abre uma nova OS (Vincula automaticamente dados do usuário).  |
| GET  | /os/minhas-os/<id_user>  | Lista todas as ordens abertas pelo usuário logado. |
| GET  | /os/todas | [ADM] Visualiza todas as ordens de serviço do sistema.  |
| PUT  | /os/<id_user> | Atualiza dados da OS ou finaliza o chamado (ADM/User).  |
| DELETE  | /os/<id_user> | Remove/Cancela uma ordem de serviço do banco.  |



### 💻 3. Equipamentos (Inventário)
Cadastro e controle de status dos itens disponíveis para reserva.

| Método | Rota | Descrição |
|----------|----------|----------|
| GET  | /equipamentos/  | Lista todos os equipamentos e seus status (Disponível, Reservado, Manutenção).  |
| POST  | /equipamentos/  | [ADM] Cadastra um novo item no inventário. |
| PUT  | /equipamentos/<id_equipe> | [ADM] Atualiza dados ou status de um equipamento. |
| DELETE  | /equipamentos/<id_equipe> |[ADM] Remove um equipamento do sistema. |

### 📅 4. Reservas de Equipamentos
Lógica de agendamento com controle automático de disponibilidade.

| Método | Rota | Descrição |
|----------|----------|----------|
| POST  | /reservas/ | Cria reserva e muda status do item para 'Reservado'.  |
| GET  | /reservas/minhas-reservas/<id_user>  | Lista histórico de reservas do usuário logado. |
| GET  | /reservas/todas  |[ADM] Painel geral com todas as reservas solicitadas. |
| PUT  | /reservas/<id_res> | Envia e-mail com token de recuperação.  |
| DELETE  | /reservas/<id_res>  | Cancela reserva e libera o item para 'Disponível'. |

### 👥 5. Gerenciamento de Usuários (ADM)
Controle total do painel administrativo sobre as contas do sistema.

| Método | Rota | Descrição |
|----------|----------|----------|
| GET  | /usuarios/ | [ADM] Lista todos os usuários cadastrados  |
| POST  | /usuarios/  | [ADM] Cria um novo usuário diretamente (Adm/Comum). |
| PUT  | /usuarios/<id_user> |[ADM] Edita dados, permissões, status ou reseta senha.|
| DELETE  | /usuarios/<id_user> | [ADM] Remove permanentemente um usuário do sistema. |
