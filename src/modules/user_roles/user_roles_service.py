from src.database import entities
from src.modules.base_repository import BaseRepository

class UserRolesService(BaseRepository):
    def __init__(self):
        super().__init__(entity=entities.UserRoleEntity)
        
        

user_roles_service = UserRolesService()