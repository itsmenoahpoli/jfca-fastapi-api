from fastapi import APIRouter, status
from .auth_dto import SigninDTO
from .auth_service import auth_service
from src.utils.http_utils import HTTPResponse

auth_router = APIRouter(
  prefix="/v1/api/auth",
  tags=["Auth API"]
)

@auth_router.post('/signin')
def signin_handler(payload: SigninDTO):
	result = auth_service.authenticate_credentials()

	return HTTPResponse(
		status_code=status.HTTP_200_OK,
		detail=result
	)