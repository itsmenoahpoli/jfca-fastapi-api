import urllib.parse, requests, smtplib
from fastapi import HTTPException, status
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.config.settings import app_settings
from src.utils.logging_utils import sms_logger, mail_logger
from src.constants.mail_constant import MailDefauls

class NotificationsService:
	__SEMAPHORE_API_KEY = app_settings.app_semaphore_key
	__SEMAPHORE_URL = app_settings.app_semaphore_url
	__SEMAPHORE_SENDER_NAME = app_settings.app_semaphore_sender_name
	__MAIL_USERNAME = app_settings.app_mail_username
	__MAIL_PASSWORD = app_settings.app_mail_password
	__MAIL_HOST = app_settings.app_mail_host
	__MAIL_PORT = app_settings.app_mail_port
	__MAIL_FROM = app_settings.app_mail_from


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
			
			sms_logger.info(response.text)
			print(f"Response: {response.text}")

			response.raise_for_status()
			return True
		except requests.exceptions.RequestException as e:
			print(f"Request failed: {e}")
			return None
		except Exception as e:
			print(f"An error occurred: {e}")
			return None
			

	def send_email(self, recipient, subject = MailDefauls.DEFAULT_SUBJECT, message = ""):
		try:
			mail = MIMEMultipart()
			mail['From'] = self.__MAIL_FROM
			mail['To'] = recipient
			mail['Subject'] = subject

			mail.attach(MIMEText(message, 'html'))

			mail_server = smtplib.SMTP(self.__MAIL_HOST, self.__MAIL_PORT)
			mail_server.starttls()
			mail_server.login(self.__MAIL_USERNAME, self.__MAIL_PASSWORD)

			mail_server.send_message(mail)
			mail_server.quit()
			mail_logger.info(f"Mail:{subject} sent to {recipient}")

			return True
		except Exception as e:
			print(f"An error occurred: {e}")
			return None



notifications_service = NotificationsService()