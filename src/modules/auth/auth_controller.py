from fastapi import APIRouter, status
from .auth_dto import SigninDTO
from .auth_service import auth_service
from src.utils.http_utils import HTTPResponse

auth_router = APIRouter(
  prefix="/auth",
  tags=["Auth API"]
)

@auth_router.post('/signin')
def signin_handler(payload: SigninDTO):
	result = auth_service.authenticate_credentials(payload.model_dump())

	if result is None:
		return HTTPResponse(
		status_code=status.HTTP_401_UNAUTHORIZED,
		detail="UNAUTHORIZED"
	)

	return HTTPResponse(
		status_code=status.HTTP_200_OK,
		detail=result
	)