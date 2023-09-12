from django.db import models


# Create your models here.
class Tag(models.Model):
    date = models.DateField()
    UUID = models.IntegerField()
    ImageID = models.IntegerField()
    AnimalID = models.IntegerField()
