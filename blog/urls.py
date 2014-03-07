from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from blog import api
api.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'blog.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(api.v1_api.urls)),
)
