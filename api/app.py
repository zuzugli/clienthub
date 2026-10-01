import os

import pymysql
from flask import Flask, jsonify, request

app = Flask(__name__)

# Configuration de la connexion MySQL via des variables d'environnement
# (les valeurs sont fournies par docker-compose.yml)
DB_HOST = os.environ.get("DB_HOST", "db")
DB_PORT = int(os.environ.get("DB_PORT", "3306"))
DB_NAME = os.environ.get("DB_NAME", "clienthub")
DB_USER = os.environ.get("DB_USER", "clienthub_user")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "")


def get_connection():
    """Ouvre une connexion à la base MySQL avec le driver pymysql."""
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
    )


def init_db():
    """Crée la table clients si elle n'existe pas encore."""
    connection = get_connection()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS clients (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL
                )
            """)
        connection.commit()


@app.route("/health")
def health():
    """Vérifie que l'API répond (n'utilise pas la base)."""
    return jsonify({"status": "ok"}), 200


@app.route("/who")
def who():
    """Retourne le prénom et le nom de l'auteur sous forme de chaîne de caractères."""
    return "Zuzanna Gliniak"


@app.route("/clients", methods=["GET"])
def list_clients():
    """Lit la liste des clients dans MySQL."""
    init_db()
    connection = get_connection()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, name FROM clients ORDER BY id")
            clients = cursor.fetchall()
    return jsonify({"source": "mysql", "count": len(clients), "clients": clients})


@app.route("/clients", methods=["POST"])
def add_client():
    """Insère un client dans MySQL puis le relit depuis la base."""
    data = request.get_json(silent=True) or {}
    name = data.get("name")
    if not name:
        return jsonify({"error": "le champ 'name' est obligatoire"}), 400

    init_db()
    connection = get_connection()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO clients (name) VALUES (%s)", (name,))
            new_id = cursor.lastrowid
            connection.commit()
            cursor.execute("SELECT id, name FROM clients WHERE id = %s", (new_id,))
            client = cursor.fetchone()
    return jsonify(client), 201


if __name__ == "__main__":
    # 0.0.0.0 : écouter sur toutes les interfaces pour être joignable hors du conteneur
    app.run(host="0.0.0.0", port=5000)
