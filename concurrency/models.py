from django.db import models


class MyModel(models.Model):
    my_field = models.CharField(max_length=10)
