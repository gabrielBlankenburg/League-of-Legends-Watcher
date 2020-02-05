class ResponseFormatter:
	def format_player_games_list_response(self, summoner, matches_teams_players):
		"""Formats the search games by nick response.

		Parameters
		----------
		summoner : lol_request.models.Summoner
		matches_teams_players : dict
			The format of the dict is the following:
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

		Returns
		-------
		dict
			Formatted game info and list of dicts with games info.
		"""
		formatted = []
		for match in matches_teams_players:
			match_team_player = matches_teams_players[match]
			response = {
				'game_creation': match_team_player['team_one'][0].team.game.creation,
				'game_duration': match_team_player['team_one'][0].team.game.duration,
				'game_mode': match_team_player['team_one'][0].team.game.mode,
				'game_type': match_team_player['team_one'][0].team.game.lol_game_type,
				#'map_id': match_team_player['team_one'][0].team.game.map_id,
				'team_one': {
					'win': match_team_player['team_one'][0].team.win,
					'players': self._format_games_players_list(match_team_player['team_one'])
				},
				'team_two': {
					'win': match_team_player['team_two'][0].team.win,
					'players': self._format_games_players_list(match_team_player['team_two'])
				}
			}

			formatted.append(response)

		return {
			'summoner': {
				'nickname': summoner.name,
				'icon_id': summoner.icon_id,
				'level': summoner.level,
				'tier_solo': summoner.tier_solo,
				'rank_solo': summoner.rank_solo,
				'points_solo': summoner.points_solo,
				'tier_flex': summoner.tier_flex,
				'rank_flex': summoner.rank_flex,
				'points_flex': summoner.points_flex
			},
			'games': formatted
		}

	def _format_games_players_list(self, team_players):
		"""Format the players of a lol_request.models.TeamPlayer object.

		Parameters
		----------
		team_players : lol_request.models.TeamPlayer

		Returns
		-------
		list
			Formatted list of dicts with players of the teams info.
		"""
		formatted = []
		for team_player in team_players:
			formatted.append({
				'champion': {
					'id': team_player.champion_chosen.lol_key,
					'name': team_player.champion_chosen.name,
					'image': team_player.champion_chosen.image
				},
				'ban': self._get_champion_ban(team_player),
				'player': {
					'summoner_name': team_player.player.name,
					'platform_id': 'BR1',
					'lol_id': team_player.player.lol_id,
					'puuid': team_player.player.puuid,
					'icon_id': team_player.player.icon_id,
					'icon_url': 'url',
					'account_id': team_player.player.account_id,
					'level': team_player.player.level,
					'rank_solo': team_player.player.rank_solo,
					'tier_solo': team_player.player.tier_solo,
					'points_solo': team_player.player.points_solo,
					'rank_flex': team_player.player.rank_flex,
					'tier_flex': team_player.player.tier_flex,
					'points_flex': team_player.player.points_flex,
					'match_history_uri': team_player.match_history_uri
				},
				"kills": team_player.kills,
				"deaths": team_player.deaths,
				"assists": team_player.assists,
				"gold": team_player.gold,
				"damage_dealt_to_champions": team_player.damage_dealt_to_champions,
				"damage_taken": team_player.damage_taken,
				"wards_placed": team_player.wards_placed,
				"wards_killed": team_player.wards_killed,
				"cs": team_player.cs
			})

		return formatted

	def _get_champion_ban(self, team_player):
		"""Get the banned champion of the player

		Parameters
		----------
		team_player : lol_request.models.TeamPlayer
		
		Returns
		-------
		dict
		"""
		try:
			return {
				'id': team_player.champion_ban.lol_key,
				'name': team_player.champion_ban.name,
				'image': team_player.champion_ban.image
			}
		except:
			return {}