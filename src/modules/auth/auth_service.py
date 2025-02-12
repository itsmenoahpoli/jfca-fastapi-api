import time
import jwt
from src.config.settings import app_settings

class AuthService:
	__JWT_SECRET_KEY = app_settings.app_api_key

	@classmethod
	def authenticate_credentials(self):
		auth_encode = {
			"user": {
				"name": "johndoe"
			},
			"expires": time.time() + 5 * 3600
		}
		token = jwt.encode(auth_encode, self.__JWT_SECRET_KEY, algorithm="HS256")

		return {
			"user": auth_encode["user"],
			"token": token
		}