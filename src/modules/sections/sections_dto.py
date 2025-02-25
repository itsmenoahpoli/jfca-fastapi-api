from pydantic import BaseModel, Field

class SectionDTO(BaseModel):
	name: str = Field(min_length=1, max_length=100)
	level: str = Field(min_length=1, max_length=100)
	school_year: str = Field(min_length=1, max_length=100)
	is_enabled: bool