# Create your views here.
from modelapi.models import *
from django.http import HttpResponse

def numberOfProjects(request):
	stage_name = request.stage
	return HttpResponse 
