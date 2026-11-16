from .embedder import generate_embedding
from .qdrant_client import client ,COLLECTION_NAME

def search_knowledge(question : str , limit : int = 5 ) : 
    
    question_vector = generate_embedding(question)
    
    results = client.query_points(
        collection_name = COLLECTION_NAME , 
        query = question_vector , 
        limit = limit 
    )
    
    documents = []
    
    for result in results.points : 
        documents.append(
            {
                "score" : result.score , 
                "text" : result.payload["text"]
            }
        )
        
    return documents 
