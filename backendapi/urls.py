from django.conf.urls import *
from report.views import *
from modelapi.views import *
from modelapi.api import *
from tastypie.api import Api
from apqp.api import *
from apqp.views import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

v1_api = Api(api_name = 'v1')
v1_api.register(CustomerResource())
v1_api.register(ProjectResource())
v1_api.register(WorkflowResource())
v1_api.register(TaskResource())
v1_api.register(UserResource())
v1_api.register(RemarkResource())

v2_api = Api(api_name = 'v2')
v2_api.register(SupplierResource())
v2_api.register(SupplierProjectResource())

urlpatterns = patterns('',
	(r'^api/v1/mailupdate/$', mailupdate),
	(r'^api/v1/salesmanmatrix/$', usermatrix),
	(r'^api/v1/progressupdate/$', progressUpdate),
	(r'^api/v1/cpc/$', categoryPieChart),
	(r'^api/v1/statusupdate/$',statusUpdate),
	(r'^api/v1/dashboard/$', dashboard),
	(r'^api/v2/suppost/$', postapqpform),
	(r'^api/', include(v1_api.urls)),
	(r'^api/', include(v2_api.urls)),
	(r'^dbcreate/$',createdb),
	(r'^taskcreate/$',tasksave),
	(r'^download/(?P<urltype>[a-zA-Z]+)/$',backup),
	(r'^remarksdownload/$',remarksbackup),
    # Examples:
    # url(r'^$', 'backendapi.views.home', name='home'),
    # url(r'^backendapi/', include('backendapi.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
