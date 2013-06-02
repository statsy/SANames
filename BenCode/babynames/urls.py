from django.conf.urls import patterns, url

from babynames import views

urlpatterns=patterns('',url(r'^$',views.index,name='index'),
	url(r'^namepage/(?P<name>\w+)/$',views.namepage,name='namepage'),
	url(r'^namejson/(?P<name>\w+)/$',views.namejson,name='namejson'),
)