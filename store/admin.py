from django.contrib import admin
from django.db.models import F

from .models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'nic', 'telephone', 'role_status']
    search_fields = ['id', 'fistname', 'lastname', 'nic']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'payment_method', 'telephone', 'total', 'order_status']
    search_fields = ['id', 'customer__username', 'telephone']


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    pass


class DepletedStockFilter(admin.SimpleListFilter):
    title = 'Depleted Stocks'

    parameter_name = 'material_available_unit'

    def lookups(self, request, model_admin):
        return [
            ('depleted', 'Depleted stocks'),
        ]

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        if self.value() == 'depleted':
            return queryset.filter(available_unit__lte=F('warning_limit'))


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'unit_price', 'available_stock', 'warning_limit']
    search_fields = ['id', 'name']
    list_filter = [DepletedStockFilter]


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    # suppliers only
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "supplier":
            kwargs["queryset"] = User.objects.filter(role='2')
        return super(StockAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(ServiceMaterial)
class ServiceMaterialAdmin(admin.ModelAdmin):
    pass
