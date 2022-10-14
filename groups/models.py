from django.db import models

# Create your models here.


class Group(models.Model):
    name = models.CharField(max_length=20, unique=True)
    scientific_name = models.CharField(
        max_length=20, unique=True
    )

    ...
