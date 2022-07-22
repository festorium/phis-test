from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Microservice)
admin.site.register(Menu)
admin.site.register(Submenu)

admin.site.register(PhisUser)

# admin.site.register(Role)
# admin.site.register(Criteria)
