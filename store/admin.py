from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models import F

from .models import *

SUPPLIER = 1


class SupplierStockInline(admin.StackedInline):
    """ Inline views of stocks on user based on role supplier """
    model = Stock
    extra = 1


@admin.register(User)
class UserAdmin(UserAdmin):
    """ user admin """

    list_display = ['id', 'username', 'first_name', 'last_name', 'nic', 'telephone', 'role_status']
    search_fields = ['id','username', 'fistname', 'lastname', 'nic']
    inlines = []

    def get_inlines(self, request, obj):
        if obj.role == SUPPLIER:
            return [SupplierStockInline]
        return []


class OrderedServiceInline(admin.StackedInline):
    """ Inline views of ordered services """
    model = OrderedService
    extra = 1

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """ Orders admin """

    list_display = ['id', 'customer', 'payment_method', 'telephone', 'total', 'order_type', 'order_status']
    search_fields = ['id', 'customer__username', 'telephone']
    list_filter = ['type', 'status', 'payment_method']
    ordering = ['status']
    inlines = [OrderedServiceInline]


class ServiceMaterialInline(admin.StackedInline):
    """ Inline views of services and its materials"""
    model = ServiceMaterial


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """ Services admin - available services """
    list_display = ['id', 'service', 'desc', 'price']
    search_fields = ['id', 'service']
    inlines = [ServiceMaterialInline]


@admin.register(OrderedService)
class OrderedServiceAdmin(admin.ModelAdmin):
    """ Ordered services admin - pivot table of order and services """

    list_display = ['id', 'order', 'service', 'quantity']
    search_fields = ['id', 'order']
    list_filter = ['service']


class DepletedStockFilter(admin.SimpleListFilter):
    """ Filter to get depleted stocks """

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
    """ Materials admin - contains the materials and available units """

    list_display = ['id', 'name', 'available_stock', 'warning_limit']
    search_fields = ['id', 'name']
    list_filter = [DepletedStockFilter, 'name']


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    """ Stock admin - stocks by suppliers """

    list_display = ['id', 'stock', 'supplier', 'material', 'quantity']
    search_fields = ['id', 'stock', 'supplier', 'material']
    list_filter = ['material', 'supplier']

    # suppliers only
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "supplier":
            kwargs["queryset"] = User.objects.filter(role='2')
        return super(StockAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(ServiceMaterial)
class ServiceMaterialAdmin(admin.ModelAdmin):
    """ Service material admin - materials required by each service|
     pivot table of service and material  """

    list_display = ['id', 'service', 'material', 'quantity']
    search_fields = ['id', 'service', 'material']
    list_filter = ['material' , 'service']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'review', 'rating']
    search_fields = ['id', 'user']
    list_filter = ['rating']