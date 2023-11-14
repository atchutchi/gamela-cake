from django.db import models
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Custom User model extending the default Django User
class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Add any additional fields here
    # String representation of the User model
    def __str__(self):
        return self.username

# Cake model to store cake details
class Cake(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = CloudinaryField('image', default='placeholder')  # This will use Cloudinary for image storage

    # String representation of the Cake model
    def __str__(self):
        return self.name

# Reservation model to store booking details
class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    SIZE_CHOICES = [
        ('S', 'Small - 1 layer x 24cm'),
        ('M', 'Medium - 2 layers x 20cm'),
        ('L', 'Large - 3 layers x 20cm'),
        ('XL', 'Extra Large - 3 layers x 24cm'),
    ]

    BATTER_CHOICES = [
        ('N', 'Nuts'),
        ('V', 'Vanilla'),
        ('B', 'Buttery'),
        ('R', 'Red Velvet'),
    ]

    FILLING_CHOICES = [
        ('BR', 'Brigadier'),
        ('BW', 'Brigadeiro with walnuts'),
        ('FM', '4 Milk'),
        ('RF', 'Red fruits'),
        ('CC', 'Coconut'),
        ('MC', 'Milk cream'),
    ]

    size = models.CharField(max_length=2, choices=SIZE_CHOICES, default='S')
    batter = models.CharField(max_length=1, choices=BATTER_CHOICES, default='N')
    filling = models.CharField(max_length=2, choices=FILLING_CHOICES, default='BR')
    special_request = models.TextField(blank=True, null=True)

    # String representation of the Reservation model
    def __str__(self):
        return f"Reservation for {self.user.username} on {self.datetime}"

# Order model to store order details associated with a reservation
class Order(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    cake = models.ForeignKey(Cake, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    # String representation of the Order model
    def __str__(self):
        return f"Order {self.id} for {self.reservation}"

