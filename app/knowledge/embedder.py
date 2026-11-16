from app.config import EMBEDDING_MODEL
from sentence_transformers import SentenceTransformer
from .loader import load_knowledge_file , get_knowledge_files
from .transformer import knowledge_to_text
model = SentenceTransformer(EMBEDDING_MODEL)

def generate_embedding( text : str ) -> list[float] : 
    
    embedding = model.encode(text)
    
    return embedding.tolist()

