import clickhouse_connect



def get_clickhouse_client() : 
    
    from app.config import (
        CLICKHOUSE_HOST, 
        CLICKHOUSE_PORT , 
        CLICKHOUSE_USER,
        CLICKHOUSE_PASSWORD,
        CLICKHOUSE_DATABASE,
    )
    client = clickhouse_connect.get_client(
        host = CLICKHOUSE_HOST , 
        port = CLICKHOUSE_PORT ,
        username = CLICKHOUSE_USER , 
        password = CLICKHOUSE_PASSWORD , 
        database = CLICKHOUSE_DATABASE , 
        secure = True , 
        proxy_path = "/ch"
        )
    
    return client 