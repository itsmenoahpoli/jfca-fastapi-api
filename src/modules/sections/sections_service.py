from src.database import entities
from src.modules.base_repository import BaseRepository

class SectionsService(BaseRepository):
    def __init__(self):
        super().__init__(entity=entities.SectionEntity)
        
        

sections_service = SectionsService()