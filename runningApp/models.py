from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Stop(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()

class Route(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.DO_NOTHING)
    route_name = models.CharField(max_length=100)
    route_description = models.CharField(max_length=500)
    approved = models.BooleanField(default=False)
    stops = models.ManyToManyField(Stop, through='RouteStop')
    distance = models.FloatField() # overall route length
    gradient_range = models.FloatField() #difference between max and min elevation

class RouteStop(models.Model):
    route_id = models.ForeignKey(Route, on_delete=models.CASCADE)
    stop_id = models.ForeignKey(Stop, on_delete=models.CASCADE)
    stop_order = models.IntegerField(default=0)

    class Meta:
        ordering = ['stop_order']
