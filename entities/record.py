from pydantic import BaseModel
from datetime import datetime

class Record(BaseModel):
    user_name:str
    message:str
    table:str
    time: datetime
