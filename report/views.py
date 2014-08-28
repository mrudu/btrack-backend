# Create your views here.
from django.http import HttpResponse
from modelapi.models import Project
from tastypie.serializers import Serializer

serializer = Serializer()
def serialize_queryset(resource_class, queryset):
	# hand me a queryset, i give you dehydrated resources
	resource = resource_class()
	dd = {}
	# make meta
	dd['meta'] = {}
	dd['meta']['limit'] = 1000
	dd['meta']['next'] = None
	dd['meta']['offset'] = 0
	dd['meta']['previous'] = None
	dd['meta']['total_count'] = len(queryset)
	# objects
	dd['objects'] = []
	for obj in queryset:
		bundle = resource.build_bundle(obj=obj)
		dehydrated_obj = resource.full_dehydrate(bundle)
		dd['objects'].append(dehydrated_obj)
	# return dict
	return dd
def report1(request):
	topten = Project.objects.extra(select={'revenue':'price*volume*life'},order_by=('-revenue',))
	data = serializer.to_json(topten)
	return HttpResponse(data, mimetype="application/json")
