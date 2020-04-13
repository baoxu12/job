from django.contrib import admin
from .models import *
from Boss.models import *
from Graduate.models import *

# Register your models here.

admin.site.register(Admins)
admin.site.register(C_type)
admin.site.register(Company)
admin.site.register(Boss)
admin.site.register(Job)
admin.site.register(Job_table)
admin.site.register(Hunter)
admin.site.register(City)
