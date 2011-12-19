from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('',
    url(r'/$', 'analytics.views.home', name='home'),
    url(r'send_event/$', 'analytics.views.send_event', name='home'),
)
