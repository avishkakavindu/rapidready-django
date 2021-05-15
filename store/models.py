from decimal import Decimal

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db.models import F
from django.utils.html import format_html
from datetime import datetime


class User(AbstractUser):
    """ User model """
    email = models.EmailField(unique=True)
    nic = models.CharField(max_length=10)
    street = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=10)
    telephone = models.CharField(max_length=12)
    profile_pic = models.ImageField(upload_to='images/user', default="images/user/default.jpg")

    def __str__(self):
        return self.username

    def role_status(self):
        """ Icon based role representation on admin panel"""
        if self.groups.filter(name='supplier').exists():
            return format_html(
                '<span style=""><i class="fa fa-truck mr" aria-hidden="true"></i></span>Supplier'
            )
        elif self.groups.filter(name='production manager').exists():
            return format_html(
                '<span style=""><i class="fa fa-user-circle-o mr" aria-hidden="true"></i></span>Production Manager'
            )
        elif self.groups.filter(name='store manager').exists():
            return format_html(
                '<span style=""><i class="fa fa-user-circle-o mr" aria-hidden="true"></i></span>Store Manager'
            )
        elif self.groups.filter(name='production team').exists():
            return format_html(
                '<span style=""><i class="fa fa-user-o mr" aria-hidden="true"></i></span>Production Teams'
            )
        elif self.groups.filter(name='store team').exists():
            return format_html(
                '<span style=""><i class="fa fa-user-o mr" aria-hidden="true"></i></span>Store Teams'
            )
        else:
            if self.is_superuser:
                return format_html(
                    '<span style=""><i class="fa fa-universal-access mr" aria-hidden="true"></i></span>{}'.format(
                        'Admin')
                )
            return 'Customer'


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
    street = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=10)
    status = models.PositiveSmallIntegerField(choices=ORDER_STATUS, default=PENDING)
    created_on = models.DateTimeField(default=datetime.now())
    
    def __str__(self):
        return '{}'.format(self.id)

    @property
    def get_total(self):
        ordereditems = OrderedService.objects.filter(order=self)
        return '$ {:.2f}'.format(
            sum(
                [item.get_sale_price for item in ordereditems]
            )
        )
    get_total.fget.short_description = 'Total Amount Paid'

    @property
    def order_type(self):
        if self.status == self.PENDING:
            if self.type == self.PREDEFINED:
                return format_html(
                    '{}'.format(
                        self.get_type_display())
                )
            else:
                return format_html(
                    '<span style=""><i class="fa fa-bell mr order-type" aria-hidden="true"></i></span>{}'.format(
                        self.get_type_display())
                )

        return self.get_type_display()

    @property
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


class Category(models.Model):
    """ Service category model """

    class Meta:
        verbose_name = "Categorie"

    category = models.CharField(max_length=255)

    def __str__(self):
        return '{}'.format(self.category)


class Service(models.Model):
    """ RapidReady services model """

    service = models.CharField(max_length=255)
    desc = models.TextField()
    image = models.ImageField(upload_to='images/service', default='images/service/default.jpg')
    category = models.ForeignKey(Category, null=False, on_delete=models.DO_NOTHING)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=4, decimal_places=2,
                                   validators=[MaxValueValidator(100), MinValueValidator(0)])

    def __str__(self):
        return '{}'.format(self.service)

    @property
    def actual_price(self):
        """ Get sale price """
        return '$ {:.2f}'.format(self.price - self.price * (self.discount / 100))

    @property
    def average_rating(self):
        """ Get average rating for service """
        if self.rating_count == 0:
            return '0'
        return '{:.1f}'.format(sum([_.rating for _ in self.review_set.all()]) / self.rating_count)

    @property
    def rating_count(self):
        """ Get total count of rating """
        return len(self.review_set.all())


class OrderedService(models.Model):
    """ Ordered services and the quantities model """

    order = models.ForeignKey(Order, null=False, on_delete=models.CASCADE, related_name='orderedservice_set')
    service = models.ForeignKey(Service, null=False, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField()
    discount = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0),
                    MaxValueValidator(100)]
    )
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return '{}'.format(self.service)

    @property
    def get_sale_price(self):
        return self.unit_price * self.quantity * ((100 - self.discount) /100)

    @property
    def get_price_for_ordered_batch(self):
        return '$ {:.2f}'.format(self.get_sale_price)

    @property
    def actual_price(self):
        """ Get sale price """
        return '$ {:.2f}'.format(self.unit_price - self.unit_price * (self.discount / 100))


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
    quantity = models.DecimalField(max_digits=5, decimal_places=2,
                                   validators=[MinValueValidator(0), MaxValueValidator(999)],
                                   help_text='Material needed for one unit. Ex: 1 business card 1/20 of 14pt business '
                                             'card stock paper')

    def __str__(self):
        return '{}'.format(self.material)


class Review(models.Model):
    """ Review model """

    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE, related_name='review_set')
    service = models.ForeignKey(Service, null=False, on_delete=models.CASCADE)
    review = models.TextField(null=True, blank=True)
    rating = models.DecimalField(
        max_digits=1,
        decimal_places=0,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    created_on = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return '{} - {} - {}'.format(self.user, self.review, self.service)


class Cart(models.Model):
    """ Cart model """

    user = models.ForeignKey(User, null=False, on_delete=models.DO_NOTHING, related_name="cart_set")
    created_on = models.DateTimeField(default=datetime.now())
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return '{} - {}'.format(self.id, self.user)


class CartItem(models.Model):
    """ Cart items model """

    cart = models.ForeignKey(Cart, null=False, on_delete=models.CASCADE, related_name='cartitem_set')
    service = models.ForeignKey(Service, null=False, on_delete=models.DO_NOTHING, related_name='cartservice_set')
    quantity = models.DecimalField(max_digits=10, decimal_places=0, validators=[MinValueValidator(1)], default=1)
    is_removed = models.BooleanField(default=False)

    def __str__(self):
        return '{}'.format(self.id)

    @property
    def get_total_for_item(self):
        return '$ {:.2f}'.format(Decimal(self.service.actual_price.strip('$')) * self.quantity)


class Quote(models.Model):
    """ Quote model """

    customer = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    order = models.OneToOneField(Order, null=True, blank=True, on_delete=models.CASCADE)
    desc = models.TextField(null=False)
    is_possible = models.BooleanField(default=False)
    order_desc = models.TextField(null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], null=True, blank=True)

    def __str__(self):
        return '{} - {}'.format(self.id, self.customer)
    