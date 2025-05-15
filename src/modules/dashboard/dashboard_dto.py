from pydantic import BaseModel

class DashboardCountsResponse(BaseModel):
    total_students: int
    total_sections: int
    total_user_roles: int
    total_users: int 