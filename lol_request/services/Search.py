from lol_request.dependency_injector.dependencies import di


class Search:
	@di.inject
	def __init__(self, _deps):
		self._lol_api = _deps.get_new_object('LolApi')
		self._converter = _deps.get_new_object('ApiToModelConverter')
		self._formatter = _deps.get_new_object('ResponseFormatter')

	def _search_league_by_summoner_id(self, summoner):
		"""Get player rank infos and converts it into a lol_request.models.Summoner object.

		Parameters
		----------
		summoner : lol_request.models.Summoner

		Returns
		------
		lol_request.models.Summoner
		"""
		response = self._lol_api.search_league_by_summoner_id(summoner.lol_id)
		summoner = self._converter.summoner_by_id(summoner, response)
		return summoner

	def _search_matches_by_account_id(self, account_id):
		"""Get a list of games using the league of legends account id.

		Parameters
		----------
		account_id : int

		Returns
		-------
		list
			This is a list of games ids
		"""
		response = self._lol_api.search_matches_by_account_id(account_id, end_index=3)

		games_ids = []

		for i in response['matches']:
			games_ids.append(i['gameId'])

		return games_ids

	def _set_teams_players(self, games_list, responses):
		"""Creates a dict with teams and their players.
		
		Parameters
		----------
		games_list : list
			A list of lol_request.models.Game object
		responses : list
			A list of dict containing infos about the games of the games_list

		Returns
		-------
		dict
			Format of dict returned:
			{
				<Game ID>: {
					'team_one': [
						<lol_request.models.TeamPlayer>
					],
					'team_two': [
						<lol_request.models.TeamPLayer>
					]
				}
			}
		"""
		matches_teams_players = {}

		for i, match in enumerate(games_list):
			matches_teams_players[match.lol_game_id] = {
				'team_one': [], 
				'team_two': []
			}
			match_team_one = self._converter.match_team_by_game_id(match, 1, responses[i])
			match_team_two = self._converter.match_team_by_game_id(match, 2, responses[i])
			for j in range(1, 6):
				team_player = self._converter.team_player_by_game_id(match_team_one, j, responses[i])
				matches_teams_players[match.lol_game_id]['team_one'].append(team_player)
			for j in range(6, 11):
				team_player = self._converter.team_player_by_game_id(match_team_two, j, responses[i])
				matches_teams_players[match.lol_game_id]['team_two'].append(team_player)
		return matches_teams_players

	def get_match_list_by_nick(self, nick):
		"""Get a league of legends nickname and returns a list of games played by the nick.

		Parameters
		----------
		nick : str

		Returns
		-------
		list
			Formatted game info and list of dicts with games info.
		"""
		summoner = Summoner()

		response = self._lol_api.search_summoner_by_nick(nick)

		summoner = self._converter.summoner_from_nickname(summoner, response)

		summoner = self._search_league_by_summoner_id(summoner)

		games_ids = self._search_matches_by_account_id(summoner.account_id)
		
		games_list = []

		responses = []

		for game_id in games_ids:
			response = self._lol_api.search_matches_by_match_id(game_id)

			responses.append(response)

			games_list.append(self._converter.match_by_id(response))


		matches_teams_players = self._set_teams_players(games_list, responses)

		return self._formatter.format_player_games_list_response(summoner,matches_teams_players)

