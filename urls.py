from django.conf.urls.defaults import patterns, include, url

from tastypie.api import Api
from todoapp.api import TodoResource, UserResource
v1_api = Api(api_name='v1')
v1_api.register(TodoResource())
v1_api.register(UserResource())

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'todoapp.views.home', name='home'),
    url(r'^analytics/', include('analytics.urls'), name='home'),
    url(r'^api/', include(v1_api.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
