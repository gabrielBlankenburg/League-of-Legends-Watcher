from django.urls import path

from . import views

app_name = 'lol_request'
urlpatterns = [
	path('player/<str:name>', views.PlayerGames.as_view(), name='player_info')
]