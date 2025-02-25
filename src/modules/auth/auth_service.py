import time
import jwt
from src.config.settings import app_settings
from src.modules.users.users_service import users_service

class AuthService:
	__JWT_SECRET_KEY = app_settings.app_api_key

	def authenticate_credentials(self, credentials):
		user = users_service.find_by_email(credentials['email'])

		if user is None or user['is_enabled'] is False:
			return 	None

		auth_encode = {
			"user": {
				"name": user['name']
			},
			"expires": time.time() + 5 * 3600
		}
		token = jwt.encode(auth_encode, self.__JWT_SECRET_KEY, algorithm="HS256")

		return {
			"user": auth_encode["user"],
			"token": token
		}
	
auth_service = AuthService()