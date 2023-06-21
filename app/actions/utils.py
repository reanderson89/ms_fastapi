from time import time
from app.utilities import PositiveNumbers


def new_9char():
	generator = PositiveNumbers.PositiveNumbers(size=9)
	uuid_time = int(str(time()).replace(".", "")[:16])
	char_9 = generator.encode(uuid_time)
	return char_9
