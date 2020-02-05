from .ApiException import ApiException

class ApiForbiddenException(ApiException):
	def __init__(self, *args, **kwargs):
		ApiException.__init__(self, *args, **kwargs)