from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models import F

from .models import *

SUPPLIER = 2


class SupplierStockInline(admin.StackedInline):
    """ Inline views of stocks on user, based on role supplier """
    model = Stock
    extra = 0


@admin.register(User)
class UserAdmin(UserAdmin):
    """ user admin """

    fieldsets = [
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': (
            'first_name',
            'last_name',
            'email',
            'nic',
            'address',
            'telephone',
            'profile_pic',
        )}),
        ('Permissions', {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
        )}),
        ('Important dates', {'fields': ('last_login', 'date_joined')})
    ]

    list_display = ['id', 'username', 'first_name', 'last_name', 'nic', 'telephone', 'role_status', 'is_active']
    search_fields = ['id', 'username', 'fist_name', 'last_name', 'nic']
    inlines = []

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.inlines = []

        try:
            obj = self.model.objects.get(pk=object_id)
        except self.model.DoesNotExist:
            pass
        else:
            if obj.groups.filter(name='supplier').exists():
                self.inlines = [SupplierStockInline,]
        return super(UserAdmin, self).change_view(request, object_id, form_url, extra_context)


class OrderedServiceInline(admin.StackedInline):
    """ Inline views of ordered services """
    model = OrderedService
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """ Orders admin """

    list_display = ['id', 'customer', 'payment_method', 'telephone', 'total', 'order_type', 'order_status']
    search_fields = ['id', 'customer__username', 'telephone']
    list_filter = ['type', 'status', 'payment_method']
    ordering = ['status']
    inlines = [OrderedServiceInline]

    # field level access read_only_fields
    production_team_read_only = [  # for production team
        'customer',
        'desc',
        'payment_method',
        'type',
        'telephone',
        'total'
    ]

    def get_readonly_fields(self, request, obj=None):
        """ Production team can only change order - status """
        if request.user.groups.filter(name='production team').exists():
            return self.production_team_read_only
        return super(OrderAdmin, self).get_readonly_fields(request, obj=obj)


class ServiceMaterialInline(admin.StackedInline):
    """ Inline views of services and its materials"""
    model = ServiceMaterial


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """ Services admin - available services """
    list_display = ['id', 'service', 'desc', 'price', 'discount']
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


class MaterialStockInline(admin.StackedInline):
    """ Inline views of Stocks belongs to Materials """
    model = Stock
    extra = 1
    readonly_fields = ['stock', 'supplier', 'material', 'quantity', 'unit_price']


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    """ Materials admin - contains the materials and available units """

    list_display = ['id', 'name', 'available_stock', 'warning_limit']
    search_fields = ['id', 'name']
    list_filter = [DepletedStockFilter, 'name']
    inlines = [MaterialStockInline]

    # field level access read_only_fields
    store_team_read_only = [  # for production team
        'name',
        'available_unit',
        'warning_limit'
    ]

    def get_readonly_fields(self, request, obj=None):
        """ Store team can only change Stock - review and rating """
        if request.user.groups.filter(name='store team').exists():
            return self.store_team_read_only
        return super(MaterialAdmin, self).get_readonly_fields(request, obj=obj)


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    """ Stock admin - stocks by suppliers """

    list_display = ['id', 'stock', 'supplier', 'material', 'quantity']
    search_fields = ['id', 'stock', 'supplier', 'material']
    list_filter = ['material', 'supplier']

    # field level access read_only_fields
    store_team_read_only = [  # for production team
        'stock',
        'supplier',
        'material',
        'quantity',
        'unit_price',
    ]

    # suppliers only
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "supplier":
            kwargs["queryset"] = User.objects.filter(groups__name='supplier')
        return super(StockAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        """ Store team can only change Stock - review and rating """
        if request.user.groups.filter(name='store team').exists():
            return self.store_team_read_only
        return super(StockAdmin, self).get_readonly_fields(request, obj=obj)

    def get_queryset(self, request):
        """ role based querying for supplier """
        queryset = super().get_queryset(request)
        # if the user isn't a supplier
        if not request.user.groups.filter(name='supplier'):
            return queryset
        return queryset.filter(supplier=request.user)


@admin.register(ServiceMaterial)
class ServiceMaterialAdmin(admin.ModelAdmin):
    """ Service material admin - materials required by each service|
     pivot table of service and material  """

    list_display = ['id', 'service', 'material', 'quantity']
    search_fields = ['id', 'service', 'material']
    list_filter = ['material', 'service']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'review', 'rating']
    search_fields = ['id', 'user']
    list_filter = ['rating']
