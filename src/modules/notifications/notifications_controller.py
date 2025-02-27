from fastapi import APIRouter, status
from .notifications_service import notifications_service
from src.utils.http_utils import HTTPResponse
from src.constants.errors_constant import ErrorTypes

notifications_router = APIRouter(
	prefix="/notifications",
	tags=["Notifications"]
)

@notifications_router.post('/sms/test')
async def get_list_handler():
	result = notifications_service.send_sms('09620636535', 'Good day \n This is a test sms from JCFA Server \n Thank you!')
	
	return HTTPResponse(
		detail=result,
		status_code=status.HTTP_200_OK
	)
