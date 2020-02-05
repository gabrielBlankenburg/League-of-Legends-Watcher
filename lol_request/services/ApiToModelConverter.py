from lol_request.dependency_injector.dependencies import di

class ApiToModelConverter:
	@di.inject
	def __init__(self, _deps):
		self._deps = _deps

	def summoner_from_nickname(self, summoner, response):
		"""Converts the response of the endpoint /summoner/v4/summoners/by-name/{summonerName} into a lol_request.models.Summoner object

		Parameters
		----------
		summoner : lol_request.models.Summoner
		response : dict

		Returns
		-------
		lol_request.models.Summoner
		"""
		summoner.lol_id = response['id']
		summoner.name = response['name']
		summoner.icon_id = response['profileIconId']
		summoner.puuid = response['puuid']
		summoner.account_id = response['accountId']
		summoner.level = response['summonerLevel']
		return summoner

	def summoner_by_id(self, summoner, response):
		"""Converts the response of the endpoint /league/v4/entries/by-summoner into a lol_request.models.Summoner object

		Parameters
		----------
		summoner : lol_request.models.Summoner
		response : dict

		Returns
		-------
		lol_request.models.Summoner
		"""
		if response == []:
			return summoner

		for i in response:
			if i['queueType'] == 'RANKED_SOLO_5x5':
				summoner.tier_solo = i['tier']
				summoner.rank_solo = i['rank']
				summoner.points_solo = i['leaguePoints']
			else:
				summoner.tier_flex = i['tier']
				summoner.rank_flex = i['rank']
				summoner.points_flex = i['leaguePoints']\

		return summoner

	def match_by_id(self, response):
		"""Converts the response of the endpoint /match/v4/matches/ into a lol_request.models.Game object

		Parameters
		----------
		response : dict

		Returns
		-------
		lol_request.models.Game
		"""
		game = self._deps.get_new_object('Game')
		game.lol_game_id = response['gameId']
		game.duration = response['gameDuration']
		game.mode = response['gameMode']
		game.creation = response['gameCreation']
		game.lol_game_type = response['gameType']

		return game

	def match_team_by_game_id(self, game, side, response):
		"""Converts the response of the endpoint /match/v4/matches/ into a lol_request.models.Team object

		Parameters
		----------
		game : lol_request.models.Game
		side : int
			It is the team side. Must be either 1 or 2
		response : dict

		Returns
		-------
		lol_request.models.Team
		"""
		team = self._deps.get_new_object('Team')
		team.game = game
		team.side = side
		team.win = response['teams'][side - 1]['win'] == 'Win'

		return team

	def team_player_by_game_id(self, team, participant_number, response):
		"""Converts the response of the endpoint /match/v4/matches/ into a lol_request.models.TeamPlayer object

		Parameters
		----------
		team : lol_request.models.Team
		participant_number : int
			It is the position of the player in the response of the endpoint
		response : dict

		Returns
		-------
		lol_request.models.TeamPlayer 
		"""
		participant_team_number = participant_number if participant_number <=5 else participant_number - 5

		summoner = self._deps.get_new_object('Summoner')
		summoner.name = response['participantIdentities'][participant_number - 1]['player']['summonerName']
		summoner.account_id = response['participantIdentities'][participant_number - 1]['player']['accountId']
		summoner.lol_id = response['participantIdentities'][participant_number - 1]['player']['summonerId']

		int_champion_chosen = int(response['participants'][participant_number - 1]['championId'])

		champion_ban = None

		if response['teams'][team.side - 1]['bans'] != []:
			if int(response['teams'][team.side - 1]['bans'][participant_team_number - 1]['championId']) <= 0:
				pass
			else:
				int_champion_ban = int(response['teams'][team.side - 1]['bans'][participant_team_number - 1]['championId'])
				champion_ban = self._deps.get('Champion').objects.get(lol_key__exact=int_champion_ban)

		champion_chosen = self._deps.get('Champion').objects.get(lol_key__exact=int_champion_chosen)

		team_player = self._deps.get_new_object('TeamPlayer')
		team_player.team = team
		team_player.player = summoner
		team_player.champion_chosen = champion_chosen
		team_player.champion_ban = champion_ban
		team_player.participant_number = participant_number
		team_player.match_history_uri = response['participantIdentities'][participant_number - 1]['player']['matchHistoryUri']
		team_player.lane = response['participants'][participant_number - 1]['timeline']['lane']
		team_player.role = response['participants'][participant_number - 1]['timeline']['role']
		team_player.kills = response['participants'][participant_number - 1]['stats']['kills']
		team_player.deaths = response['participants'][participant_number - 1]['stats']['deaths']
		team_player.assists = response['participants'][participant_number - 1]['stats']['assists']
		team_player.gold = response['participants'][participant_number - 1]['stats']['goldEarned']
		team_player.damage_dealt_to_champions = response['participants'][participant_number - 1]['stats']['totalDamageDealtToChampions']
		team_player.damage_taken = response['participants'][participant_number - 1]['stats']['totalDamageTaken']
		team_player.wards_placed = response['participants'][participant_number - 1]['stats']['wardsPlaced']
		team_player.wards_killed = response['participants'][participant_number - 1]['stats']['wardsKilled']
		team_player.cs = response['participants'][participant_number - 1]['stats']['totalMinionsKilled']

		return team_player