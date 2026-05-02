from django.db import models
from django.contrib.auth.models import User


class ChargingStation(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    address = models.TextField()
    charger_type = models.CharField(
        max_length=20,
        choices=[("Fast", "Fast"), ("Normal", "Normal")]
    )
    is_active = models.BooleanField(default=True) 

    def __str__(self):
        return self.name



class Booking(models.Model):
    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("CONFIRMED", "Confirmed"),
        ("CANCELLED", "Cancelled"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    station = models.ForeignKey(ChargingStation, on_delete=models.CASCADE)
    date = models.DateField()
    time_slot = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")

    created_at = models.DateTimeField(auto_now_add=True)


class LoginHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)
    ip_address = models.CharField(max_length=45)

    def __str__(self):
        return self.user.username