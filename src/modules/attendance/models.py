from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId

class AttendanceEntry(BaseModel):
    type: str = Field(..., description="Type of attendance (in/out)")
    time_recorded: datetime = Field(default_factory=datetime.utcnow)
    student_name: str
    sms_status: str = Field(..., description="Status of SMS notification (sent/not-sent)")
    student_id: ObjectId
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {
            ObjectId: str,
            datetime: lambda dt: dt.isoformat()
        } 