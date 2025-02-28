from fastapi import APIRouter, status
from .notifications_service import notifications_service
from src.utils.http_utils import HTTPResponse
from src.constants.errors_constant import ErrorTypes

notifications_router = APIRouter(
	prefix="/notifications",
	tags=["Notifications"]
)

@notifications_router.post('/sms/test')
async def test_send_sms_handler():
	result = notifications_service.send_sms('09620636535', 'Good day \n This is a test sms from JCFA Server \n Thank you!')
	
	if result is None:
		return HTTPResponse(
			detail=ErrorTypes.SMS_SENDING_FAILED,
			status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
		)

	return HTTPResponse(
		detail="SMS_SENT",
		status_code=status.HTTP_200_OK
	)


@notifications_router.post('/mail/test')
async def test_send_mail_handler():
	result = notifications_service.send_email('user@domain.com', 'Test Mail', 'This is a test mail from JCFA Server')
	
	if result is None:
		return HTTPResponse(
			detail=ErrorTypes.MAIL_SENDING_FAILED,
			status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
		)
	
	return HTTPResponse(
		detail="MAIL_SENT",
		status_code=status.HTTP_200_OK
	)