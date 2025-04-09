import logging

# SMS Logger
sms_handler = logging.FileHandler('logs/sms.txt')
sms_logger = logging.getLogger('sms_logger')
sms_logger.setLevel(logging.INFO)
sms_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
sms_handler.setFormatter(sms_formatter)
sms_logger.addHandler(sms_handler)

# Mail Logger  
mail_handler = logging.FileHandler('logs/mail.txt')
mail_logger = logging.getLogger('mail_logger')
mail_logger.setLevel(logging.INFO)
mail_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
mail_handler.setFormatter(mail_formatter)
mail_logger.addHandler(mail_handler)