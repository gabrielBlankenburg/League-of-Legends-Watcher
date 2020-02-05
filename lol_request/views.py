from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from rest_response import api_response

from .services import Search

# def player_info(request, name):
# 	search = Search()
# 	response = search.get_match_list_by_nick(name)

# 	return api_response.generic_response(body=response)

class PlayerGames(View):
	def get(request, *args, **kwargs):
		search = Search()
		response = search.get_match_list_by_nick(kwargs.get('name'))

		return api_response.generic_response(body=response)