from django.db import models
from django.core.validators import RegexValidator

# This Project is for the APQP Software.

PURPOSE_CHOICES = (('NEW', 'New Part'),('LOC', 'Localization'),('COST','Cost Reduction'),('ALT','Alternate Source'))

SUPPLIER_CHOICES = (('LOC','Local Supplier'),('SUB','Sub COntracted Supplier'),('IMP','Imported Supplier'))

class Employee(models.Model):
	name = models.CharField(max_length =50)
	email = models.EmailField(unique=True)
	ph = models.CharField(max_length=10,validators=[RegexValidator(regex='^\d{10}$', message='Phone number has to be 10 digits long.', code='nomatch')])

class DWTeam(models.Model):
	vd = models.ForeignKey(Employee, related_name="vd")
	sta = models.ForeignKey(Employee, related_name="sta")
	engg = models.ForeignKey(Employee, related_name="engg")
	mfg = models.ForeignKey(Employee, related_name="mfg")
	gaugesupport = models.ForeignKey(Employee, related_name="gaugesupport")
	quality = models.ForeignKey(Employee, related_name="quality")
	metallurgist = models.ForeignKey(Employee, related_name="metallurgist")
	production = models.ForeignKey(Employee, related_name="production")
	class Meta:
		unique_together = ('vd','sta','engg','mfg','gaugesupport','quality','metallurgist','production')

class SupplierTeam(models.Model):
	md = models.ForeignKey(Employee, related_name="md")
	marketing = models.ForeignKey(Employee, related_name="marketing")
	design = models.ForeignKey(Employee, related_name="design")
	projectleader = models.ForeignKey(Employee, related_name="projectleader")
	class Meta:
		unique_together = ('md','marketing','design','projectleader')

class Supplier(models.Model):
	name = models.CharField(max_length = 120,unique=True)
	category = models.CharField(max_length=10,choices = SUPPLIER_CHOICES)
	created_on = models.DateTimeField(auto_now_add= True)
	dwteam = models.ForeignKey(DWTeam, null=True)
	suppteam = models.ForeignKey(SupplierTeam, null=True)

class SupplierProject(models.Model):
	created_on = models.DateTimeField(auto_now_add= True)
	dwteam = models.ForeignKey(DWTeam)
	suppteam = models.ForeignKey(SupplierTeam)
	number = models.CharField(max_length = 50)
	name = models.CharField(max_length = 150)
	partname = models.CharField(max_length = 200)
	partnumber = models.CharField(max_length = 100)
	purpose = models.CharField(max_length = 5, choices = PURPOSE_CHOICES)
	supplier = models.ForeignKey(Supplier)
	teamfeasibility = models.BooleanField()
	ponumber = models.CharField(max_length = 100)
	status = models.CharField(max_length=10)

class Programs(models.Model):
	description = models.CharField(max_length = 100)
	phase = models.SmallIntegerField(default = 0)
	def __unicode__(self):
		return self.description[:10]+" "+str(self.phase)

class ProjectPrograms(models.Model):
	program = models.ForeignKey(Programs)
	project = models.ForeignKey(SupplierProject)
	need_date = models.DateTimeField(blank = True,null=True)
	supplier_date = models.DateTimeField(blank = True,null=True)
	close_date = models.DateTimeField(blank = True,null=True)
	status = models.SmallIntegerField(default = 0)
	Remarks = models.CharField(max_length=500)
	attachments = models.FileField(upload_to = 'files/%Y/%m/%d')
