from lol_request.exceptions import ApiInvalidValueException, ApiNotFoundException, ApiBadRequestException, ApiUnauthorizedException, ApiForbiddenException, ApiRateLimitExceededException

class LolApi:
	def __init__(self, base_url, lol_key, requests):
		"""Recieves the lol api url and the token for making requests

		Parameters
		----------
		base_url : str
		lol_key : str
		requests : requests
			Python default requests library
		"""
		self._base_url = base_url
		self._lol_key = lol_key
		self._requests = requests
	
	def _handle_get_request(self, url, on_success):
		"""Handle the get requests of the api

		Parameters
		----------
		url : str
			The league of legends endpoint
		on_success : function
			The callback function when the request is successful.
			This callback handles the response of the api

		Returns
		-------
		function
			A callback function passing the api response
		"""
		r = self._requests.get(url)

		print('status code {} for the url {}'.format(r.status_code, url))

		if (r.status_code == 200):
			return on_success(r)
		elif (r.status_code == 400):
			raise ApiBadRequestException(r.json())
		elif (r.status_code == 401):
			raise ApiUnauthorizedException(r.json())
		elif (r.status_code == 403):
			raise ApiForbiddenException(r.json())
		elif (r.status_code == 404):
			raise ApiNotFoundException(r.json())
		elif (r.status_code == 429):
			raise ApiRateLimitExceededException(r.json())

	def _get_request_returning_json(self, url):
		"""
		Parameters
		----------
		url : str
		
		Returns
		-------
		dict
			The response of the request json as a dict
		"""
		def on_success(r):
			return r.json()

		return self._handle_get_request(url, on_success)

	def search_summoner_by_nick(self, nick):
		"""Get basic info about a player with his nickname

		Parameters
		----------
		nick : str

		Returns
		-------
		dict
		"""

		if nick == '':
			raise ApiInvalidValueException('Nick cannot be empty')

		url = "{}/summoner/v4/summoners/by-name/{}?api_key={}".format(self._base_url, nick, self._lol_key)

		return self._get_request_returning_json(url)

	def search_league_by_summoner_id(self, lol_id):
		"""Get ranked infos about a player with his league of legends id

		Parameters
		----------
		lol_id : str

		Returns
		-------
		dict
		"""
		url = '{}/league/v4/entries/by-summoner/{}?api_key={}'.format(self._base_url, lol_id, self._lol_key)

		return self._get_request_returning_json(url)

	def search_matches_by_account_id(self, account_id, begin_index=0, end_index=100):
		"""Get matches by the account id

		Parameters
		----------
		account_id : str
		begin_index : int, optional
			The default is 0 
		end_index : int, optional
			The default is 100

		Returns
		-------
		dict
		"""
		if type(begin_index) is not int or type(end_index) is not int:
			raise ApiInvalidValueException('begin_index and end_index must be integer')
		elif begin_index < 0 or end_index < 0:
			raise ApiInvalidValueException('begin_index and end_index must be higher than 0')

		url = '{}/match/v4/matchlists/by-account/{}?beginIndex={}&endIndex={}&api_key={}'.format(self._base_url, account_id, begin_index, end_index, self._lol_key)

		return self._get_request_returning_json(url)

	def search_matches_by_match_id(self, game_id):
		"""Get matches by game id

		Parameters
		----------
		game_id : int

		Returns 
		-------
		dict
		"""
		url = '{}/match/v4/matches/{}?api_key={}'.format(self._base_url, game_id, self._lol_key)

		return self._get_request_returning_json(url)

