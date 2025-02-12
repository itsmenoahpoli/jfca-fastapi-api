import requests, urllib
from config.settings import app_settings

class SmsLibrary:
    __SENDER_NAME: str = app_settings.app_semaphore_sender_name
    __API_KEY : str = app_settings.app_semaphore_key
    __API_URL : str = app_settings.app_semaphore_url