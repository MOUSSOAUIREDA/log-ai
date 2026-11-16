from pydantic import BaseModel
from datetime import date 

class SummaryRequest(BaseModel) : 
    source_id : str 
    requested_date : str




