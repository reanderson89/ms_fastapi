import random

from _settings import TWILIO

from twilio.rest import Client
TwilioClient = Client(*TWILIO)

from Token import addTokenLookup
from Utilities import SHA224Hash


def sendCode(verb, path, args):
	print ('v1.SMS.sendCode -> verb, path, args', verb, path, args)
	celNumber = args['cel'].strip()

	code = "%04d" % random.randint(0,9999)

	message = TwilioClient.messages.create(
		to='+1'+celNumber, 
		from_="+12125551212",
		body='Your verification code is: '+ code+'. Enter it in the app to finish logging in.'
	)

	token = SHA224Hash('sms')
	addTokenLookup(token, 'sms', celNumber)

	return {
		'status' : 'success',
		'sid' : message.sid,
		'code' : code,
		'token' : token
	}