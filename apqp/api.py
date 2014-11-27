from tastypie.authorization import Authorization
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields
from apqp.models import *
from tastypie.serializers import Serializer

'''
This file describes the resources for api reference.
'''
# Users comprise of mainly the employees of the company within various departments.
# POST, GET, DELETE and PUT operations on users. 
# Most important field is username, password, email and group.
# Will have to make it accept username and password or set a default one. 
# Set permission classes for different users.
# Need to create notification and remarks(linked to projecct also) table for this.
class EmployeeResource(ModelResource):
	class Meta:
		queryset = SupplierProject.objects.all()
		resource_name = 'employee'
		authorization = Authorization()
		filtering = {
			'name':ALL,
		}

class DWTeamResource(ModelResource):
	vd = fields.ToOneField(EmployeeResource, 'vd', full=True)
	sta = fields.ToOneField(EmployeeResource, 'sta', full=True)
	engg = fields.ToOneField(EmployeeResource, 'engg', full=True)
	mfg = fields.ToOneField(EmployeeResource, 'mfg', full=True)
	gaugesupport = fields.ToOneField(EmployeeResource, 'gaugesupport', full=True)
	quality = fields.ToOneField(EmployeeResource, 'quality', full=True)
	metallurgist = fields.ToOneField(EmployeeResource, 'metallurgist', full=True)
	production = fields.ToOneField(EmployeeResource, 'production', full=True)
	class Meta:
		queryset = DWTeam.objects.all()
		resource_name = 'dwteam'
		authorization = Authorization()
		filtering = ()

class SupplierTeamResource(ModelResource):
	md = fields.ToOneField(EmployeeResource, 'md', full=True)
	marketing = fields.ToOneField(EmployeeResource, 'marketing', full=True)
	design = fields.ToOneField(EmployeeResource, 'design', full=True)
	projectleader = fields.ToOneField(EmployeeResource, 'projectleader', full=True)
	class Meta:
		queryset = SupplierTeam.objects.all()
		resource_name = 'supplierteam'
		authorization = Authorization()
		filtering = ()

class SupplierResource(ModelResource):
	dwteam = fields.ToOneField(DWTeamResource, 'dwteam', full=True)
	suppteam = fields.ToOneField(SupplierTeamResource, 'suppteam', full=True)
	class Meta:
		queryset = Supplier.objects.all()
		resource_name = 'supplier'
		authorization = Authorization()
		filtering = {
			'name': ALL,
		}
class SupplierProjectResource(ModelResource):
	supplier = fields.ToOneField(SupplierResource, 'supplier', full=True)
	dwteam = fields.ToOneField(DWTeamResource, 'dwteam', full=True)
	suppteam = fields.ToOneField(SupplierTeamResource, 'suppteam', full=True)
	class Meta:
		queryset = SupplierProject.objects.all()
		resource_name = 'supplierproject'
		authorization = Authorization()
		filtering = {
			'name':ALL,
		}

class ProgramsResource(models.Model):
	class Meta:
		queryset = Programs.objects.all()
		resource = 'programs'
		authorization = Authorization()
		filtering = ()

class ProjectProgramsResource(models.Model):
	program = fields.ToOneField(ProgramsResource, 'program', full=True)
	project = fields.ToOneField(SupplierProjectResource, 'project', full=True)
	class Meta:
		queryset = ProjectPrograms.objects.all()
		resource = 'projectprograms'
		authorization = Authorization()
		filtering = ()
