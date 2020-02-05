from django.test import TestCase
from unittest.mock import MagicMock
#from lol_request.dependency_injector.dependencies import di
from lol_request.dependency_injector.ServiceInjector import di
from lol_request.services.LolApi import LolApi
from lol_request.exceptions import ApiInvalidValueException, ApiNotFoundException, ApiBadRequestException, ApiUnauthorizedException, ApiForbiddenException, ApiRateLimitExceededException

class LolApiTests(TestCase):
	def test_search_summoner_by_existing_nick(self):
		url = 'https://br1.api.riotgames.com/lol'
		lol_key = '123'
		nick = 'test'

		requests_mock = MagicMock()
		response_mock = MagicMock()
		response_mock.status_code = 200
		response_mock.json = MagicMock(return_value={
			'summonerName': 'test'
		})
		requests_mock.get = MagicMock(return_value=response_mock)
		di.register('requests')(requests_mock)

		lol_api = LolApi(url, lol_key)

		response = {
			'summonerName': 'test'
		}
		self.assertEqual(lol_api.search_summoner_by_nick(nick), response)
		requests_mock.get.assert_called_with('{}/summoner/v4/summoners/by-name/{}?api_key={}'.format(url, nick, lol_key))
		response_mock.json.assert_called_with()

	def test_search_summoner_by_empty_nick(self):
		url = 'https://br1.api.riotgames.com/lol'
		lol_key = '123'
		nick = ''

		requests_mock = MagicMock()
		di.register('requests')(requests_mock)

		lol_api = LolApi(url, lol_key)

		self.assertRaises(ApiInvalidValueException, lol_api.search_summoner_by_nick, nick)

	def test_search_summoner_by_unexisting_nick(self):
		url = 'https://br1.api.riotgames.com/lol'
		lol_key = '123'
		nick = 'unexisting user'

		requests_mock = MagicMock()
		response_mock = MagicMock()
		response_mock.status_code = 404

		requests_mock.get = MagicMock(return_value=response_mock)
		di.register('requests')(requests_mock)

		lol_api = LolApi(url, lol_key)
		self.assertRaises(ApiNotFoundException, lol_api.search_summoner_by_nick, nick)
		requests_mock.get.assert_called_with('{}/summoner/v4/summoners/by-name/{}?api_key={}'.format(url, nick, lol_key))

	def test_search_summmoner_by_nick_bad_request(self):
		url = 'https://br1.api.riotgames.com/lol'
		lol_key = '123'
		nick = 'test'

		requests_mock = MagicMock()
		response_mock = MagicMock()
		response_mock.status_code = 400

		requests_mock.get = MagicMock(return_value=response_mock)
		di.register('requests')(requests_mock)

		lol_api = LolApi(url, lol_key)
		self.assertRaises(ApiBadRequestException, lol_api.search_summoner_by_nick, nick)
		requests_mock.get.assert_called_with('{}/summoner/v4/summoners/by-name/{}?api_key={}'.format(url, nick, lol_key))

	def test_search_summoner_by_nick_unauthorized(self):
		url = 'https://br1.api.riotgames.com/lol'
		lol_key = 'some unauthorized key'
		nick = 'test'

		requests_mock = MagicMock()
		response_mock = MagicMock()
		response_mock.status_code = 401

		requests_mock.get = MagicMock(return_value=response_mock)
		di.register('requests')(requests_mock)

		lol_api = LolApi(url, lol_key)
		self.assertRaises(ApiUnauthorizedException, lol_api.search_summoner_by_nick, nick)
		requests_mock.get.assert_called_with('{}/summoner/v4/summoners/by-name/{}?api_key={}'.format(url, nick, lol_key))

	def test_search_summoner_by_nick_forbidden(self):
		url = 'https://br1.api.riotgames.com/lol'
		lol_key = 'some forbidden key'
		nick = 'test'

		requests_mock = MagicMock()
		response_mock = MagicMock()
		response_mock.status_code = 403

		requests_mock.get = MagicMock(return_value=response_mock)
		di.register('requests')(requests_mock)

		lol_api = LolApi(url, lol_key)
		self.assertRaises(ApiForbiddenException, lol_api.search_summoner_by_nick, nick)
		requests_mock.get.assert_called_with('{}/summoner/v4/summoners/by-name/{}?api_key={}'.format(url, nick, lol_key))

	def test_search_summoner_by_nick_rate_limit_exceeded(self):
		url = 'https://br1.api.riotgames.com/lol'
		lol_key = '123'
		nick = 'test'

		requests_mock = MagicMock()
		response_mock = MagicMock()
		response_mock.status_code = 429

		requests_mock.get = MagicMock(return_value=response_mock)
		di.register('requests')(requests_mock)

		lol_api = LolApi(url, lol_key)
		self.assertRaises(ApiRateLimitExceededException, lol_api.search_summoner_by_nick, nick)
		requests_mock.get.assert_called_with('{}/summoner/v4/summoners/by-name/{}?api_key={}'.format(url, nick, lol_key))

	def test_search_league_by_valid_existing_summoner_id(self):
		url = 'https://br1.api.riotgames.com/lol'
		lol_key = '123'
		summoner_id = '112233'

		requests_mock = MagicMock()
		response_mock = MagicMock()
		response_mock.status_code = 200
		response_mock.json = MagicMock(return_value={
			'summonerId': summoner_id
		})
		requests_mock.get = MagicMock(return_value=response_mock)
		di.register('requests')(requests_mock)

		lol_api = LolApi(url, lol_key)

		response = {
			'summonerId': summoner_id
		}
		self.assertEqual(lol_api.search_league_by_summoner_id(summoner_id), response)
		requests_mock.get.assert_called_with('{}/league/v4/entries/by-summoner/{}?api_key={}'.format(url, summoner_id, lol_key))
		response_mock.json.assert_called_with()

	def test_search_matches_by_account_id(self):
		url = 'https://br1.api.riotgames.com/lol'
		lol_key = '123'
		account_id = '112233'
		begin_index = 0
		end_index = 10

		requests_mock = MagicMock()
		response_mock = MagicMock()
		response_mock.status_code = 200
		response_mock.json = MagicMock(return_value=[
			{
				'gameID': 123
			}
		])
		requests_mock.get = MagicMock(return_value=response_mock)
		di.register('requests')(requests_mock)

		lol_api = LolApi(url, lol_key)

		response = [
			{
				'gameID': 123
			}
		]
		self.assertEqual(lol_api.search_matches_by_account_id(account_id, begin_index, end_index), response)
		requests_mock.get.assert_called_with('{}/match/v4/matchlists/by-account/{}?beginIndex={}&endIndex={}&api_key={}'.format(url, account_id, begin_index, end_index, lol_key))
		response_mock.json.assert_called_with()

	def test_search_matches_by_account_id_str_begin_index(self):
		url = 'https://br1.api.riotgames.com/lol'
		lol_key = '123'
		account_id = '112233'
		begin_index = 'test'
		end_index = 10

		requests_mock = MagicMock()
		di.register('requests')(requests_mock)

		lol_api = LolApi(url, lol_key)

		self.assertRaises(ApiInvalidValueException, lol_api.search_matches_by_account_id, account_id, begin_index, end_index)

	def test_search_matches_by_account_id_str_end_index(self):
		url = 'https://br1.api.riotgames.com/lol'
		lol_key = '123'
		account_id = '112233'
		begin_index = 0
		end_index = 'test'

		requests_mock = MagicMock()
		di.register('requests')(requests_mock)

		lol_api = LolApi(url, lol_key)

		self.assertRaises(ApiInvalidValueException, lol_api.search_matches_by_account_id, account_id, begin_index, end_index)

	def test_search_matches_by_account_id_lower_than_zero_begin_index(self):
		url = 'https://br1.api.riotgames.com/lol'
		lol_key = '123'
		account_id = '112233'
		begin_index = -3
		end_index = 10

		requests_mock = MagicMock()
		di.register('requests')(requests_mock)

		lol_api = LolApi(url, lol_key)

		self.assertRaises(ApiInvalidValueException, lol_api.search_matches_by_account_id, account_id, begin_index, end_index)

	def test_search_matches_by_account_id_lower_than_zero_end_index(self):
		url = 'https://br1.api.riotgames.com/lol'
		lol_key = '123'
		account_id = '112233'
		begin_index = 3
		end_index = -9

		requests_mock = MagicMock()
		di.register('requests')(requests_mock)

		lol_api = LolApi(url, lol_key)

		self.assertRaises(ApiInvalidValueException, lol_api.search_matches_by_account_id, account_id, begin_index, end_index)

	def test_search_matches_by_match_id(self):
		url = 'https://br1.api.riotgames.com/lol'
		lol_key = '123'
		game_id = 123123

		requests_mock = MagicMock()
		response_mock = MagicMock()
		response_mock.status_code = 200
		response_mock.json = MagicMock(return_value={
			'game_id': game_id
		})
		requests_mock.get = MagicMock(return_value=response_mock)
		di.register('requests')(requests_mock)

		lol_api = LolApi(url, lol_key)

		response = {
			'game_id': game_id
		}
		self.assertEqual(lol_api.search_matches_by_match_id(game_id), response)
		requests_mock.get.assert_called_with('{}/match/v4/matches/{}?api_key={}'.format(url, game_id, lol_key))
		response_mock.json.assert_called_with()
