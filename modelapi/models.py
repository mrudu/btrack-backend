from django.db import models
from django.contrib.auth.models import User, Group

CATEGORY_CHOICES = (('Comp','Components'),('Synchro','Synchronizers'),('T/c','Next Generation Transfer Cases'),('PTU','Next Trac Power Transfer Units'),('Oth','Others'))

class PossibleOpportunities(models.Model):
	customer = models.CharField(max_length = 100, blank = False)
	product = models.CharField(max_length = 100, blank = False)
	description = models.CharField(max_length = 800, blank = False)
	phone = models.CharField( max_length = 10, blank = False)
	name = models.CharField(max_length = 10)
	created_on = models.DateTimeField(auto_now_add = True)

	class Meta:
		ordering = ['created_on']
	def __unicode__self(self):
		return self.customer

class Customer(models.Model):
	name = models.CharField(max_length = 100, blank=False)
	revenue = models.IntegerField(default=0)

	class Meta:
		ordering = ["name"]
	def __unicode__(self):
		return self.name

class Product(models.Model):
	name = models.CharField(max_length = 100, blank = False)
	partId = models.CharField(default="000", max_length = 100)
	customer = models.ForeignKey(Customer)
	category = models.CharField(max_length = 10, choices = CATEGORY_CHOICES)

	class Meta:
		ordering = ['customer']
	def __unicode__(self):
		return self.name

class Project(models.Model):
	createdBy = models.ForeignKey(User)
	created_on = models.DateTimeField(auto_now_add = True)
	priority = models.SmallIntegerField(default= 0)
	progress = models.IntegerField(default=0)
	product = models.ForeignKey(Product)
	title = models.CharField(max_length = 100)
	price = models.IntegerField(default = 0)
	volume = models.IntegerField(default = 0)
	winprobability = models.IntegerField(default = 0)
	total_revenue = models.IntegerField(default = 0)
	pr_status = models.CharField(max_length = 100, blank = True)
	current_status = models.CharField(max_length = 300, blank = True)
	description = models.CharField(max_length = 800, blank = True)
	wf_status = models.IntegerField(default = 1)
	
	class Meta:
		ordering = ['created_on']
	def __unicode__(self):
		return self.title

class Form(models.Model):
	name = models.CharField(max_length = 100)
	file_path = models.FileField(upload_to = 'forms')
	description = models.CharField(max_length = 800)
	def __unicode__(self):
		return self.name

class Workflow(models.Model):
	name = models.CharField(max_length = 100)
	description = models.CharField(max_length = 800, blank = True)
	stage = models.SmallIntegerField()
	def __unicode__(self):
		return self.name

	class Meta:
		ordering = ['stage']

class WTask(models.Model):
	name = models.CharField(max_length = 100)
	description = models.CharField(max_length = 800, blank = True)
	workflow = models.ForeignKey(Workflow)
	form = models.ForeignKey(Form)
	substep = models.IntegerField(default = 1)
	class Meta:
		ordering = ['workflow', 'substep']
	def __unicode__(self):
		return self.name

class Task(models.Model):
	name = models.CharField(max_length = 100)
	description = models.CharField(max_length = 800)
	start_date = models.DateTimeField(auto_now_add = True)
	due_date = models.DateTimeField()
	end_date = models.DateTimeField(blank = True)
	wtask = models.ForeignKey(WTask)
	assigned_to = models.ForeignKey(User, related_name = "assigned_to")
	assigned_by = models.ForeignKey(User, related_name = "assigned_by")
	identification = models.CharField(max_length = 50)
	def __unicode__(self):
		return self.name
