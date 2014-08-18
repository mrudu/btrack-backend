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
		fields = ['username']
		filtering = {
			'username': ALL,
		}

# Contains a list of Customers in business with the company.
class CustomerResource(ModelResource):
	class Meta:
		queryset = Customer.objects.all()
		resource_name = 'customer'
		authorization = Authorization()
		filtering = {
			'id': ALL,
		}

# Category of products being shipped such as Transfer Case, Synchronizers, etc.
class ProductResource(ModelResource):
	customer = fields.ForeignKey(CustomerResource,'customer')
	class Meta:
		queryset = Product.objects.all()
		resource_name = 'product'
		authorization = Authorization()
		filtering = {
			'customer': ALL_WITH_RELATIONS
		}

# On-going, completed and suspended projects 
class ProjectResource(ModelResource):
	product = fields.ForeignKey(ProductResource, 'product')
	createdBy = fields.ToOneField(UserResource, 'createdBy', full=True)
	class Meta:
		queryset = Project.objects.all()
		resource_name = 'project'
		authorization = Authorization()

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

class WTaskResource(ModelResource):
	workflow = fields.ForeignKey(WorkflowResource, 'workflow')
	class Meta:
		queryset = WTask.objects.all()
		resource_name = 'workflow_task'
		authorization = Authorization()

class TaskResource(ModelResource):
	assigned_to = fields.ForeignKey(UserResource,'user')
	assigned_by = fields.ForeignKey(UserResource,'user')
	wtask = fields.ForeignKey(WTaskResource, 'workflow_task')

	class Meta:
		queryset = Workflow.objects.all()
		resource_name = 'task'
		authorization = Authorization()
