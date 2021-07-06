from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models import F
from django.contrib import messages

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
            'street',
            'city',
            'state',
            'zipcode',
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
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """ Orders admin """

    list_display = ['id', 'customer', 'payment_method', 'telephone', 'get_total', 'order_type', 'order_status']
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

    def save_model(self, request, obj, form, change):
        """ update the stock upon order status change to processing """

        pre_status = Order.objects.get(id=obj.id).status
        super().save_model(request, obj, form, change)

        if obj.status == obj.PROCESSING and (pre_status == obj.PENDING or pre_status == obj.CANCELED):
            orderedservices = obj.orderedservice_set.all()
            can_fulfill = True
            for orderedservice in orderedservices:
                materials = orderedservice.service.servicematerial_set.all()    # materials required for a service
                for material in materials:
                    for mat in materials:
                        """ checks if materials are available in required quantities """
                        req_for_order = mat.quantity * orderedservice.quantity
                        if mat.material.available_unit < req_for_order:
                            can_fulfill = False
                            break
                    if can_fulfill:
                        req_for_order = material.quantity * orderedservice.quantity
                        material.material.available_unit -= req_for_order
                        material.material.save()
                    else:
                        break
            if can_fulfill:
                messages.success(request, "Material stocks updated!")
            else:
                obj.status = pre_status
                obj.save()
                messages.error(request, "Required materials are NOT SUFFICIENT!")

        elif obj.status == obj.CANCELED:
            if pre_status != obj.PENDING:
                orderedservices = obj.orderedservice_set.all()
                for orderedservice in orderedservices:
                    materials = orderedservice.service.servicematerial_set.all()  # materials required for a service
                    for material in materials:
                        req_for_order = material.quantity * orderedservice.quantity
                        material.material.available_unit += req_for_order
                        material.material.save()

            messages.error(request, "Order canceled!")


class ServiceCategoryInline(admin.StackedInline):
    """ Inline views of Services belongs to the category """
    model = Service
    extra = 0

    def has_change_permission(self, request, obj=None):
        """ read only """
        return False


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """ Service categories  """
    list_display = ['id', 'category']
    inlines = [ServiceCategoryInline]


class ServiceMaterialInline(admin.StackedInline):
    """ Inline views of services and its materials"""
    model = ServiceMaterial
    extra = 0


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    """ Services admin - available services """
    list_display = ['id', 'service', 'desc', 'price', 'discount', 'category']
    search_fields = ['id', 'service', 'category']
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
    extra = 0
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
    list_display = ['id', 'user', 'service', 'review', 'rating']
    search_fields = ['id', 'user']
    list_filter = ['rating']


class CartItemInline(admin.StackedInline):
    """ Inline views of cart items belongs to a cart """
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_on']
    search_fields = ['id', 'user', 'created_on']
    inlines = [CartItemInline]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart', 'service', 'quantity']
    search_field = ['id', 'cart', 'service']
    list_filter = ['service']


@admin.register(Quote)
class Quotes(admin.ModelAdmin):
    list_display = ['id', 'customer', 'order', 'total']
    search_fields = ['id', 'customer', 'order']

    def render_change_form(self, request, context, *args, **kwargs):
        form_instance = context['adminform'].form
        form_instance.fields['order_desc'].widget.attrs['placeholder'] = 'Describe the services want by the customer'
        return super().render_change_form(request, context, *args, **kwargs)
