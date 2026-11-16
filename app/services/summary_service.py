
from datetime import date 
from .log_service import get_logs_from_source
from .log_analyzer import build_log_analysis
from .report_service import generate_markdown_report
from .prompt_service import build_prompt_llm_analysis
from .llm_service import ask_llm

from app.celery_app import celery_app

def determine_log_source(requested_date : date ) : 
    
    today = date.today()
    
    days_difference = (today - requested_date).days 
    
    if days_difference > 30 : 
        return "s3"
    else : 
        return "clickhouse"

# le décorateur permet de déclarer summary comme tache de celery
# les arguments de la tache doivent etre sérialisable 
@celery_app.task 
def summary(source_id : str , requested_date : str ) : 
    
    requested_date = date.fromisoformat(requested_date)
    
    source = determine_log_source(requested_date)

    logs = get_logs_from_source(source_id, requested_date, "clickhouse")
    
    if not logs : 
        return {
            "message" : "Aucun log trouvé pour cette source et cette date."
        }
        
    result = build_log_analysis(logs)
    
    structured_analysis = generate_markdown_report(result)
    
    prompt = build_prompt_llm_analysis(result)
    
    llm_analysis = ask_llm(prompt)
    
    return {
         "structured_analysis": structured_analysis,
    "hierarchical_analysis": llm_analysis
    }

    
    
    
