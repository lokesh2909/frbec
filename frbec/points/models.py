from django.db import models
from django.utils.timezone import now

# Create your models here.
class Transactions(models.Model):
    payer = models.CharField(max_length=30)   
    points = models.IntegerField()
    timestamp = models.DateTimeField(default=now())