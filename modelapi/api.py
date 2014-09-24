from tastypie.authorization import Authorization
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields
from modelapi.models import *
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
class UserResource(ModelResource):
	class Meta:
		queryset = User.objects.all()
		resource_name = 'user'
		authorization = Authorization()
		fields = ['username','first_name']
		filtering = {
			'username': ALL,
		}

# Contains a list of Customers in business with the company.
class CustomerResource(ModelResource):
	class Meta:
		queryset = Customer.objects.all()
		resource_name = 'customer'
		authorization = Authorization()
		fields = ['name','id']
		filtering = {
			'id': ALL,
			'name': ALL
		}

# On-going, completed and suspended projects 
class ProjectResource(ModelResource):
	customer = fields.ToOneField(CustomerResource, 'customer', full=True)
	createdBy = fields.ToOneField(UserResource, 'createdBy', full=True)
	tasks = fields.ToManyField('modelapi.api.TaskResource', 'tasks',full=True,null=True)
	class Meta:
		queryset = Project.objects.all()
		resource_name = 'project'
		authorization = Authorization()
		filtering = {
			"id": ALL_WITH_RELATIONS,
			"winprobability": ALL,
			"sopDate": ALL,
			"status":ALL,
			"product":ALL,
			"tasks":ALL_WITH_RELATIONS
		}
		ordering = {
			"tot_revenue":ALL
		}

class FormResource(ModelResource):
	class Meta:
		queryset = Form.objects.all()
		resource_name = 'form'
		authorization = Authorization()

class WorkflowResource(ModelResource):
	class Meta:
		queryset = Workflow.objects.all()
		resource_name = 'workflow'
		authorization = Authorization()
		filtering = {
			'stage': ALL,
			'id':ALL_WITH_RELATIONS,
		}
		ordering = {
			'stage': ALL
		}

class WTaskResource(ModelResource):
	workflow = fields.ForeignKey(WorkflowResource, 'workflow')
	class Meta:
		queryset = WTask.objects.all()
		resource_name = 'workflow_task'
		authorization = Authorization()

class TaskResource(ModelResource):
	project = fields.ForeignKey(ProjectResource,'project')
	workflow = fields.ToOneField(WorkflowResource, 'workflow', full=True)

	class Meta:
		queryset = Task.objects.all()
		resource_name = 'task'
		authorization = Authorization()
		filtering = {
			'project': ALL_WITH_RELATIONS,
			'workflow':ALL_WITH_RELATIONS,
			'id':ALL_WITH_RELATIONS,
			'end_date':ALL_WITH_RELATIONS,
		}

class RemarkResource(ModelResource):
	createdBy = fields.ToOneField(UserResource, 'createdBy', full=True)
	project = fields.ToOneField(ProjectResource, 'project', full=True)
	class Meta:
		queryset = Remark.objects.all()
		resource_name = 'remark'
		authorization = Authorization()
		filtering = {
			'project' :ALL_WITH_RELATIONS
		}

# Opportunity Progress Checklist
class OPCResource(ModelResource):
	project = fields.ToOneField(ProjectResource, 'project', full=True)
	class Meta:
		queryset = OppProChe.objects.all()
		resource_name = 'opc'
		authorization = Authorization()
		filtering = {
			'project': ALL_WITH_RELATIONS
		}

