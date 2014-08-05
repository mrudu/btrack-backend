from django.db import models
from django.contrib.auth.models import User, Group
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())

class Customer(models.Model):
	name = models.CharField(max_length = 100, blank=False)
	revenue = models.IntegerField(default=0)

	class Meta:
		ordering = ('name')

class Component(models.Model):
	name = models.CharField(max_length = 100, blank = False)
	partId = models.CharField(default="000")
	customer = models.ForeignKey(Customer)

	class Meta:
		ordering = ('customer_id')

class Project(models.Model):
	createdBy = models.ForeignKey(User)
	created_on = models.DateTimeField(auto_now_add = True)
	progress = model.IntegerField(default=0)
	component = models.ForeignKey(Component)
	title = models.CharField(max_length = 100, blank = True)

	class Meta:
		ordering = ('created_on')
