from django.db import models
from django.contrib.auth.models import User, Group
import datetime
from django.core.exceptions import ObjectDoesNotExist

CATEGORY_CHOICES = (
	('WTC','World Transfer Cases'),
	('ACE','ACE'),
	('Comp','Components (Exports/Domestic)'),
	('Synchro','Synchronizers'),
	('NTC','Next Generation Platforms/Transfer Cases'),
	('PTU','Nextrac/ Power Transfer Units'),
	('DEF','Defense'),
	('eGear','eGear'),
	('Oth','Others')
)
PRODUCTION_CHOICES = (('Bho', 'Bhosari'),('Sir', 'Sirsi'))
GENERATED_CHOICES = (('S','Self Generated'),('C','Customer Generated'))


# Refers to the Companies who buy DW's products. eg. "Mahindra and Mahindra"
class Customer(models.Model):
	name = models.CharField(max_length = 100, blank=False)
	revenue = models.IntegerField(default=0)

	class Meta:
		ordering = ["name"]
	def __unicode__(self):
		return self.name


#Refers to the list of On-Going/Suspended/Completed Projects
class Project(models.Model):
	reference = models.CharField(max_length=70, default="DW/MKT/001") # Reference Number of the project. Should be auto-generated.
	createdBy = models.ForeignKey(User) # Describes who is in charge of the product. Related to the User model. Auto-generated - based on session of user.
	created_on = models.DateTimeField(auto_now_add = True) # Records when the project was created. Auto-populated.
	generated = models.CharField(max_length=1,choices= GENERATED_CHOICES) # Describes whether the project is Self Generated or Customer Generated.
	progress = models.IntegerField(default=0) # Shows the number of days by which the project has been delayed.
	product = models.CharField(max_length = 50, choices = CATEGORY_CHOICES) # Describes the category of products the customer is interested in buying.
	customer = models.ForeignKey(Customer) # Links to the Customer model of the Project.
	title = models.CharField(max_length = 100) # Usually the name of the product the customer is buying. Ex. Ring Gear-001, Tundra Flange.
	volume = models.IntegerField(default = 0) # The amount of pieces supplied in a year.
	price = models.IntegerField(default = 0) # Price per piece
	life = models.IntegerField(default = 5) # Duration of the project
	winprobability = models.IntegerField(default = 0) # Probability of getting the business. Out of hundred.
	part_no = models.CharField(default = "000", max_length=100) # Part Number of the Product getting Manufactured.
	status = models.SmallIntegerField(default = 0) # Project status. 0-On-going, 1-Suspended, 2-Completed
	edit_date = models.DateTimeField(blank=True) # Latest Edit Date.
	description = models.CharField(max_length = 800, blank = True) # Project Scope and description.
	sopDate = models.DateTimeField() # Tentative Start-Of-Production Date.
	pop = models.CharField(choices = PRODUCTION_CHOICES, max_length = 50) # Place of Production - Bhosari or Sirsi.
	tot_revenue = models.BigIntegerField(blank=True,null=True)
	year_revenue = models.BigIntegerField(blank=True,null=True)
	late_status = models.IntegerField(default = 0)
	
	class Meta:
		ordering = ['created_on']
	def __unicode__(self):
		return self.title
	def save(self, *args, **kwargs):
		try:
			self.edit_date = datetime.datetime.now()
			self.tot_revenue = self.price*self.volume*self.life
			self.year_revenue = self.price*self.volume
			if not self.pk:
				year = str(datetime.datetime.now().year)
				number = Project.objects.filter(created_on__gte = year+'-01-01').count()+1
				self.reference = 'DW/MKT/'+str(number)
			super(Project, self).save(*args, **kwargs)
		except ObjectDoesNotExist:
			return

# Daily Commentory on the Project
class Remark(models.Model):
	createdBy = models.ForeignKey(User) # Links to the User who wrote the remark. Auto-generated - based on session of user.
	created_on = models.DateTimeField(auto_now_add = True) # Records when the remark was created. Auto-populated.
	project = models.ForeignKey(Project) # Links to the project
	content = models.CharField(max_length = 10000, blank = False) # Content of the remark. Not to exceed 1000 charecters.
	class Meta:
		ordering = ['project','created_on']
	def __unicode__(self):
		return self.content


class Workflow(models.Model):
	name = models.CharField(max_length = 100)
	description = models.CharField(max_length = 800, blank = True)
	stage = models.SmallIntegerField()
	def __unicode__(self):
		return self.name

	class Meta:
		ordering = ['stage']

class Task(models.Model): 
	workflow = models.ForeignKey(Workflow)
	project = models.ForeignKey(Project, related_name="tasks")
	start_date = models.DateTimeField(default=datetime.datetime.now,blank=True)
	due_date = models.DateTimeField()
	end_date = models.DateTimeField(blank=True,null=True)
	description = models.CharField(max_length = 800)
	remarks = models.CharField(max_length = 100)
	class Meta:
		ordering = ['project','end_date']
		unique_together = (('workflow','project'),)
	def __unicode__(self):
		return self.project.title
	
class Track(models.Model):
	month = models.CharField(max_length = 3)
	suspended = models.IntegerField(default = 0)
	active = models.IntegerField(default = 0)
	completed = models.IntegerField(default = 0)
	year = models.CharField(max_length = 4)
