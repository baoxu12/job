from django.urls import path,re_path
from Boss.views import *

urlpatterns = [
	re_path('index/(?P<page>\d+)',index),
	path('logout/',logout),

	path('add_job/',add_job),

	path('record/',record),
	path('boss_info/',boss_info),
	path('update/',update),
	path('company/',company),
	path('check/',check),
	path('invate/',invate),
	path('operate/',operate),
	path('delete_job/',delete_job),
	path('job_publish/',job_publish),
	re_path('job_list/(?P<status>[0123])/(?P<page>\d+)',job_list),
	re_path('send_status/(?P<status>[012345678])/(?P<page>\d+)',send_status),
]