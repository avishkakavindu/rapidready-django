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
                '<span style=""><i class="fa fa-truck mr" aria-hidden="true"></i></span>{}'.format(self.get_role_display())
            )
        elif self.role == 3 or self.role == 5:
            return format_html(
                '<span style=""><i class="fa fa-user-circle-o mr" aria-hidden="true"></i></span>{}'.format(self.get_role_display())
            )
        elif self.role == 4 or self.role == 6:
            return format_html(
                '<span style=""><i class="fa fa-user-o mr" aria-hidden="true"></i></span>{}'.format(self.get_role_display())
            )
        else:
            return format_html(
                '<span style=""><i class="fa fa-universal-access mr" aria-hidden="true"></i></span>{}'.format('Admin')
            )


class Order(models.Model):
    """ Order model """

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
    telephone = models.CharField(max_length=12)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.PositiveSmallIntegerField(choices=ORDER_STATUS, default='1')

    def __str__(self):
        return '{}-{}'.format(self.id, self.customer)

    def order_status(self):
        if self.status == 1:
            return format_html(
                '<span style=""><i class="fa fa-clock-o pending mr" aria-hidden="true"></i></span>{}'.format(self.get_status_display())
            )
        elif self.status == 2:
            return format_html(
                '<span style=""><i class="fa fa-cogs processing mr" aria-hidden="true"></i></span>{}'.format(self.get_status_display())
            )
        elif self.status == 3:
            return format_html(
                '<span style=""><i class="fa fa-truck delivered mr" aria-hidden="true"></i></span>{}'.format(self.get_status_display())
            )
        else:
            return format_html(
                '<span style=""><i class="fa fa-ban canceled mr" aria-hidden="true"></i></span>{}'.format(self.get_status_display())
            )

