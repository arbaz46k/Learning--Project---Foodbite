from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    hotel_image = models.ImageField(upload_to="images/restaurant",default='https://cdn2.vectorstock.com/i/1000x1000/34/96/flat-busness-man-user-profile-avatar-in-suit-vector-4333496.jpg')
    is_restaurant = models.BooleanField(default=False)

  


class Dishes(models.Model):
    restaurant = models.ForeignKey("User",on_delete=models.CASCADE, related_name="dishes")
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=526)
    image = models.ImageField(upload_to="images/dishes")
    price = models.FloatField()

    def __str__(self):
        return f"dish:{self.name}, price:{self.price}"

    def serialize(self):
        return{
            "restaurant" : self.restaurant,
            "name" : self.name,
            "description" : self.description,
            "image" : self.image,
            "price" : self.price
        }

class Order(models.Model):
    restaurant = models.ForeignKey("User", on_delete=models.CASCADE, related_name='orders')
    customer = models.ForeignKey("User", on_delete=models.CASCADE, related_name="ordered")
    address = models.CharField(max_length=512)
    contact = models.CharField(max_length=13)
    total_bill = models.FloatField(default=10)
    timestamp = models.TimeField(auto_now_add=True)
    delivered = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.customer} has ordered from {self.restaurant}"

class Ordered_dishes(models.Model):
    quantity = models.PositiveIntegerField(default=1)
    dish = models.ForeignKey('Dishes', on_delete=models.CASCADE)
    order = models.ForeignKey('Order', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.dish} {self.quantity} units"
    