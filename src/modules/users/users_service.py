from src.database import entities
from src.modules.base_repository import BaseRepository

class UsersService(BaseRepository):
    def __init__(self):
        super().__init__(entity=entities.UserEntity)
        
    
    def find_by_email(self, email):
        user = self._entity.find_one({ "email": email })

        if user is None:
            return None

        return self._single_serializer(user)
        


users_service = UsersService()