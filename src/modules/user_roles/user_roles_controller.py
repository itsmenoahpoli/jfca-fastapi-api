from fastapi import APIRouter, status
from .user_roles_service import user_roles_service
from .user_roles_dto import UserRoleDTO
from src.utils.http_utils import HTTPResponse
from src.constants.errors_constant import ErrorTypes

user_roles_router = APIRouter(
	prefix="/user-roles",
	tags=["User Roles"]
)

@user_roles_router.get('/')
async def get_list_handler():
	result = user_roles_service.get_list_data()
	
	return HTTPResponse(
		detail=result,
		status_code=status.HTTP_200_OK
	)

@user_roles_router.get('/{id}')
async def get_single_handler(id: str):
	result = user_roles_service.get_single_data(id)
	
	return HTTPResponse(
		detail=result,
		status_code=status.HTTP_200_OK
	)

@user_roles_router.delete('/{id}')
async def delete_one_handler(id: str):
	result = user_roles_service.delete_data(id)
	
	return HTTPResponse(
		detail=result,
		status_code=status.HTTP_200_OK
	)

@user_roles_router.post('/')
async def create_list_handler(payload: UserRoleDTO):
	result = user_roles_service.create_data(payload.model_dump(), 'name')

	if result == ErrorTypes.ALREADY_EXISTS:
		return HTTPResponse(
			detail=result,
			status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
		)
	
	return HTTPResponse(
		detail=result,
		status_code=status.HTTP_201_CREATED
	)