from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class CommonToken(models.Model):
	name = models.CharField(max_length=100)
	def __str__(self):
		return self.name
	class Meta:
		abstract = True

class Class(CommonToken):
	pass

class Ability(CommonToken):
	desc = models.CharField(max_length=2000, default = '')
	cls = models.ForeignKey(Class, default = None)
	required_level = models.PositiveIntegerField()
	exp_cost = models.PositiveIntegerField(default = 0)

class Item(CommonToken):
	SLOTS = (
		('s', 'Default Small Slot'),
		('l', 'Default Large Slot'),
	)
	desc = models.CharField(max_length=2000, default = '')
	production_cost = {}
	slot = models.CharField(max_length=1, choices = SLOTS)

class ItemToken(models.Model):
	item = models.ForeignKey(Item)
	count = models.PositiveIntegerField()
	price = models.PositiveIntegerField(default=0)
	available = models.BooleanField(default=True)
	def __str__(self):
		return self.item.name + ' x' + str(self.count)

# we strongly recommend you not use Account model; 
# use django.contrib.auth.User model instead in any occurence you don't know which to choose.
class Account(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	items = models.ManyToManyField(ItemToken, blank=True)

class Char(CommonToken):
	host = models.ForeignKey(User, default = User.objects.filter(pk=2)[0].pk)
	abilities = models.ManyToManyField(Ability, blank=True)

class Mission(CommonToken):
	MISSION_STATUS = (
		(0, 'Not opened'),
		(1, 'Opened'),
		(2, 'Closed'),
		(3, 'Finalized'),
	)
	participants = models.ManyToManyField(Char)
	pub_date = models.DateField()
#	status = models.CharField(max_length=1, choices = MISSION_STATUS)

class Report(models.Model):
	text = models.CharField(max_length = 10000)
	pub_date = models.DateField()
	related_mission = models.ForeignKey(Mission)
	related_char = models.ForeignKey(Char)

