from app.services.log_analyzer import build_log_analysis
from app.services.log_service import get_logs_from_source

source_id = '019feb77-bf5e-70df-84b7-22859e04f2f0'
requested_date = '2026-08-15'

logs = get_logs_from_source(source_id , requested_date , 'clickhouse')

print(build_log_analysis(logs))