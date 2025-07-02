from django.contrib import admin

# Register your models here.
from hr.models import *

admin.site.register(Reports) 
admin.site.register(Advancehr)
admin.site.register(Resume)
admin.site.register(Define_User)