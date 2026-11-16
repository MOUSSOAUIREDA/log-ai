from qdrant_client import QdrantClient 
from qdrant_client.models import Distance , VectorParams


from app.config import QDRANT_API_KEY, QDRANT_URL

client = QdrantClient(
    url = QDRANT_URL , 
    check_compatibility=False,
    api_key = QDRANT_API_KEY
)
COLLECTION_NAME = "knowledge_base"

VECTOR_SIZE = 1024

def create_collection() : 
    
    collections = client.get_collections()
    
    exists = any(
        collection.name == COLLECTION_NAME
        for collection in collections.collections  
        )
    
    if not exists : 
        client.create_collection(
            collection_name = COLLECTION_NAME , 
            vectors_config = VectorParams(
                size = VECTOR_SIZE , 
                distance = Distance.COSINE
            )
        )
        
        print(f"Collection : {COLLECTION_NAME} créée.")
    else : 
        print(f"Collection : {COLLECTION_NAME} existe déjà.")


create_collection()