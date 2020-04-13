from django.urls import path,re_path
from Admins.views import *

urlpatterns = [
	re_path('index/(?P<page>\d+)',index),
	path('job_check/',job_check),
	path('check_operation/',check_operation),
	path('adm_info/',adm_info),
	re_path('hunter/(?P<page>\d+)/',hunter),
	re_path('boss/(?P<page>\d+)/',boss),
	path('update/',update),
	path('logout/',logout),
	path('operation/',operation),
	path('delete/',delete),
	re_path('job_manage/(?P<status>[01234])/(?P<page>\d+)',job_manage),
]