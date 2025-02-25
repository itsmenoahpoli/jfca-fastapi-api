from fastapi import APIRouter, status
from .students_service import students_service
from .students_dto import StudentDTO
from src.utils.http_utils import HTTPResponse
from src.constants.errors_constant import ErrorTypes

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
async def get_single_handler(id):
	result = students_service.get_single_data(id)
	
	return HTTPResponse(
		detail=result,
		status_code=status.HTTP_200_OK
	)

@students_router.delete('/{id}')
async def delete_one_handler(id):
	result = students_service.delete_data(id)
	
	return HTTPResponse(
		detail=result,
		status_code=status.HTTP_200_OK
	)

@students_router.patch('/{id}')
async def create_list_handler(payload: StudentDTO, id):
	result = students_service.update_data(id, payload.model_dump())

	if result == ErrorTypes.ALREADY_EXISTS:
		return HTTPResponse(
			detail=result,
			status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
		)
	
	return HTTPResponse(
		detail=result,
		status_code=status.HTTP_201_CREATED
	)

@students_router.post('/')
async def create_list_handler(payload: StudentDTO):
	result = students_service.create_data(payload.model_dump(), 'name')

	if result == ErrorTypes.ALREADY_EXISTS:
		return HTTPResponse(
			detail=result,
			status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
		)
	
	return HTTPResponse(
		detail=result,
		status_code=status.HTTP_201_CREATED
	)