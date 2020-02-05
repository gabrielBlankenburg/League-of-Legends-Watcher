from django.db import models

class Summoner(models.Model):
	lol_id = models.CharField(max_length=63)
	name = models.CharField(max_length=200)
	icon_id = models.IntegerField()
	puuid = models.CharField(max_length=78)
	account_id = models.CharField(max_length=56)
	level = models.IntegerField()
	tier_solo = models.CharField(max_length=10)
	tier_flex = models.CharField(max_length=10)
	rank_solo = models.IntegerField()
	rank_flex = models.IntegerField()
	points_solo = models.IntegerField()
	points_flex = models.IntegerField()

	def __str__(self):
		return self.name

	class Meta:
		managed = False

class Champion(models.Model):
	lol_key = models.IntegerField()
	name = models.CharField(max_length=10)
	title = models.CharField(max_length=30)
	description = models.CharField(max_length=500)
	image = models.CharField(max_length=50)
	version = models.CharField(max_length=50)

	def __str__(self):
		return self.name

class Game(models.Model):
	lol_game_id = models.BigIntegerField()
	creation = models.BigIntegerField()
	duration = models.IntegerField()
	mode = models.CharField(max_length=20)
	lol_game_type = models.CharField(max_length=20)
	map_id: models.IntegerField()

	class Meta:
		managed = False

class Item(models.Model):
	item_id = models.IntegerField()
	name = models.CharField(max_length=30)
	description = models.CharField(max_length=500)
	image = models.CharField(max_length=200)

	def __str__(self):
		return self.name

	class Meta:
		managed = False

class Rune(models.Model):
	rune_id = models.IntegerField()
	name = models.CharField(max_length=20)
	description = models.CharField(max_length=500)
	image = models.CharField(max_length=200)

	class Meta:
		managed = False

class ItemAttribute(models.Model):
	item = models.ForeignKey(Item, on_delete=models.CASCADE)
	attribute = models.CharField(max_length=20)

	def __str__(self):
		return self.attribute

	class Meta:
		managed = False

class Team(models.Model):
	game = models.ForeignKey(Game, on_delete=models.CASCADE)
	win = models.BooleanField()
	side = models.IntegerField()

	class Meta:
		managed = False

class TeamPlayer(models.Model):
	team = models.ForeignKey(Team, on_delete=models.CASCADE)
	player = models.ForeignKey(Summoner, on_delete=models.CASCADE)
	participant_number = models.IntegerField()
	match_history_uri = models.CharField(max_length=200)
	champion_chosen = models.ForeignKey(Champion, related_name='%(class)s_chosen', on_delete=models.CASCADE)
	champion_ban = models.ForeignKey(Champion, related_name='%(class)s_ban', on_delete=models.CASCADE)
	# primary_rune_slot_one = models.ForeignKey(Rune, on_delete=models.CASCADE)
	# primary_rune_slot_two = models.ForeignKey(Rune, on_delete=models.CASCADE)
	# primary_rune_slot_three = models.ForeignKey(Rune, on_delete=models.CASCADE)
	# primary_rune_slot_four = models.ForeignKey(Rune, on_delete=models.CASCADE)
	# secondary_rune_slot_one = models.ForeignKey(Rune, on_delete=models.CASCADE)
	# secondary_rune_slot_two = models.ForeignKey(Rune, on_delete=models.CASCADE)
	# perk_one = models.ForeignKey(Rune, on_delete=models.CASCADE)
	# perk_two = models.ForeignKey(Rune, on_delete=models.CASCADE)
	# perk_three = models.ForeignKey(Rune, on_delete=models.CASCADE)
	kills = models.IntegerField()
	deaths = models.IntegerField()
	assists = models.IntegerField()
	gold = models.IntegerField()
	damage_dealt_to_champions = models.IntegerField()
	damage_taken = models.IntegerField()
	wards_placed = models.IntegerField()
	wards_killed = models.IntegerField()
	cs = models.IntegerField()

	class Meta:
		managed = False

