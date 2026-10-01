import pymysql

import app as app_module
from app import app


def test_health():
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_who():
    client = app.test_client()
    response = client.get("/who")
    assert response.status_code == 200
    assert response.get_data(as_text=True) == "Zuzanna Gliniak"


def test_clients_sans_base(monkeypatch):
    # On simule une base MySQL injoignable
    def connexion_impossible():
        raise pymysql.err.OperationalError(2003, "connexion impossible")

    monkeypatch.setattr(app_module, "get_connection", connexion_impossible)

    client = app.test_client()
    response = client.get("/clients")
    assert response.status_code == 503
    assert response.get_json() == {"error": "base de données indisponible"}


def test_ajout_client_sans_nom():
    client = app.test_client()
    response = client.post("/clients", json={})
    assert response.status_code == 400
