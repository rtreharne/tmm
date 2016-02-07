from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

urlpatterns = patterns('',
    url(r'^$', 'library.views.shelves', name='shelves'),
    url(r'^(?P<shelf>.*)/(?P<book>.*)/(?P<page>\d+)/$', 'library.views.page', name='page'),
    url(r'^(?P<shelf>.*)/(?P<book>.*)/$', 'library.views.book', name='book'),
    url(r'^(?P<shelf>.*)/$', 'library.views.shelf', name='shelf'),
)
