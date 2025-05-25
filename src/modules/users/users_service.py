from src.database import entities
from src.modules.base_repository import BaseRepository
from src.utils.password_utils import hash_password

class UsersService(BaseRepository):
    def __init__(self):
        super().__init__(entity=entities.UserEntity)
        
    
    def find_by_email(self, email):
        user = self._entity.find_one({ "email": email })

        if user is None:
            return None

        return self._single_serializer(user)
        
    def create_data(self, data, flag_unique_by = None):
        if "password" in data:
            data["password"] = hash_password(data["password"])
        return super().create_data(data, "email")
    
    def update_data(self, id, data):
        if "password" in data:
            data["password"] = hash_password(data["password"])
        return super().update_data(id, data)

users_service = UsersService()