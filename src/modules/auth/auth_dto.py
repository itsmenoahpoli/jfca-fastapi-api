from pydantic import BaseModel

class SigninDTO(BaseModel):
	email: str;
	password: str;
    
