from .ApiException import ApiException

class ApiRateLimitExceededException(ApiException):
	def __init__(self, *args, **kwargs):
		ApiException.__init__(self, *args, **kwargs)