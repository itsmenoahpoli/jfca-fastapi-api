from fastapi import APIRouter, status
from .users_service import users_service
from .users_dto import UserCreateDTO, UserUpdateDTO, UserResponseDTO
from src.utils.http_utils import HTTPResponse
from src.constants.errors_constant import ErrorTypes

users_router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@users_router.get('/', response_model=list[UserResponseDTO])
async def get_list_handler():
    result = users_service.get_list_data()
    
    return HTTPResponse(
        detail=result,
        status_code=status.HTTP_200_OK
    )

@users_router.get('/{id}', response_model=UserResponseDTO)
async def get_single_handler(id: str):
    result = users_service.get_single_data(id)
    
    if result == ErrorTypes.NOT_FOUND_ERROR:
        return HTTPResponse(
            detail=result,
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    return HTTPResponse(
        detail=result,
        status_code=status.HTTP_200_OK
    )

@users_router.post('/', response_model=UserResponseDTO)
async def create_handler(payload: UserCreateDTO):
    result = users_service.create_data(payload.model_dump())

    if result == ErrorTypes.ALREADY_EXISTS:
        return HTTPResponse(
            detail=result,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )
    
    return HTTPResponse(
        detail=result,
        status_code=status.HTTP_201_CREATED
    )

@users_router.put('/{id}', response_model=UserResponseDTO)
async def update_handler(id: str, payload: UserUpdateDTO):
    result = users_service.update_data(id, payload.model_dump())
    
    if result == ErrorTypes.NOT_FOUND_ERROR:
        return HTTPResponse(
            detail=result,
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    if result is None:
        return HTTPResponse(
            detail=ErrorTypes.UPDATE_FAILED,
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    return HTTPResponse(
        detail=result,
        status_code=status.HTTP_200_OK
    )

@users_router.delete('/{id}')
async def delete_handler(id: str):
    result = users_service.delete_data(id)
    
    if result == ErrorTypes.NOT_FOUND_ERROR:
        return HTTPResponse(
            detail=result,
            status_code=status.HTTP_404_NOT_FOUND
        )
    
    return HTTPResponse(
        detail=result,
        status_code=status.HTTP_200_OK
    ) 