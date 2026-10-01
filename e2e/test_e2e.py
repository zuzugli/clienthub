"""Tests E2E : parcours réel via HTTP sur l'application lancée avec docker compose."""
import os
import time

import pytest
import requests

BASE_URL = os.environ.get("E2E_BASE_URL", "http://localhost:5000")


@pytest.fixture(scope="session", autouse=True)
def attendre_application():
    """Attend que l'API réponde avant de lancer les tests (60 s maximum)."""
    for _ in range(30):
        try:
            if requests.get(f"{BASE_URL}/health", timeout=2).status_code == 200:
                return
        except requests.ConnectionError:
            pass
        time.sleep(2)
    pytest.fail("L'application ne répond pas sur /health")


def test_disponibilite():
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_who():
    response = requests.get(f"{BASE_URL}/who")
    assert response.status_code == 200
    assert response.text == "Zuzanna Gliniak"


def test_clients_initialises_par_init_sql():
    response = requests.get(f"{BASE_URL}/clients")
    assert response.status_code == 200
    noms = [client["name"] for client in response.json()["clients"]]
    assert "Alice Martin" in noms


def test_parcours_ajout_puis_lecture_client():
    # 1. L'utilisateur ajoute un client
    response = requests.post(f"{BASE_URL}/clients", json={"name": "Client E2E"})
    assert response.status_code == 201
    nouveau = response.json()

    # 2. Il le retrouve ensuite dans la liste lue depuis MySQL
    response = requests.get(f"{BASE_URL}/clients")
    assert nouveau in response.json()["clients"]
