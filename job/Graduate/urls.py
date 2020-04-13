from django.urls import path,re_path
from Graduate.views import *

urlpatterns = [
	path('index/',index),
	path('userinfo/',userinfo),
	path('update/',update),
	path('company_info/',company_info),
	path('job_info/',job_info),
	path('operate/',operate),
	path('resume/',resume),
	path('logout/',logout),
	path('send_resume/',send_resume),
	re_path('resume_status/(?P<status>[012345678])/(?P<page>\d+)',resume_status),
]