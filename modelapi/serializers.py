from rest_framework import serializers
from django.contrib.auth.models import User, Group
from modelapi.models import LANGUAGE_CHOICES, STYLE_CHOICES, Customer, Project, Component

class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = User
		fields = ('url', 'username', 'email', 'groups')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Group
		fields = ('url', 'name')

class CustomerSerializer(serializers.ModelSerializer):
	components = serializers.RelatedField(True)
	class Meta:
		model= Customer
		fields = ('id','name','revenue')

class ComponentSerializer(serializers.ModelSerializer):
	projects = serializer.RelatedField(True)
	class Meta:
		model= Component

class ProjectSerializer(serializers.ModelSerializer):
	class Meta:
		model = Project

class WorkflowSerializer(serializers.ModelSerializer):
	class Meta:
		model = Workflow



