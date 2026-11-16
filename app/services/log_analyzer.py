from app.models.log import Log
from drain3 import TemplateMiner


def process_logs(logs : list[Log]) -> dict : 
    grouped = {}
    
    for log in logs : 
        vendor = log.vendor.lower().strip()
        topic = log.topic.lower().strip()
        level = log.level.lower().strip()
        
        if vendor not in grouped : 
            grouped[vendor] = {}
            
        if topic not in grouped[vendor] : 
            grouped[vendor][topic] = {}
            
        if level not in grouped[vendor][topic] : 
            grouped[vendor][topic][level] = []
            
        grouped[vendor][topic][level].append(log)
        
    return grouped 

def select_examples(logs : list[Log] , n = 3 ) -> list[str] : 
    
    length = len(logs)
    
    if length <= n : 
        return [log.message for log in logs]
    
    indexes = [
        0 , 
        length // 2 , 
        length - 1 
    ]
    
    return [logs[i].message for i in indexes]

def analyze_templates(logs : list[Log]) -> list[dict] : 
    
    miner = TemplateMiner()
    
    log_clusters = {}
    
    for log in logs : 
        parser_result = miner.add_log_message(log.message)
        
        cluster_id = parser_result["cluster_id"]
        
        if cluster_id not in log_clusters : 
            log_clusters[cluster_id] = []
            
        log_clusters[cluster_id].append(log)
    
    templates = []
    
    for cluster in miner.drain.clusters : 
        
        cluster_id = cluster.cluster_id
        template = cluster.get_template()
        
        associated_logs = log_clusters[cluster_id]
        
        
        templates.append({
            "template" : template , 
            "count" :  cluster.size, 
            "first_seen" : min(
                log.received_at for log in associated_logs
            ) , 
            "last_seen" : max(
                log.received_at for log in associated_logs
            ),
            "examples" : select_examples(associated_logs)
            })
        
    return templates

def build_analysis(grouped : dict) -> dict : 
    
    result = {}
    
    for vendor , topics in grouped.items() : 
        
        result[vendor] = {}
        
        for topic , levels in topics.items() : 
            result[vendor][topic] = {}
            
            for level, logs in levels.items() : 
                result[vendor][topic][level] = analyze_templates(logs)
                
    return result     

def build_log_analysis(logs : list[Log]) -> dict : 
    
    grouped = process_logs(logs)
    
    result = build_analysis(grouped)

    return result 


