from tastypie.authorization import Authorization
from tastypie.resources import ModelResource
from tastypie import fields
from modelapi.models import *
from tastypie.serializers import Serializer

class UserResource(ModelResource):
	class Meta:
		queryset = User.objects.all()
		resource_name = 'user'
		authorization = Authorization()
		excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
		serializer = Serializer(formats=['json'])

class CustomerResource(ModelResource):
	class Meta:
		queryset = Customer.objects.all()
		resource_name = 'customer'
		authorization = Authorization()

class ProductResource(ModelResource):
	customer = fields.ForeignKey(CustomerResource,'customer')
	class Meta:
		queryset = Product.objects.all()
		resource_name = 'product'
		authorization = Authorization()

class ProjectResource(ModelResource):
	product = fields.ForeignKey(ProductResource, 'product')
	createdBy = fields.ForeignKey(UserResource, 'user')
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
		resource_name = 'workflow'
		authorization = Authorization()
