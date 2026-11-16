# Utiliser une image contenant Python 3.12 et une base système légère 
FROM python:3.12-slim 

# Créer/utiliser le répertoire /app comme espace de travail 
WORKDIR /app 

# Copier le fichier requirements.txt dans l'image 
COPY requirements-python.txt . 

# Installer les dépendances indiquées dans requirements.txt 
# sans conserver le cache de téléchargement de pip 
RUN pip install --no-cache-dir -r requirements-python.txt

# Copier l'application Python dans l'image 
COPY app ./app
COPY init_knowledge.py ./init_knowledge.py
COPY knowledge ./knowledge
# Le Dockerfile permet donc de construire une image contenant Python, les dépendances nécessaires et notre application.
# Après la construction de cette image, on peut créer et démarrer un conteneur à partir de celle-ci.


# Après le démarrage du conteneur, lancer Uvicorn
# Uvicorn récupère l'objet "app" contenant l'application web depuis le fichier main.py situé dans le dossier app.
# Il démarre ensuite le serveur et l'écoute sur le port 8001.
# --host 0.0.0.0 indique à Uvicorn d'écouter sur toutes les
# interfaces réseau du conteneur 

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]

#  docker compose exec python-api pip list : permet de savoir les versions des packages 