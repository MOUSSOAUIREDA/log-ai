from app.models.log import Log
from app.database.clickhouse import get_clickhouse_client
from datetime import date 

def get_logs_from_source(source_id : str ,requested_date : date , source : str  ) -> list[Log] : 
    logs = []
    
    if source == 'clickhouse' : 
        table = 'events'
    else : 
        # archive est une table clickhouse configuré pour utiliser S3
        table = 'archive'
    
    query = f"""
                SELECT received_at, vendor, topic,  level, message
                FROM {table}
                WHERE collector_id = {{source_id:String}}
                AND toDate(received_at) = {{requested_date:Date}}   
            """
    client = get_clickhouse_client()
          
    result = client.query(
        query ,
        parameters= {
            'source_id': source_id , 
            'requested_date': requested_date
        }
    )
    
    rows = result.result_rows
    
    for row in rows : 
        log = Log(
                received_at = row[0] ,
                vendor = row[1] , 
                topic = row[2] ,
                level = row[3] ,
                message = row[4] ,
        )
        
        logs.append(log)

    return logs 


