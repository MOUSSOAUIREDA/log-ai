from pathlib import Path
import json 

def load_prompt(file_name) -> str : 
    
    prompt_path = Path(__file__).resolve().parent.parent / "prompt" / file_name
    
    return prompt_path.read_text(encoding="utf-8")

def build_prompt_llm_analysis(result : dict ) -> str : 
    
    prompt = load_prompt("prompt.txt")
    
    result_json = json.dumps( result , indent = 2 , ensure_ascii = False, default=str)
    
    return prompt.replace("{result}", result_json)


def build_prompt(file_name : str, question : str, context : str = "") -> str : 
    
    prompt = load_prompt(file_name)
    
    return (
        prompt
        .replace("{question}", question)
        .replace("{context}", context)
    )
