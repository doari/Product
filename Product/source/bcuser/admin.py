from django.contrib import admin
from .models import Bcuser

class BcuserAdmin(admin.ModelAdmin):
    list_display=('email',)

admin.site.register(Bcuser, BcuserAdmin)  

