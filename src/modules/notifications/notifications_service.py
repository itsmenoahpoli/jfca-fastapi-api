import urllib.parse, requests
from src.config.settings import app_settings
from src.utils.logging_utils.sms import sms_logging

class NotificationsService:
    __SEMAPHORE_API_KEY = app_settings.app_semaphore_key
    __SEMAPHORE_URL = app_settings.app_semaphore_url
    __SEMAPHORE_SENDER_NAME = app_settings.app_semaphore_sender_name

    def send_sms(self, recipient, message):
        try:
            params = (
                ('apikey', self.__SEMAPHORE_API_KEY),
                ('sendername', self.__SEMAPHORE_SENDER_NAME),
                ('message', message),
                ('number', recipient)
            )

            url = self.__SEMAPHORE_URL + urllib.parse.urlencode(params)
            response = requests.post(url)
            
            sms_logging.info(response.text)
            print(f"Response: {response.text}")

            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")


notifications_service = NotificationsService()