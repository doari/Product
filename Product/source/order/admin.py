from django.contrib import admin
from .models import Order

class OrderAdmin(admin.ModelAdmin):
    list_display = ('bcuser', 'product')

admin.site.register(Order, OrderAdmin)

