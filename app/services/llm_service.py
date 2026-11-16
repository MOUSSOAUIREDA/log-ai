from app.config import OLLAMA_HOST , OLLAMA_MODEL , OLLAMA_API_KEY
import requests 


def ask_llm(prompt : str ) -> str : 
    
    response = requests.post(
        f"{OLLAMA_HOST}/api/chat" , 
        
        headers =
            {
             "Authorization": f"Bearer {OLLAMA_API_KEY}",
             "Content-Type": "application/json",
            } ,
            
        json = {
            "model" : OLLAMA_MODEL , 
            
            "messages" : [
                {
                "role" : "user" , 
                "content" : prompt
                 }
            ], 
            
            "stream" : False
        }
    )
    
    response.raise_for_status()
    
    data = response.json()
    
    return data["message"]["content"]

