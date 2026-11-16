from pydantic import BaseModel 
from datetime import datetime

class Log(BaseModel) : 
    received_at : datetime 
    vendor : str
    topic : str 
    level : str 
    message : str 
    