from django.conf.urls import patterns, include, url
from django.contrib import admin
from main.views import PortView, DockDetailView, generate_employees


admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', PortView.as_view() , name='port'),
    url(r'^dock/(?P<pk>\d+)$', DockDetailView.as_view() , name='dock_detail'),
    url(r'^generate_employees$', generate_employees , name='generate_employees'),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
