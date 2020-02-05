from .ApiException import ApiException

class ApiBadRequestException(ApiException):
	def __init__(self, *args, **kwargs):
		ApiException.__init__(self, *args, **kwargs)