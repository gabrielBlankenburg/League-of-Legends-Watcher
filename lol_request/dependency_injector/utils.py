from .ServiceInjector import di
from lol_request.models import Game, Team, Summoner, TeamPlayer, Champion
import requests

di.register('requests')(requests)
di.register('Game')(Game)
di.register('Team')(Team)
di.register('Summoner')(Summoner)
di.register('TeamPlayer')(TeamPlayer)
di.register('Champion')(Champion)