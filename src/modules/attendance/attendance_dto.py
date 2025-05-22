from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AttendanceCreateDTO(BaseModel):
    student_id: str
    status: str
    notes: Optional[str] = None


class AttendanceUpdateDTO(BaseModel):
    status: Optional[str] = None
    notes: Optional[str] = None


class AttendanceResponseDTO(BaseModel):
    _id: str
    student_id: str
    status: str
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime


class TimeInOutResponseDTO(BaseModel):
    _id: str
    student_id: str
    date_recorded: datetime
    time_in: Optional[datetime]
    time_out: Optional[datetime]
    in_status: bool
    out_status: bool
    sms_notif_status: str
    created_at: datetime
    updated_at: datetime


class TimeInOutDTO(BaseModel):
    student_id: str 