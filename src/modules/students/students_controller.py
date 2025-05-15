from fastapi import APIRouter, status, UploadFile, File, Form
from .students_service import students_service
from .students_dto import StudentDTO
from src.utils.http_utils import HTTPResponse
from src.utils.image_utils import get_image_url
from src.constants.errors_constant import ErrorTypes
import os
import shutil
from typing import List
from bson.objectid import ObjectId

students_router = APIRouter(
	prefix="/students",
	tags=["Student Profiles"]
)

@students_router.get('/')
async def get_list_handler():
	result = students_service.get_list_data()
	
	return HTTPResponse(
		detail=result,
		status_code=status.HTTP_200_OK
	)

@students_router.get('/{id}')
async def get_single_handler(id: str):
	result = students_service.get_single_data(id)
	
	if result is None or result == ErrorTypes.NOT_FOUND_ERROR:
		return HTTPResponse(
			detail="Student not found",
			status_code=status.HTTP_404_NOT_FOUND
		)
	
	return HTTPResponse(
		detail=result,
		status_code=status.HTTP_200_OK
	)

@students_router.delete('/{id}')
async def delete_one_handler(id):
	result = students_service.delete_student_and_images(id)
	if result is None or result == ErrorTypes.NOT_FOUND_ERROR:
		return HTTPResponse(
			detail="Student not found",
			status_code=status.HTTP_404_NOT_FOUND
		)
	return HTTPResponse(
		detail=True,
		status_code=status.HTTP_200_OK
	)

@students_router.patch('/{id}')
async def update_handler(
    id: str,
    name: str = Form(...),
    email: str = Form(...),
    gender: str = Form(...),
    contact: str = Form(...),
    guardian_name: str = Form(...),
    guardian_relation: str = Form(...),
    guardian_mobile_number: str = Form(...),
    section_id: str = Form(...),
    photo1: UploadFile = File(None),
    photo2: UploadFile = File(None),
    photo3: UploadFile = File(None)
):
    payload = {
        "name": name,
        "email": email,
        "gender": gender,
        "contact": contact,
        "guardian_name": guardian_name,
        "guardian_relation": guardian_relation,
        "guardian_mobile_number": guardian_mobile_number,
        "section_id": section_id,
    }

    if photo1 and photo2 and photo3:
        image_paths = students_service.process_student_images(id, photo1, photo2, photo3)
        payload["images"] = image_paths

    result = students_service.update_data(id, payload)

    if result == ErrorTypes.ALREADY_EXISTS:
        return HTTPResponse(
            detail=result,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )
    
    if not result or not isinstance(result, dict):
        return HTTPResponse(
            detail="Failed to update student",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    return HTTPResponse(
        detail=result,
        status_code=status.HTTP_200_OK
    )

@students_router.post('/')
async def create_handler(
    name: str = Form(...),
    email: str = Form(...),
    gender: str = Form(...),
    contact: str = Form(...),
    guardian_name: str = Form(...),
    guardian_relation: str = Form(...),
    guardian_mobile_number: str = Form(...),
    section_id: str = Form(...),
    is_enabled: bool = Form(...),
    photo1: UploadFile = File(None),
    photo2: UploadFile = File(None),
    photo3: UploadFile = File(None)
):
    temp_id = str(ObjectId())
    image_paths = students_service.process_student_images(temp_id, photo1, photo2, photo3)
    
    payload = {
        "name": name,
        "email": email,
        "gender": gender,
        "contact": contact,
        "guardian_name": guardian_name,
        "guardian_relation": guardian_relation,
        "guardian_mobile_number": guardian_mobile_number,
        "section_id": section_id,
        "is_enabled": is_enabled,
        "images": image_paths
    }
    
    result = students_service.create_data(payload, 'name')
    
    if result == ErrorTypes.ALREADY_EXISTS:
        return HTTPResponse(
            detail=result,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )
    
    if not result or not isinstance(result, dict):
        return HTTPResponse(
            detail="Failed to create student",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    actual_id = result.get('id')
    if actual_id:
        updated_image_paths = students_service.rename_student_images(temp_id, actual_id)
        if updated_image_paths:
            result["images"] = updated_image_paths
    
    return HTTPResponse(
        detail=result,
        status_code=status.HTTP_201_CREATED
    )