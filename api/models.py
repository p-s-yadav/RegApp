from django.db import models

# Create your models here.
class BizData(models.Model):
    series_reference = models.CharField(max_length=50)
    period = models.CharField(max_length=50)
    data_value = models.CharField(max_length=50)
    status = models.CharField(max_length=1)
    units = models.CharField(max_length=50)
    magnitude = models.CharField(max_length=50)
    subject = models.CharField(max_length=50)
    group = models.CharField(max_length=100)
