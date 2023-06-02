_scriptname = 'ThirdParty.SparkPost'
from json import loads, dumps
from geventhttpclient import HTTPClient, URL

from Blueboard.ADO.Settings import SPARKPOST
from Blueboard.Utilities import *

def send(template, data, recipients):
	if not isList(recipients):
		recipients = [recipients]
		
	params = {
		"metadata": {},
		"options" : {
			"open_tracking" : True,
			"click_tracking" : True
		},
		"content" : {
			 "template_id" : template
		},
		"recipients" : [
			{
				"address" : {
					"email" : email
				}
			} for email in recipients
		],
		"substitution_data": data
	}	

	url = URL('https://api.sparkpost.com/api/v1/transmissions')
	print (_scriptname + '.send.params:', dumps(params, indent=5))

	params = dumps(params)
	print (_scriptname + '.send.url, params:', url, params
)
	http = HTTPClient.from_url(
		url, 
		connection_timeout=1000, 
		network_timeout=1000, 
		headers={
			"authorization" : SPARKPOST,
			"content-type" : "application/json"
		}
	)
	response = http.post(url.request_uri, params)
	http.close()
	content = response.read()
	status = loads(content)
	print (_scriptname + '.send.status:', status)
	return status
	
if __name__ == '__main__':

	print send(
		'raceday-manager-newuser', 
		{
			'server' : 'hyperdrive.me',
			"code" : 'CODE'
		}, 
		'jason@jasonwiener.com'
	)