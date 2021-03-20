from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.utils.html import format_html


class User(AbstractUser):
    """ User model """

    # user roles
    CUSTOMER = 1
    SUPPLIER = 2
    PRODUCTION_MANAGER = 3
    PRODUCTION_TEAM = 4
    STORE_MANAGER = 5
    STORE_TEAM = 6

    ROLE_CHOICES = [
        (CUSTOMER, 'Customer'),
        (SUPPLIER, 'Supplier'),
        (PRODUCTION_MANAGER, 'Production Manager'),
        (PRODUCTION_TEAM, 'Production Team'),
        (STORE_MANAGER, 'Store Manager'),
        (STORE_TEAM, 'Store Team'),

    ]

    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, null=True, blank=True)
    nic = models.CharField(max_length=10)
    address = models.TextField()
    telephone = models.CharField(max_length=12)
    profile_pic = models.ImageField(upload_to='images/user', default="images/user/default.jpg")

    def role_status(self):
        if self.role == 1:
            return 'Customer'
        if self.role == 2:
            return format_html(
                '<span style=""><i class="fa fa-truck mr" aria-hidden="true"></i></span>{}'.format(
                    self.get_role_display())
            )
        elif self.role == 3 or self.role == 5:
            return format_html(
                '<span style=""><i class="fa fa-user-circle-o mr" aria-hidden="true"></i></span>{}'.format(
                    self.get_role_display())
            )
        elif self.role == 4 or self.role == 6:
            return format_html(
                '<span style=""><i class="fa fa-user-o mr" aria-hidden="true"></i></span>{}'.format(
                    self.get_role_display())
            )
        else:
            return format_html(
                '<span style=""><i class="fa fa-universal-access mr" aria-hidden="true"></i></span>{}'.format('Admin')
            )


class Order(models.Model):
    """ Orders model """
    # order types
    PREDEFINED = 1
    CUSTOM = 2

    ORDER_TYPES = [
        (PREDEFINED, 'Predefined Order'),
        (CUSTOM, 'Custom Order')
    ]

    # payment methods
    PAYHERE = 1
    CASHONDELIVERY = 2

    PAYMENT_METHOD = [
        (PAYHERE, 'Payhere'),
        (CASHONDELIVERY, 'Cash on delivery'),
    ]

    # order status
    PENDING = 1
    PROCESSING = 2
    DELIVERED = 3
    CANCELED = 4

    ORDER_STATUS = [
        (PENDING, 'Pending'),
        (PROCESSING, 'Processing'),
        (DELIVERED, 'Delivered'),
        (CANCELED, 'Canceled')
    ]

    customer = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    desc = models.TextField()
    payment_method = models.PositiveSmallIntegerField(choices=PAYMENT_METHOD, null=True, blank=True)
    type = models.PositiveSmallIntegerField(choices=ORDER_TYPES, default=PREDEFINED)
    telephone = models.CharField(max_length=12)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.PositiveSmallIntegerField(choices=ORDER_STATUS, default=PENDING)

    def __str__(self):
        return '{}'.format(self.id)

    def order_type(self):
        if self.status == self.PENDING:
            if self.type == self.PREDEFINED:
                return format_html(
                    '<span style=""><i class="fa fa-bell-o mr order-type" aria-hidden="true"></i></span>{}'.format(
                        self.get_type_display())
                )
            else:
                return format_html(
                    '<span style=""><i class="fa fa-bell mr order-type" aria-hidden="true"></i></span>{}'.format(
                        self.get_type_display())
                )

        return self.get_type_display()

    def order_status(self):
        if self.status == 1:
            return format_html(
                '<span style=""><i class="fa fa-clock-o pending mr" aria-hidden="true"></i></span>{}'.format(
                    self.get_status_display())
            )
        elif self.status == 2:
            return format_html(
                '<span style=""><i class="fa fa-cogs processing mr" aria-hidden="true"></i></span>{}'.format(
                    self.get_status_display())
            )
        elif self.status == 3:
            return format_html(
                '<span style=""><i class="fa fa-truck delivered mr" aria-hidden="true"></i></span>{}'.format(
                    self.get_status_display())
            )
        else:
            return format_html(
                '<span style=""><i class="fa fa-ban canceled mr" aria-hidden="true"></i></span>{}'.format(
                    self.get_status_display())
            )


class Service(models.Model):
    """ RapidReady services model """

    service = models.CharField(max_length=255)
    desc = models.TextField()
    image = models.ImageField(upload_to='images/service', default='images/service/default.jpg')
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return '{}'.format(self.service)


class OrderedService(models.Model):
    """ Ordered services and the quantities model """

    order = models.ForeignKey(Order, null=False, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, null=False, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField()

    def __str__(self):
        return '{}'.format(self.service)


class Material(models.Model):
    """ Total available materials model"""

    name = models.TextField(max_length=255)
    available_unit = models.PositiveIntegerField()
    warning_limit = models.PositiveIntegerField()

    def __str__(self):
        return '{}'.format(self.name)

    def available_stock(self):
        if self.available_unit < self.warning_limit:
            return format_html(
                '<span class="msg">{}<i class ="fa fa-exclamation-triangle ml canceled" aria-hidden="true" > '
                'Running low on stock</i></span>'.format(self.available_unit)
            )
        return self.available_unit


class Stock(models.Model):
    """ Bought stocks from suppliers model """

    stock = models.CharField(max_length=255)
    supplier = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, null=False, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    review = models.TextField(null=True, blank=True)
    rating = models.DecimalField(
        max_digits=1,
        decimal_places=0,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )

    def __str__(self):
        return '{}'.format(self.stock)


class ServiceMaterial(models.Model):
    """ Materials required by each service model """

    service = models.ForeignKey(Service, null=True, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, null=False, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return '{}'.format(self.material)


class Review(models.Model):
    """ Review model """

    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, null=False, on_delete=models.CASCADE)
    review = models.TextField(null=True, blank=True)
    rating = models.DecimalField(
        max_digits=1,
        decimal_places=0,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )

    def __str__(self):
        return'{}-{}-{}'.format(self.user, self.review, self.service)
