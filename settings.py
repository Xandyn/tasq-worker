import os

DEBUG = False

# MAIL
MAIL_USERNAME = os.environ['MAIL_USERNAME']
MAIL_PASSWORD = os.environ['MAIL_PASSWORD']
MAIL_SERVER = 'email-smtp.us-west-2.amazonaws.com'
MAIL_PORT = 587
MAIL_DEFAULT_SENDER = 'arviqo@gmail.com'
