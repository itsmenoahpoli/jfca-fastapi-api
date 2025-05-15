from src.database import entities
from src.modules.base_repository import BaseRepository

class SectionsService(BaseRepository):
    def __init__(self):
        super().__init__(entity=entities.SectionEntity)
        
    def get_list_data(self):
        sections = super().get_list_data()
        
        for section in sections:
            students = entities.StudentEntity.find({"section_id": section["id"]})
            section["students"] = [self._single_serializer(student) for student in students]
            
        return sections
        
    def get_single_data(self, id):
        section = super().get_single_data(id)
            
        students = entities.StudentEntity.find({"section_id": id})
        section["students"] = [self._single_serializer(student) for student in students]
        
        return section

sections_service = SectionsService()