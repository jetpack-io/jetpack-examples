import asyncio
from random import randint
from jetpack import jetroutine
from time import time


class EmailMessage(object):
    def __init__(self, email, subject, body):
        self.email = email
        self.subject = subject
        self.body = body

class EmailResult(object):
    def __init__(self, email, success, duration):
        self.email = email
        self.success = success
        self.duration = duration


# simulate building and sending an email
@jetroutine # <-- Turns the call into a Kubernetes job
async def send_brochure(email: str) -> EmailResult:


    start = time()

    message = await build_email(email)
    await send_email(message)

    end = time()
    duration = round((end - start) * 1000, 2)
    return EmailResult(email, success=True, duration=duration)


async def build_email(email: str) -> EmailMessage:

    # TODO: build email from template
    await asyncio.sleep(.1)
    
    if randint(0, 10) <= 3:
        await asyncio.sleep(.3) # Take too long 30% of the time

    message = EmailMessage(email, subject="email", body="body")
    return message


async def send_email(message: EmailMessage):

    # TODO: contact the SMTP server
    await asyncio.sleep(.2)

    if randint(0, 10) <= 3:
        await asyncio.sleep(.7) # Take too long 30% of the time

    if randint(0, 10) <= 2:
        raise Exception("Failed to send email to "+message.email)
