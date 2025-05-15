from pydantic import BaseModel, Field, EmailStr
from fastapi import UploadFile

class StudentDTO(BaseModel):
	name: str = Field(min_length=1, max_length=100)
	email: str = EmailStr()
	gender: str
	contact: str
	guardian_name: str
	guardian_relation: str
	guardian_mobile_number: str
	section_id: str 
	is_enabled: bool
	photo1: UploadFile
	photo2: UploadFile
	photo3: UploadFile