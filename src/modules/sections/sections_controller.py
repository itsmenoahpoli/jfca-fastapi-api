from fastapi import APIRouter, status
from .sections_service import sections_service
from .sections_dto import SectionDTO
from src.utils.http_utils import HTTPResponse
from src.constants.errors_constant import ErrorTypes

sections_router = APIRouter(
	prefix="/sections",
	tags=["Sections (Student Classes)"]
)

@sections_router.get('/')
async def get_list_handler():
	result = sections_service.get_list_data()
	
	return HTTPResponse(
		detail=result,
		status_code=status.HTTP_200_OK
	)

@sections_router.get('/{id}')
async def get_single_handler(id):
	result = sections_service.get_single_data(id)
	
	return HTTPResponse(
		detail=result,
		status_code=status.HTTP_200_OK
	)

@sections_router.delete('/{id}')
async def delete_one_handler(id):
	result = sections_service.delete_data(id)
	
	return HTTPResponse(
		detail=result,
		status_code=status.HTTP_200_OK
	)

@sections_router.patch('/{id}')
async def create_list_handler(payload: SectionDTO, id):
	result = sections_service.update_data(id, payload.model_dump())

	if result == ErrorTypes.ALREADY_EXISTS:
		return HTTPResponse(
			detail=result,
			status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
		)
	
	return HTTPResponse(
		detail=result,
		status_code=status.HTTP_201_CREATED
	)

@sections_router.post('/')
async def create_list_handler(payload: SectionDTO):
	result = sections_service.create_data(payload.model_dump(), 'name')

	if result == ErrorTypes.ALREADY_EXISTS:
		return HTTPResponse(
			detail=result,
			status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
		)
	
	return HTTPResponse(
		detail=result,
		status_code=status.HTTP_201_CREATED
	)