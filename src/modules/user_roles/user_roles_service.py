from database import entities
from modules.base_repository import BaseRepository

class UserRolesService(BaseRepository):
    def __init__():
        super().__init__(entity=entities.UserRole)
        print('UserRolesService(BaseRepository(entity=entities.UserRole)) initialized')
        

user_roles_service = UserRolesService()