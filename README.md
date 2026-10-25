# sample-flask-auth

API REST de usuários com autenticação em Python e Flask: cadastro, login e logout com sessão (Flask-Login), senhas criptografadas com bcrypt e permissões por papel (`user` e `admin`). Os dados ficam em MySQL, acessado pelo SQLAlchemy, com o banco rodando em Docker Compose.

Projeto de estudo feito em 2024.

## Rotas

| Método | Rota | Login | O que faz |
| --- | --- | --- | --- |
| POST | `/user` | não | Cadastra um usuário com papel `user`. Corpo: `username` e `password`. |
| POST | `/login` | não | Entra. Corpo: `username` e `password`. A sessão fica num cookie. |
| GET | `/logout` | sim | Sai. |
| GET | `/user/<id>` | sim | Mostra o `username`. |
| PUT | `/user/<id>` | sim | Troca a senha. Corpo: `password`. Um `user` só troca a própria; um `admin` troca a de qualquer um. |
| DELETE | `/user/<id>` | sim | Apaga um usuário. Só `admin`, e nunca a própria conta. |

Sem login, as rotas protegidas redirecionam para `/login` (302).

## Como rodar

Precisa de Python 3 e Docker.

1. Copie o modelo de configuração e troque as senhas e a chave:

   ```bash
   cp .env.example .env
   ```

2. Suba o MySQL:

   ```bash
   docker compose up -d
   ```

3. Instale as dependências e rode a API. As tabelas são criadas na primeira execução.

   ```bash
   python -m venv venv
   venv\Scripts\activate        # Windows
   source venv/bin/activate     # Linux ou macOS
   pip install -r requirements.txt
   python app.py
   ```

A API fica em `http://127.0.0.1:5000`. Todo usuário nasce com o papel `user`. Para tornar um usuário `admin`:

```bash
docker compose exec db mysql -u admin -p flask-crud -e "UPDATE \`user\` SET role='admin' WHERE username='seu_usuario';"
```

## Testes

```bash
pytest tests.py
```

Os testes usam SQLite em memória, então não precisam do MySQL nem do `.env`. Eles cobrem cadastro e login, rota protegida, troca de senha seguida de novo login e as permissões de `user` e `admin`.

## Tecnologias

Python, Flask, Flask-Login, Flask-SQLAlchemy, bcrypt, MySQL, Docker Compose e pytest.
