from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

urlpatterns = patterns('',
    url(r'^$', 'tmm.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^library/', include('library.urls')),
)

#urlpatterns += patterns(
#    'django.views.static',
#    (r'^media/(?P<path>.*)',
#    {'document_root': settings.MEDIA_ROOT}),
#    )
