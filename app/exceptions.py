from fastapi import HTTPException


class ExceptionHandling():

	@staticmethod
	async def check404(item):
		if not item:
			raise HTTPException(status_code=404, detail="Not Found")

	@staticmethod
	async def custom500(message):
		raise HTTPException(status_code=500, detail=message)

	@staticmethod
	async def custom405(message):
		raise HTTPException(status_code=405, detail=message)
