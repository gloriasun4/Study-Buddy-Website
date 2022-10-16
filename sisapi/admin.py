from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Instructor)
admin.site.register(Section)
admin.site.register(Meeting)
