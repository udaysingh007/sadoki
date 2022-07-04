# Download the helper library from https://www.twilio.com/docs/python/install
import os
import logging
from twilio.rest import Client
from constants import const as cn

client = Client(cn.ACCOUNT_SID, cn.AUTH_TOKEN)

def sendsms (msgbody, to_number):
	message = client.messages.create(body=msgbody, from_=cn.FROM_NUMBER, to=to_number)
	logging.debug(message.sid)

