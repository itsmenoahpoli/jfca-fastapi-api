from src.database.entities import StudentEntity
from bson import ObjectId

def seed_student_keys():
    students = list(StudentEntity.find().sort("createdAt", 1))
    updated_count = 0
    
    for index, student in enumerate(students, 1):
        student_key = f"STUDENT_{index:02d}"
        
        StudentEntity.update_one(
            {"_id": student["_id"]},
            {"$set": {"student_key": student_key}}
        )
        updated_count += 1
    
    print(f"Successfully updated {updated_count} student records with student_key values")

if __name__ == "__main__":
    seed_student_keys() 