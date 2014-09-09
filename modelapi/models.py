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
	('Oth','Others')
)
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
	priority = models.SmallIntegerField(default= 0) # Describes the priority of the project. High-3, Medium-2, Low-1.
	progress = models.IntegerField(default=0) # Describes the completion stage of the project. Auto-generated depending on the workflow status.
	product = models.CharField(max_length = 50, choices = CATEGORY_CHOICES) # Describes the category of products the customer is interested in buying.
	customer = models.ForeignKey(Customer) # Links to the Customer model of the Project.
	title = models.CharField(max_length = 100) # Usually the name of the product the customer is buying. Ex. Ring Gear-001, Tundra Flange.
	volume = models.IntegerField(default = 0) # The amount of pieces supplied in a year.
	price = models.IntegerField(default = 0) # Price per piece
	life = models.IntegerField(default = 5) # Duration of the project
	winprobability = models.IntegerField(default = 0) # Probability of getting the business. Out of hundred.
	part_no = models.CharField(default = "000", max_length=100)
	status = models.SmallIntegerField(default = 0) # Project status. 0-On-going, 1-Suspended, 2-Completed
	edit_date = models.DateTimeField(blank=True) # Latest Edit Date.
	description = models.CharField(max_length = 800, blank = True) # Project Scope and description.
	sopDate = models.DateTimeField() # Tentative Start-Of-Production Date.
	pop = models.CharField(choices = PRODUCTION_CHOICES, max_length = 50) # Place of Production - Bhosari or Sirsi.
	tot_revenue = models.IntegerField(blank=True,null=True)
	year_revenue = models.IntegerField(blank=True,null=True)
	
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

class OppProChe(models.Model):
	project = models.ForeignKey(Project)
	NDA = models.NullBooleanField(default=False, blank=True,null=True)
	PDS = models.NullBooleanField(default=False, blank=True,null=True)
	PFR = models.NullBooleanField(default=False, blank=True,null=True)
	NBO = models.NullBooleanField(blank=True,default=False, null=True)
	TFC = models.NullBooleanField(blank=True,default=False, null=True)
	IRS = models.NullBooleanField(blank=True,default=False, null=True)
	FRS = models.NullBooleanField(blank=True,default=False, null=True)
	ProjectApproved = models.NullBooleanField(blank=True,default=False, null=True)
	QUO = models.NullBooleanField(blank=True,default=False, null=True)
	LOI = models.NullBooleanField(blank=True,default=False, null=True)
	CCRecieve = models.NullBooleanField(blank=True,default=False, null=True)
	CCReview = models.NullBooleanField(blank=True,default=False, null=True)
	CCFrozen = models.NullBooleanField(blank=True,default=False, null=True)
	PPAPPORecieve = models.NullBooleanField(blank=True,default=False, null=True)
	PPAPPOReview = models.NullBooleanField(blank=True,default=False, null=True)
	POAccepted = models.NullBooleanField(blank=True,default=False, null=True)
	def __unicode__(self):
		return self.project
	def save(self, *args, **kwargs):
		if self.PFR:
			if not self.PDS:
				return
		if self.NBO:
			if not self.PFR:
				return
		if self.TFC:
			if not self.NBO:
				return
		if self.IRS:
			if not self.TFC:
				return
		if self.FRS:
			if not self.IRS:
				return
		if self.ProjectApproved:
			if not self.FRS:
				return
		if self.QUO:
			if not self.ProjectApproved:
				return
		if self.LOI:
			if not self.QUO:
				return
		if self.CCRecieve:
			if not self.LOI:
				return
		if self.CCReview:
			if not self.CCRecieve:
				return
		if self.CCFrozen:
			if not self.CCReview:
				return
		if self.PPAPPORecieve:
			if not self.CCFrozen:
				return
		if self.PPAPPOReview:
			if not self.PPAPPORecieve:
				return
		if self.POAccepted:
			if not self.PPAPPOReview:
				return	
		super(OppProChe, self).save(*args, **kwargs)

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

#Different forms which need to be filled
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
	workflow = models.ForeignKey(Workflow)
	project = models.ForeignKey(Project, related_name="tasks")
	start_date = models.DateTimeField(default=datetime.datetime.now,blank=True)
	due_date = models.DateTimeField()
	end_date = models.DateTimeField(blank=True,null=True)
	description = models.CharField(max_length = 800)
	remarks = models.CharField(max_length = 100)
	class Meta:
		ordering = ['project','start_date']
		unique_together = (('workflow','project'),)
	def __unicode__(self):
		return self.project.title
	
class STask(models.Model):
	name = models.CharField(max_length = 100)
	description = models.CharField(max_length = 800)
	start_date = models.DateTimeField(default=datetime.datetime.now,blank=True)
	due_date = models.DateTimeField()
	end_date = models.DateTimeField(blank = True,null=True)
	task = models.ForeignKey(Task)
	wtask = models.ForeignKey(WTask)
	assigned_to = models.ForeignKey(User, related_name = "assigned_to")
	assigned_by = models.ForeignKey(User, related_name = "assigned_by")
	identification = models.CharField(max_length = 50)
	def __unicode__(self):
		return self.name

