from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.utils.html import format_html


class User(AbstractUser):
    """ User model """
    email = models.EmailField(unique=True)
    nic = models.CharField(max_length=10)
    address = models.TextField()
    telephone = models.CharField(max_length=12)
    profile_pic = models.ImageField(upload_to='images/user', default="images/user/default.jpg")

    def role_status(self):
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


class Category(models.Model):
    """ Service category model """

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
        return self.price + self.price * (self.discount / 100)

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

    def __str__(self):
        return '{}-{}-{}'.format(self.user, self.review, self.service)
