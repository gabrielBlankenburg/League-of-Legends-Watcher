from django.conf import settings 
from .ServiceInjector import di
from lol_request.services.LolApi import LolApi
from lol_request.services.ApiToModelConverter import ApiToModelConverter
from lol_request.services.ResponseFormatter import ResponseFormatter
import requests

di.register('LolApi', "https://br1.api.riotgames.com/lol", settings.LOL_KEY, requests)(LolApi)
di.register('ApiToModelConverter')(ApiToModelConverter)
di.register('ResponseFormatter')(ResponseFormatter)