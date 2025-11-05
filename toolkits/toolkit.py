import pandas as pd 
from typing import Literal 
from langchain_core.tools import tool 
from data_model.model import *

@tool
def check_availability_specialization(desired_date:DateModel,specialization:Literal["general_dentist","cosmetic_dentist","prosthodontist","pediatric_dentist","emergency_dentist","oral_surgeon","orthodontist"]):
    df=pd.read.csv("../data/doctor_availability.csv")
    df["date_time_slot"]=df["date_slot"].apply(lambda input: input.spilt('')[-1])
    rows=df[(df["date_slot"].apply(lambda input: input.split(' ')[0])==desired_date.date)&(df["is_available"]==True)].groupby(['specialization','doctor_name'])['date_slot_time'].apply(list).reset_index(name='available_time_slots')
    if len(rows)==0:
        return f"no doctors available for {specialization} on {desired_date.date}"
    else:
        def convert_to_am_pm(time_str):
            time_str=str(time_str)
            hour, minute = map(int, time_str.split(':')) 
            period='AM' if hour<12 else 'PM' 
            
            hour=hour %12 or 12 
            return f"{hour}:{minute:02d} {period}"   
        print("this is the availability") 
    
@tool
def check_availability_by_name(desired_date:DateModel,doctor_name:str):
    df=pd.read.csv("../data/doctor_availability.csv")
    df["date_time_slot"]=df["date_slot"].apply(lambda input: input.spilt('')[-1])
    rows=df[(df["date_slot"].apply(lambda input: input.split(' ')[0])==desired_date.date)&(df["doctor_name"]==doctor_name)&(df["is_available"]==True)]['date_slot_time']
    if len(rows)==0:
        output=f"no availability for Dr.{doctor_name} on {desired_date}"
    else:
        output=f"Dr.{doctor_name}is available on {desired_date.date}"
        
    return output
@tool


def book_appointment(desired_time:DateTimeModel, id:IdentificationNumberModel,doctor_name:Literal['kevin anderson','robert martinez','susan davis','daniel miller','sarah wilson','michael green','lisa brown','jane smith','emily johnson','john doe']):
    from datetime import datetime
    # def convert_datetime_format(dt_str):
    #     # Parse the input datetime string
    #     #dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
    #     dt = datetime.strptime(dt_str, "%d-%m-%Y %H:%M")
        
    #     # Format the output as 'DD-MM-YYYY H.M' (removing leading zero from hour only)
    #     return dt.strftime("%d-%m-%Y %#H.%M")
    
    
    df=pd.read.csv("../data/doctor_availability.csv")
    mask=(df["date_slot"]==desired_time.date)&(df["doctor_name"]==doctor_name)&(df["is_available"]==True)
    if df[mask].empty:
        return f"unable to book appointment with Dr.{doctor_name} at {desired_time.date}. either the doctor is not available at that time or the time slot is already booked."
    else:
        df.loc[mask,"is_available"]=False
        df.to_csv("../data/doctor_availability.csv",index=False)
        return f"appointment successfully booked with Dr.{doctor_name} at {desired_time.date} for patient ID:{id.id_number}"

@tool
def cancel_appointment(date:DateTimeModel,id:IdentificationNumberModel,doctor_name:Literal['kevin anderson','robert martinez','susan davis','daniel miller','sarah wilson','michael green','lisa brown','jane smith','emily johnson','john doe']):
    df=pd.read_csv("../data/doctor_availability.csv")
    df=df[(df["date_slot"]==date.date) & (df["patient_to_attend"]==id.id_number) & (df["doctor_name"]==doctor_name)]
    if len(df)==0:
        return "you do ot have that appointment with that specification"
    else:
        df.loc[(df["date_slot"]==date.date) & (df["patient_to_attend"]==id.id_number) & (df["doctor_name"]==doctor_name),['is_available','patient_to_attend']]=[True,"None"]
        df.to_csv('../data/doctor_availability.csv',index=False)
        return "successfully removed"
    
    
@tool 
def reschedule_appointment(old_date:DateTimeModel,new_date:DateTimeModel,id: IdentificationNumberModel,doctor_name:Literal['kevin anderson','robert martinez','susan davis','daniel miller','sarah wilson','michael green','lisa brown','jane smith','emily johnson','john doe']):
    df=pd.read_csv("../data/doctor_availability.csv")
    availability_of_desired_date=df[(df["date_slot"]==new_date.date)&(df['is_available']==True)&(df["doctor_name"]==doctor_name)]
    if len(availability_of_desired_date)==0:
        return f"unable to reschedule appointment"
    else:
        cancel_appointment.invoke({'date':old_date, 'id_number':id, 'doctor_name':doctor_name})
        book_appointment.invoke({{'date':new_date, 'id_number':id, 'doctor_name':doctor_name}})
        
        return f"successfully rescheduled appointment to {new_date}  "
   