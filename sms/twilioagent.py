# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = 'AC90500fd622ea00db67e19e8e44854c30'
auth_token = 'cb5c15ea61240b726acfdf148d3eb84f'

client = Client(account_sid, auth_token)

message = client.messages \
    .create(
         body='Message alert from your Sadoki car lifeguard',
         from_='+12513027736',
         to='+19175824874'
     )

print(message.sid)
