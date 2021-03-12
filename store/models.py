from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
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



