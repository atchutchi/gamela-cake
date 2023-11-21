from django.db import models
from django.utils import timezone
from django.conf import settings
from cloudinary.models import CloudinaryField
from datetime import timedelta


# Stores user authentication and profile information.
class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    def __str__(self):
        return self.username


# Represents a cake available for reservation or purchase.
class Cake(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = CloudinaryField('image', default='placeholder')

    def __str__(self):
        return self.name


# Represents an order made by a user. Associates the user with a specific cake.
class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    cake = models.ForeignKey(
        Cake,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Order {self.id} for {self.user.username}"


# Used to store contact messages sent by users through the website.
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"


# Represents a cake reservation made by a user. Stores details
class Reservation(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    cake = models.ForeignKey(
        Cake,
        on_delete=models.CASCADE
    )
    datetime = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    order = models.OneToOneField(
        Order,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reservation'
    )

    def __str__(self):
        return f"Reservation for {self.cake.name} by {self.user.username}"

    # define whether the reservation can be canceled based on the 24-hour rule
    def can_cancel(self):
        return timezone.now() <= self.datetime - timedelta(hours=24)
