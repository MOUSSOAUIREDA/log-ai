from pathlib import Path 
import json

# Un objet Path qui contient le chemin knowledge 
KNOWLEDGE_PATH = Path("knowledge")

def get_knowledge_files() : 
    
    # à partir du chemin knowledge, récupère récursivement tous les fichiers qui correspondent à .json
    return list(KNOWLEDGE_PATH.rglob("*.json"))

def load_knowledge_file(path : Path) : 
    
    with open (path , "r" , encoding = "utf-8") as file : 
        return json.load(file)

