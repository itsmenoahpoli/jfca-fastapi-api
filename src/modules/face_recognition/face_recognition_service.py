import os
import face_recognition
import numpy as np
from typing import List, Dict, Tuple, Optional
from pathlib import Path

class FaceRecognitionService:
    def __init__(self, student_faces_dir: str = "public/assets/images/student-face"):
        self.student_faces_dir = student_faces_dir
        self.known_face_encodings = {}
        self.known_face_ids = []
        self._load_known_faces()

    def _load_known_faces(self) -> None:
        """Load all known faces from the student faces directory"""
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
        """
        Recognize a face in the given image and return the student ID if found
        
        Args:
            image_path: Path to the image file containing the face to recognize
            
        Returns:
            Optional[str]: Student ID if a match is found, None otherwise
        """
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
        """
        Add a new face for a student
        
        Args:
            student_id: ID of the student
            image_path: Path to the image file containing the face
            
        Returns:
            bool: True if face was successfully added, False otherwise
        """
        try:
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