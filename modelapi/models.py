from django.db import models
from django.contrib.auth.models import User, Group
import datetime

CATEGORY_CHOICES = (('Comp','Components'),('Synchro','Synchronizers'),('T/c','Next Generation Transfer Cases'),('PTU','Next Trac Power Transfer Units'),('Oth','Others'))
PRODUCTION_CHOICES = (('Bho', 'Bhosari'),('Sir', 'Sirsi'))

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

class Project(models.Model):
	createdBy = models.ForeignKey(User) # Describes who is in charge of the product. Related to the User model. Auto-generated - based on session of user.
	reference = models.CharField(max_length=70, default="DW/MKT/001") # Reference Number of the project. Should be auto-generated.
	created_on = models.DateTimeField(auto_now_add = True) # When the project was created. Auto-populated - date and time entry was created.
	priority = models.SmallIntegerField(default= 0) # Describes the priority of the project. High-3, Medium-2, Low-1.
	progress = models.IntegerField(default=0) # Describes the completion stage of the project. Auto-generated depending on the workflow status.
	product = models.CharField(max_length = 10, choices = CATEGORY_CHOICES) # Describes the category of products the customer is interested in buying.
	customer = models.ForeignKey(Customer) # Links to the Customer model of the Project.
	title = models.CharField(max_length = 100) # Usually the name of the product the customer is buying. Ex. Ring Gear-001, Tundra Flange.
	volume = models.IntegerField(default = 0) # The amount of pieces supplied in a year.
	price = models.IntegerField(default = 0) # Price per piece
	life = models.IntegerField(default = 5) # Duration of the project
	winprobability = models.IntegerField(default = 0) # Probability of getting the business. Out of hundred.
	part_no = models.IntegerField(default = 0)
	status = models.SmallIntegerField(default = 0) # Project status. 0-On-going, 1-Suspended, 2-Completed
	edit_date = models.DateTimeField() # Latest Edit Date.
	description = models.CharField(max_length = 800, blank = True) # Project Scope and description.
	sopDate = models.DateTimeField() # Tentative Start-Of-Production Date.
	pop = models.CharField(choices = PRODUCTION_CHOICES, max_length = 50) # Place of Production - Bhosari or Sirsi.
	
	class Meta:
		ordering = ['created_on']
	def __unicode__(self):
		return self.title
	def save(self, *args, **kwargs):
		try:
			edit_date = datetime.datetime.now()
			if not self.pk:
				year = datetime.datetime.now().year
				number = super(Project,self).objects.filter(created_on__gte = year+'-01-01').count()+1
				self.reference = 'DW/MKT/'+number
			super(Project, self).save(*args, **kwargs)
		except ObjectDoesNotExist:
			return

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
