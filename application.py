# -*- coding: utf-8 -*-
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import asyncio

from aiohttp import web

from settings import *


async def email_handler(request):
    """
        handle emails
    """
    message = await request.json()

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


async def index(request):
    return web.Response(text='Ok')


def init():
    loop = asyncio.get_event_loop()
    application = web.Application(loop=loop)
    application.router.add_get('/', index)
    application.router.add_post('/email', email_handler)
    return application


app = init()


if __name__ == '__main__':
    web.run_app(app)
