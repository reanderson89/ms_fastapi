from time import time
from collections import namedtuple
import logging

import pycountry
from geopy.geocoders import Nominatim

from app.utilities import PositiveNumbers


def new_9char():
	"""Generate a new 9-character string.

	:returns: str: 9-character string
	"""
	generator = PositiveNumbers.PositiveNumbers(size=9)
	uuid_time = int(str(time()).replace(".", "")[:16])
	char_9 = generator.encode(uuid_time)
	return char_9


def convert_coordinates(value):
	"""Convert coordinates to/from microdegrees.

	:param: value (float or int):
		Value to convert

	:returns: float or int: Converted value
	"""
	if isinstance(value, float):
		return int(value * 10**6)
	elif isinstance(value, int):
		return value / 10**6
	else:
		return value

STATE_ABBREVIATIONS = {
	'AL': 'Alabama',
	'AK': 'Alaska',
	'AZ': 'Arizona',
	'AR': 'Arkansas',
	'CA': 'California',
	'CO': 'Colorado',
	'CT': 'Connecticut',
	'DE': 'Delaware',
	'FL': 'Florida',
	'GA': 'Georgia',
	'HI': 'Hawaii',
	'ID': 'Idaho',
	'IL': 'Illinois',
	'IN': 'Indiana',
	'IA': 'Iowa',
	'KS': 'Kansas',
	'KY': 'Kentucky',
	'LA': 'Louisiana',
	'ME': 'Maine',
	'MD': 'Maryland',
	'MA': 'Massachusetts',
	'MI': 'Michigan',
	'MN': 'Minnesota',
	'MS': 'Mississippi',
	'MO': 'Missouri',
	'MT': 'Montana',
	'NE': 'Nebraska',
	'NV': 'Nevada',
	'NH': 'New Hampshire',
	'NJ': 'New Jersey',
	'NM': 'New Mexico',
	'NY': 'New York',
	'NC': 'North Carolina',
	'ND': 'North Dakota',
	'OH': 'Ohio',
	'OK': 'Oklahoma',
	'OR': 'Oregon',
	'PA': 'Pennsylvania',
	'RI': 'Rhode Island',
	'SC': 'South Carolina',
	'SD': 'South Dakota',
	'TN': 'Tennessee',
	'TX': 'Texas',
	'UT': 'Utah',
	'VT': 'Vermont',
	'VA': 'Virginia',
	'WA': 'Washington',
	'WV': 'West Virginia',
	'WI': 'Wisconsin',
	'WY': 'Wyoming'
}


def parse_input_param(input_param):
	"""Parse input parameter into a dictionary of location parts.

	:param: input_param (str):
		Input parameter should be in the format "city, state, country", "city, country" or "city"

	:returns: dict: Dictionary of location parts
	"""

	location_parts = input_param.split(", ")
	city = location_parts[0]
	state_code = None
	country_name = None
	if len(location_parts) > 1:
		state_or_country = location_parts[1]
		state_code = STATE_ABBREVIATIONS.get(state_or_country)
		if state_code is None:
			try:
				# Try to convert state/country to state/country code using pycountry
				country = pycountry.countries.search_fuzzy(state_or_country)[0]
				country_name = country.name
				country_code = country.alpha_2
				subdivisions = pycountry.subdivisions.get(country_code=country_code)
				for subdivision in subdivisions:
					if subdivision.name == state_or_country or subdivision.code == state_or_country or subdivision.code.lower() == state_or_country.lower():
						state_code = subdivision.code.split("-")[-1]
						break
			except LookupError:
				# State/country is not a subdivision of a country
				pass
	if state_code is not None:
		return {"city": city, "state": state_code}
	elif country_name is not None:
		return {"city": city, "country": country_name}
	return {"city": city}


def query_location(input_param):
	from geopy.exc import GeocoderServiceError

	geolocator = Nominatim(user_agent="milestone_app")

	MAX_RETRIES = 4
	for retries in range(MAX_RETRIES):
		try:
			location = geolocator.geocode(input_param, timeout=5)
			if location is not None:
				return location
		except GeocoderServiceError as e:
			if "502" in e.args[0]:
				logging.warning("Geocoding failed due to 502 error. Retrying...")
			else:
				logging.error("Geocoding failed with error: %s", e)
	# handle case where all retries failed
	logging.error("Geocoding failed after %d retries", MAX_RETRIES)
	return None


def get_location_data(location_string):
	"""
	Get location data from a string using geopy and Nominatim.

	:param str location_string: Location string to get data for

	:returns: Location: namedtuple with latitude and longitude
	"""
	Location = namedtuple("Location", ["latitude", "longitude", "location"])

	query_dict = parse_input_param(location_string)
	location = query_location(query_dict)

	return Location(
			location.latitude, location.longitude, location
		) if location else Location(None, None, None)
