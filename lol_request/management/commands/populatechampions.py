from django.core.management.base import BaseCommand, CommandError
from lol_request.models import Champion

import json

class Command(BaseCommand):
	help = 'Gets a league of legends oficial data of champions.json and populate the database'

	def add_arguments(self, parser):
		parser.add_argument('path', type=str, help='The json file location')

	def handle(self, *args, **kwargs):
		path = kwargs['path']

		with open(path, 'r') as f:
			json_data = json.load(f)

			for data in json_data['data']:
				champion = Champion()
				champion.version = json_data['data'][data]['version']
				champion.name = json_data['data'][data]['id']
				champion.lol_key = json_data['data'][data]['key']
				champion.title = json_data['data'][data]['title']
				champion.description = json_data['data'][data]['blurb']
				champion.image = json_data['data'][data]['image']['full']
				champion.save()

		self.stdout.write(self.style.SUCCESS('Champions created successfully'))