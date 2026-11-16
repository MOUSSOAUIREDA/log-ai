from .prompt_service import build_prompt
from .llm_service import ask_llm
from app.knowledge.retreiver import search_knowledge

def classify_question(question : str) -> str : 
    
    file_name = "prompt_llm_classifier.txt"
    
    prompt = build_prompt(file_name , question)
    
    return ask_llm(prompt).strip()

def get_file_name(classification : str) -> str : 
    if classification == "EXPLAIN_LOG_TEMPLATE" :
        return "prompt_explain_log.txt"
    
    elif  classification == "DIAGNOSE_PROBLEM" : 
        return "prompt_diagnose_problem.txt"
    
    elif classification == "PROPOSE_SOLUTION" : 
        return "prompt_propose_solution.txt"
    
    else : 
        return "prompt_explain_technology.txt"

def build_context(results : list[dict]) -> str : 
    
    context = ""
    
    for i, result in enumerate(results, start = 1) : 
        context += f"---- Document {i} ----\n"
        context += f"score : {result['score']}\n"
        context += f"{result['text']}\n\n"
        
    return context.strip()

def handle_question(question : str ) :
    
    classification = classify_question(question)
    
    if classification == "OUT_OF_SCOPE" : 
        return {
    "response": "Je suis un assistant spécialisé dans l'analyse des logs, le diagnostic des problèmes techniques, la proposition de solutions et l'explication des technologies liées aux systèmes d'infrastructure informatique. "
               }
    
    file_name = get_file_name(classification)
    
    results = search_knowledge(question)
    
    context = build_context(results)
    
    prompt = build_prompt(file_name, question, context)
    
    return { 
            "response":
        ask_llm(prompt).strip()
    }