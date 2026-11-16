from app.knowledge.qdrant_client import create_collection
from app.knowledge.indexor import index_knowledge

def intialize_knowledge_base() : 
    print("Initialisation de la knowledge base...")

    create_collection()
    index_knowledge()

    print("Knowledge base initialisée.")