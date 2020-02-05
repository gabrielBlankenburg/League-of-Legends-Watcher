from .ApiException import ApiException

class ApiInvalidValueException(ApiException):
	def __init__(self, *args, **kwargs):
		ApiException.__init__(self, *args, **kwargs)