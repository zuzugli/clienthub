# 1. Image Python adaptée (version légère "slim")
FROM python:3.12-slim

# Dossier de travail dans le conteneur
WORKDIR /app

# 2. Installation des dépendances via requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copie des fichiers de l'API dans l'image
COPY app.py .

# 4. Port interne utilisé par Flask
EXPOSE 5000

# 5. Commande de démarrage de l'application
CMD ["python", "app.py"]
