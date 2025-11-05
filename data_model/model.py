import re
from pydantic import BaseModel,Field,field_validator

class DateTimeModel(BaseModel):
    date:str=Field(description="Properly formatted time and data", pattern=r"^\d{2}-\d{2}-\d{4} \d{2}:\d{2}$")
    @field_validator("date")
    def validate_datetime(cls,v):
        if not re.match(r"^\d{2}-\d{2}-\d{4} \d{2}:\d{2}$",v):
            raise ValueError("Datetime format should be DD-MM-YYYY HH:MM")
        return v
                            
class DateModel(BaseModel):
    date:str=Field(Description="Properly formatted date", pattern=r"^\d{2}-\d{2}-\d{4}$")
    
    @field_validator("date")
    def time_validator(cls,v):
        if not re.match(r"^\d{2}-\d{2}-\d{4}$",v):
            raise ValueError("date format should be DD-MM-YYYY")
        return v
    
class IdentificationNumberModel(BaseModel):
    id_number:str=Field(description="Properly formatted id number with 7,8 digit",pattern=r"^\d{7,8}$") 
    @field_validator("Id_number")
    def if_num_validator(cls,v):
        if not re.match(r"^\d{7,8}$",v):
            raise ValueError("ID number should be 7 or 8 digits")
        return v
        
    
  
