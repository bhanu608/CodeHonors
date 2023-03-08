from django.db import models

from myapp.views import problem

# Create your models here.
class Problem(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.TextField()
    input = models.TextField()
    output = models.TextField()
    testin = models.TextField(default='')
    testout = models.TextField(default='')