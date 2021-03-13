from django.contrib import admin
from .models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'nic', 'telephone', 'role_status']
    search_fields = ['id', 'fistname', 'lastname', 'nic']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = ['id', 'customer', 'payment_method', 'telephone', 'total', 'order_status']
    search_fields = ['id', 'customer__username', 'telephone']