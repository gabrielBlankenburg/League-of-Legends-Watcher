from .ApiException import ApiException

class ApiNotFoundException(ApiException):
	def __init__(self, *args, **kwargs):
		ApiException.__init__(self, *args, **kwargs)