import sys, urllib, requests
from src.config.settings import app_settings

class NotificationsService:
	__SEMAPHORE_API_KEY = app_settings.app_semaphore_api_key
	__SEMAPHORE_URL = app_settings.app_semaphore_url
	__SEMAPHORE_SENDER_NAME = app_settings.app_semaphore_sender_name

	