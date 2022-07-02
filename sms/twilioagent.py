# Download the helper library from https://www.twilio.com/docs/python/install
import os
import logging
from twilio.rest import Client

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = 'AC90500fd622ea00db67e19e8e44854c30'
auth_token = 'cb5c15ea61240b726acfdf148d3eb84f'
from_number = '+12513027736'

client = Client(account_sid, auth_token)

def sendsms (msgbody, to_number):
	message = client.messages.create(body=msgbody, from_=from_number, to=to_number)
	logging.debug(message.sid)
