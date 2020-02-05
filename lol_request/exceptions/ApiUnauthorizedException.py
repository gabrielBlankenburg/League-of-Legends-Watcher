from .ApiException import ApiException

class ApiUnauthorizedException(ApiException):
	def __init__(self, *args, **kwargs):
		ApiException.__init__(self, *args, **kwargs)