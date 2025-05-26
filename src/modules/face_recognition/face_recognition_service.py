import os
import face_recognition
import numpy as np
from typing import List, Dict, Tuple, Optional
from pathlib import Path
import shutil

class FaceRecognitionService:
    def __init__(self, student_faces_dir: str = "public/assets/images/student-face"):
        self.student_faces_dir = student_faces_dir
        self.known_face_encodings = {}
        self.known_face_ids = []
        self._load_known_faces()

    def _load_known_faces(self) -> None:
        for student_id in os.listdir(self.student_faces_dir):
            student_path = os.path.join(self.student_faces_dir, student_id)
            if not os.path.isdir(student_path):
                continue

            face_encodings = []
            for image_file in os.listdir(student_path):
                if not image_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    continue

                image_path = os.path.join(student_path, image_file)
                try:
                    image = face_recognition.load_image_file(image_path)
                    face_encodings = face_recognition.face_encodings(image)
                    
                    if face_encodings:
                        self.known_face_encodings[student_id] = face_encodings[0]
                        self.known_face_ids.append(student_id)
                except Exception as e:
                    print(f"Error loading face for student {student_id}: {str(e)}")

    def recognize_face(self, image_path: str) -> Optional[str]:
        try:
            unknown_image = face_recognition.load_image_file(image_path)
            unknown_face_encodings = face_recognition.face_encodings(unknown_image)
            
            if not unknown_face_encodings:
                return None

            unknown_face_encoding = unknown_face_encodings[0]
            
            matches = face_recognition.compare_faces(
                list(self.known_face_encodings.values()),
                unknown_face_encoding,
                tolerance=0.6
            )
            
            if True in matches:
                first_match_index = matches.index(True)
                return self.known_face_ids[first_match_index]
            
            return None
            
        except Exception as e:
            print(f"Error recognizing face: {str(e)}")
            return None

    def add_student_face(self, student_id: str, image_path: str) -> bool:
        try:
            print(image_path)
            student_dir = os.path.join(self.student_faces_dir, student_id)
            os.makedirs(student_dir, exist_ok=True)
            
            image = face_recognition.load_image_file(image_path)
            face_encodings = face_recognition.face_encodings(image)
            
            if not face_encodings:
                return False
                
            self.known_face_encodings[student_id] = face_encodings[0]
            self.known_face_ids.append(student_id)
            
            return True
            
        except Exception as e:
            print(f"Error adding student face: {str(e)}")
            return False

    def remove_student_face(self, student_id: str) -> bool:
        try:
            student_dir = os.path.join(self.student_faces_dir, student_id)
            
            if not os.path.exists(student_dir):
                return False
                
            if student_id in self.known_face_encodings:
                del self.known_face_encodings[student_id]
                self.known_face_ids.remove(student_id)
            
            shutil.rmtree(student_dir)
            return True
            
        except Exception as e:
            print(f"Error removing student face: {str(e)}")
            return False

    def remove_all_student_faces(self) -> bool:
        try:
            if not os.path.exists(self.student_faces_dir):
                return False
                
            self.known_face_encodings.clear()
            self.known_face_ids.clear()
            
            shutil.rmtree(self.student_faces_dir)
            os.makedirs(self.student_faces_dir, exist_ok=True)
            
            return True
            
        except Exception as e:
            print(f"Error removing all student faces: {str(e)}")
            return False 