from django.db import models

# Create your models here.
class Todo(models.Model):
     name = models.CharField(max_length=100, blank=False, null=False, default="")
     completed = models.BooleanField(default=False, blank=False, null=False)
     description = models.TextField(default="", blank=False, null=False)
     priority = models.IntegerField(default=0, blank=False, null=False)