from src.database import entities
from src.modules.base_repository import BaseRepository
from src.utils.image_utils import get_image_url
from datetime import datetime
import os
import shutil
from fastapi import UploadFile
from bson import ObjectId

class StudentsService(BaseRepository):
    def __init__(self):
        super().__init__(entity=entities.StudentEntity)
    
    def get_next_student_key(self):
        latest_student = self._entity.find_one(
            sort=[("student_key", -1)]
        )
        
        if latest_student and "student_key" in latest_student:
            current_number = int(latest_student["student_key"].split("_")[1])
            next_number = current_number + 1
        else:
            next_number = 1
            
        return f"STUDENT_{next_number:02d}"
    
    def create_data(self, data: dict, flag_unique_by: str = None):
        data["student_key"] = self.get_next_student_key()
        if "contact" in data:
            data["contact"] = data["contact"].replace(" ", "").replace("-", "")
        if "guardian_mobile_number" in data:
            data["guardian_mobile_number"] = data["guardian_mobile_number"].replace(" ", "").replace("-", "")
        return super().create_data(data, flag_unique_by)
    
    def get_list_data(self):
        students = super().get_list_data()
        
        for student in students:
            if student.get("section_id"):
                try:
                    section = entities.SectionEntity.find_one({"_id": ObjectId(student["section_id"])})
                    if section:
                        student["section"] = {
                            "id": str(section["_id"]),
                            "name": section.get("name", ""),
                            "level": section.get("level", ""),
                            "school_year": section.get("school_year", "")
                        }
                except:
                    pass
        
        return students
    
    def process_student_images(self, student_id: str, photo1: UploadFile, photo2: UploadFile, photo3: UploadFile):
        photo_dir = f"public/assets/images/student-face/{student_id}"
        os.makedirs(photo_dir, exist_ok=True)
        
        photo_mapping = {
            photo1: "facefront",
            photo2: "faceleft",
            photo3: "faceright"
        }
        
        image_paths = {}
        for photo, filename in photo_mapping.items():
            if photo is not None:
                file_path = f"{photo_dir}/{filename}.jpg"
                with open(file_path, "wb") as buffer:
                    shutil.copyfileobj(photo.file, buffer)
                image_paths[filename] = get_image_url(f"student-face/{student_id}/{filename}.jpg")
        
        return image_paths

    def rename_student_images(self, temp_id: str, actual_id: str):
        if not actual_id or actual_id == "None":
            return None
        
        temp_dir = f"public/assets/images/student-face/{temp_id}"
        actual_dir = f"public/assets/images/student-face/{actual_id}"
        
        if os.path.exists(temp_dir):
            if os.path.exists(actual_dir):
                shutil.rmtree(actual_dir)
            os.rename(temp_dir, actual_dir)
            
            image_paths = {}
            for filename in ["facefront", "faceleft", "faceright"]:
                image_paths[filename] = get_image_url(f"student-face/{actual_id}/{filename}.jpg")
            
            return image_paths
        return None

    def delete_student_and_images(self, student_id):
        result = self.delete_data(student_id)
        image_dir = f"public/assets/images/student-face/{student_id}"
        if os.path.exists(image_dir):
            shutil.rmtree(image_dir)
        return result

    def format_all_student_mobile_numbers(self):
        students = self._entity.find()
        updated_count = 0
        
        for student in students:
            update_data = {}
            needs_update = False
            
            if "contact" in student:
                formatted_contact = student["contact"].replace(" ", "").replace("-", "")
                if formatted_contact != student["contact"]:
                    update_data["contact"] = formatted_contact
                    needs_update = True
                    
            if "guardian_mobile_number" in student:
                formatted_guardian = student["guardian_mobile_number"].replace(" ", "").replace("-", "")
                if formatted_guardian != student["guardian_mobile_number"]:
                    update_data["guardian_mobile_number"] = formatted_guardian
                    needs_update = True
            
            if needs_update:
                self._entity.update_one(
                    {"_id": student["_id"]},
                    {"$set": update_data}
                )
                updated_count += 1
        
        return {
            "total_updated": updated_count,
            "message": f"Successfully updated {updated_count} student records"
        }

    def get_single_data(self, id: str):
        student = super().get_single_data(id)
        
        if student and student.get("section_id"):
            try:
                section = entities.SectionEntity.find_one({"_id": ObjectId(student["section_id"])})
                if section:
                    student["section"] = {
                        "id": str(section["_id"]),
                        "name": section.get("name", ""),
                        "level": section.get("level", ""),
                        "school_year": section.get("school_year", "")
                    }
            except:
                pass
        
        return student

students_service = StudentsService()