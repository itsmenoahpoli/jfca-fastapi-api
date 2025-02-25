from src.database import entities
from src.modules.base_repository import BaseRepository

class StudentsService(BaseRepository):
    def __init__(self):
        super().__init__(entity=entities.StudentEntity)
        
        

students_service = StudentsService()