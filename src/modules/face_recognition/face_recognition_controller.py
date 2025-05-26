from fastapi import APIRouter, UploadFile, File, HTTPException
from src.modules.face_recognition.face_recognition_service import FaceRecognitionService
import os
import shutil
from typing import Optional

router = APIRouter(prefix="/face-recognition", tags=["Face Recognition"])
face_service = FaceRecognitionService()

@router.post("/recognize")
async def recognize_face(file: UploadFile = File(...)) -> dict:
    """
    Recognize a face from an uploaded image
    """
    try:
        temp_file_path = f"temp_{file.filename}"
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        student_id = face_service.recognize_face(temp_file_path)
        os.remove(temp_file_path)
        
        if student_id:
            return {"student_id": student_id}
        else:
            raise HTTPException(status_code=404, detail="Face not recognized")
            
    except Exception as e:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/add-face/{student_id}")
async def add_student_face(student_id: str, file: UploadFile = File(...)) -> dict:
    """
    Add a new face for a student
    """
    try:
        temp_file_path = f"temp_{file.filename}"
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        success = face_service.add_student_face(student_id, temp_file_path)
        os.remove(temp_file_path)
        
        if success:
            return {"message": "Face added successfully"}
        else:
            raise HTTPException(status_code=400, detail="Failed to add face")
            
    except Exception as e:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/remove-face/{student_id}")
async def remove_student_face(student_id: str) -> dict:
    """
    Remove a student's face from the recognition system
    """
    try:
        success = face_service.remove_student_face(student_id)
        
        if success:
            return {"message": "Face removed successfully"}
        else:
            raise HTTPException(status_code=404, detail="Student face not found")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/remove-all-faces")
async def remove_all_student_faces() -> dict:
    """
    Remove all student faces from the recognition system
    """
    try:
        success = face_service.remove_all_student_faces()
        
        if success:
            return {"message": "All faces removed successfully"}
        else:
            raise HTTPException(status_code=404, detail="No faces found to remove")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 