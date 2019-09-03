from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    USER_TYPE_CHOICES =(
        ('Agent', 'Agent'),
        ('User', 'User'),
    )
    user_type = models.CharField(choices=USER_TYPE_CHOICES, max_length=100, default='User')
    first_name = models.CharField(max_length=20, null=True, blank=True)
    last_name = models.CharField(max_length=20, null=True, blank=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    password = models.CharField(max_length=255)
    password2 = models.CharField(max_length=255)
    address = models.CharField(max_length=20, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username


class Post(models.Model):
    STATUS_CHOICES = (
        ('Picked', 'Picked'),
        ('Drop', 'On Progress'),
        ('Delivered', 'Delivered'),
    )
    status = models.CharField(choices=STATUS_CHOICES, max_length=100, null=True)
    description = models.CharField(max_length=500)
    preffered_location = models.CharField(max_length=150)
    delivery_location = models.CharField(max_length=150)
    owner = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)

    def __str__(self):
        return self.delivery_location





