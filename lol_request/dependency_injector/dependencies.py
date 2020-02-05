from .ServiceInjector import di
from django.conf import settings 
from lol_request.services.ApiToModelConverter import ApiToModelConverter
from lol_request.services.ResponseFormatter import ResponseFormatter
from lol_request.services.LolApi import LolApi
from lol_request.models import Game, Team, Summoner, TeamPlayer, Champion
import requests

di.register('ApiToModelConverter')(ApiToModelConverter)
di.register('ResponseFormatter')(ResponseFormatter)
#LolApi("https://br1.api.riotgames.com/lol", settings.LOL_KEY)
di.register('LolApi', "https://br1.api.riotgames.com/lol", settings.LOL_KEY, requests)(LolApi)
di.register('requests')(requests)
di.register('Game')(Game)
di.register('Team')(Team)
di.register('Summoner')(Summoner)
di.register('TeamPlayer')(TeamPlayer)
di.register('Champion')(Champion)