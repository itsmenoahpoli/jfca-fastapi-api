import time
import jwt
from src.config.settings import app_settings
from src.modules.users.users_service import users_service
from src.utils.password_utils import verify_password

TOKEN_EXPIRATION_TIME = time.time() + 86400

class AuthService:
	__JWT_SECRET_KEY = app_settings.app_api_key

	def __check_user_credentials( credentials):
		user = users_service.find_by_email(credentials['email'])

		if user is None or user['is_enabled'] is False or not verify_password(credentials['password'], user['password']):
			return False
		
		return user

	def authenticate_credentials(self, credentials):
		check_user = self.__check_user_credentials(credentials)

		if check_user is False:
			return False

		auth_encode = {
			"user": {
				"name": check_user['name']
			},
			"expires": TOKEN_EXPIRATION_TIME
		}
		token = jwt.encode(auth_encode, self.__JWT_SECRET_KEY, algorithm="HS256")

		return {
			"user": auth_encode["user"],
			"token": token
		}
	
auth_service = AuthService()