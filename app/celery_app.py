# Importer la classe Celery depuis la bib celery 
# qui va permettre de créer une application celery 
from celery import Celery 

# La création de l'application celery intitulée infralogs
# redis:// : indique à celery d'utiliser le protocole redis pour communiquer avec le serveur redis 
# redis : le nom du conteneur qui contient le serveur redis 
# 6379 : le port sur lequel le serveur redis écoute 
# Une base est un espace logique de stockage 
# /0 : la base logique Redis numéro 0 
celery_app = Celery(
             "infralogs" ,
             broker = "redis://redis:6379/0",
             backend = "redis://redis:6379/1" ,
             include=["app.services.summary_service"]
             )

