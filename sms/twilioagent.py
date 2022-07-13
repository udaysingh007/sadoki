# Download the helper library from https://www.twilio.com/docs/python/install
import os
import logging
from twilio.rest import Client
from constants import const as cn

client = Client(cn.ACCOUNT_SID, cn.AUTH_TOKEN)

def sendsms (msgbody, to_number):
	message = client.messages.create(body=msgbody, from_=cn.FROM_NUMBER, to=to_number)
	logging.debug(message.sid)

# NOTE: imageuri needs to be a publicly accessible URL, without need for authentication.
# Hence the image needs to be posted to a cloud service
def sendmms(msgbody, imageuri, to_number):
	# need to convert the local imageuri into a publicly accessible URL (i.e., https) 
	# Post the image to something like google drive (or we might have to run a dedicated 
	# service on the Cloud
	httpsImageUrl = 'https://www.google.com/logos/google.jpg'
	
	# POST the imageuri onto the Cloud
	
	message = client.messages.create(body=msgbody, 
									from_=cn.FROM_NUMBER, 
									media_url=[imageuri],  # [httpsImageUrl]
									to=to_number)
	logging.debug(message.sid)
