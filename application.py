# -*- coding: utf-8 -*-

# Stdlib imports
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Core aiohttp imports
import asyncio

from aiohttp import web

# Third-party app imports

# Imports from your apps
from settings import *


@asyncio.coroutine
def sqs_handler(request):
    """
        handle emails
    """
    message = yield from request.json()

    if message is None:
        return web.Response(text='', status=415)

    if message.get('subject', None):
        s = smtplib.SMTP(MAIL_SERVER, MAIL_PORT)
        s.starttls()
        s.login(MAIL_USERNAME, MAIL_PASSWORD)

        msg = MIMEMultipart('alternative')
        msg['Subject'] = message.get("subject")
        msg['From'] = MAIL_DEFAULT_SENDER
        msg['To'] = message.get("recipients")[0]
        part2 = MIMEText(message.get("html"), 'html')
        msg.attach(part2)

        try:
            s.sendmail(msg['From'], msg['To'], msg.as_string())
        except smtplib.SMTPException:
            return web.Response(text='Not send', status=403)

    return web.Response(text='Ok')


@asyncio.coroutine
def index(request):
    return web.Response(text='Ok')


def init():
    loop = asyncio.get_event_loop()
    app = web.Application(loop=loop)
    app.router.add_get('/', index)
    app.router.add_post('/', sqs_handler)
    return app


application = init()


if __name__ == '__main__':
    web.run_app(application)
