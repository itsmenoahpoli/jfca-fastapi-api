from pydantic import BaseModel, Field, EmailStr, field_validator
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

	@field_validator('contact', 'guardian_mobile_number')
	@classmethod
	def format_phone_number(cls, v):
		return v.replace(' ', '').replace('-', '')