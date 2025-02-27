from pydantic import BaseModel, Field

class NotificationSmsDTO(BaseModel):
    message: str = Field(max_length=100)
    recipient: str