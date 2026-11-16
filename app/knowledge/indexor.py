import uuid 

from .loader import get_knowledge_files , load_knowledge_file
from .transformer import knowledge_to_text
from .embedder import generate_embedding
from .qdrant_client import client , COLLECTION_NAME

from qdrant_client.models import PointStruct

def index_knowledge() : 
    
    points = []
    
    files = get_knowledge_files()
    
    for path in files : 
        
        print(f"Traitement de : {path}")
        
        knowledge_list = load_knowledge_file(path)
        
        for index , knowledge in enumerate(knowledge_list) : 
            
            text = knowledge_to_text(knowledge)
            
            vector = generate_embedding(text)
            
            point_id = str(
                uuid.uuid5(
                    uuid.NAMESPACE_URL , 
                    f"{path}:{index}"
                )
            )
            
            point = PointStruct(
                id = point_id , 
                vector = vector , 
                payload = {
                    "text": text,
                    "vendor": knowledge.get("vendor",""),
                    "topic": knowledge.get("topic",""),
                    "component": knowledge.get("component",""),
                    "title": knowledge.get("title",""),
                    "source_file": str(path),
                    "object_index": index
                }
            )
            
            points.append(point)
    
    client.upsert(
        collection_name = COLLECTION_NAME , 
        points = points 
    )
    
    print(f"{len(points)} documents indexés.") 

index_knowledge()