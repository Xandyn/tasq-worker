# -*- coding: utf-8 -*-

# Stdlib imports
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Core Flask imports
from flask import Flask, request, Response

# Third-party app imports

# Imports from your apps


application = Flask(__name__)
application.config.from_object('settings')
application.debug = application.config['DEBUG']


@application.route('/', methods=['POST'])
def sqs_handler():
    """
        handle emails
    """
    message = request.get_json()

    if message is None:
        return Response('', status=415)

    if message.get('subject', None):
        s = smtplib.SMTP(
            application.config['MAIL_SERVER'],
            application.config['MAIL_PORT']
        )
        s.starttls()
        s.login(
            application.config['MAIL_USERNAME'],
            application.config['MAIL_PASSWORD']
        )

        msg = MIMEMultipart('alternative')
        msg['Subject'] = message.get("subject")
        msg['From'] = application.config['MAIL_DEFAULT_SENDER']
        msg['To'] = message.get("recipients")[0]
        part2 = MIMEText(message.get("html"), 'html')
        msg.attach(part2)

        try:
            s.sendmail(msg['From'], msg['To'], msg.as_string())
        except smtplib.SMTPException:
            return Response('Not send', status=403)

    return Response('Ok')


if __name__ == '__main__':
    application.run(host='0.0.0.0')
