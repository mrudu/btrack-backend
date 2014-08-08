from django.conf.urls import *
from modelapi import views
from modelapi.api import *
from tastypie.api import Api

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

v1_api = Api(api_name = 'v1')
v1_api.register(CustomerResource())
v1_api.register(ProductResource())
v1_api.register(ProjectResource())
v1_api.register(WorkflowResource())
v1_api.register(WTaskResource())
v1_api.register(FormResource())
v1_api.register(TaskResource())
v1_api.register(UserResource())

urlpatterns = patterns('',
	(r'^api/', include(v1_api.urls)),
    # Examples:
    # url(r'^$', 'backendapi.views.home', name='home'),
    # url(r'^backendapi/', include('backendapi.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
