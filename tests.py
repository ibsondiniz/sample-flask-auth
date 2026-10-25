import os

# Banco SQLite em memória: os testes não precisam do MySQL
os.environ["DATABASE_URL"] = "sqlite://"
os.environ.setdefault("SECRET_KEY", "teste")

import pytest
from app import app
from database import db
from models.user import User


@pytest.fixture
def client():
    with app.app_context():
        db.drop_all()
        db.create_all()
    return app.test_client()


def cadastrar(client, username, password):
    return client.post("/user", json={"username": username, "password": password})


def entrar(client, username, password):
    return client.post("/login", json={"username": username, "password": password})


def test_cadastro_e_login(client):
    assert cadastrar(client, "ana", "123").status_code == 200
    assert entrar(client, "ana", "errada").status_code == 400
    assert entrar(client, "ana", "123").status_code == 200
    assert client.get("/user/1").get_json() == {"username": "ana"}


def test_rotas_exigem_login(client):
    cadastrar(client, "ana", "123")
    resposta = client.get("/user/1")
    assert resposta.status_code == 302  # login_view manda para /login
    assert resposta.location.startswith("/login")


def test_troca_de_senha_vale_no_proximo_login(client):
    cadastrar(client, "ana", "123")
    entrar(client, "ana", "123")
    assert client.put("/user/1", json={"password": "nova"}).status_code == 200
    client.get("/logout")
    assert entrar(client, "ana", "123").status_code == 400
    assert entrar(client, "ana", "nova").status_code == 200


def test_usuario_comum_nao_altera_nem_apaga_outro(client):
    cadastrar(client, "ana", "123")
    cadastrar(client, "bia", "456")
    entrar(client, "ana", "123")
    assert client.put("/user/2", json={"password": "x"}).status_code == 403
    assert client.delete("/user/2").status_code == 403


def test_admin_apaga_outro_mas_nao_a_si_mesmo(client):
    cadastrar(client, "admin", "123")
    cadastrar(client, "bia", "456")
    with app.app_context():
        db.session.get(User, 1).role = "admin"
        db.session.commit()
    entrar(client, "admin", "123")
    assert client.delete("/user/1").status_code == 403
    assert client.delete("/user/2").status_code == 200
    assert client.get("/user/2").status_code == 404
