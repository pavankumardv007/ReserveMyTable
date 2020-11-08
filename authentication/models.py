from django.db import models
import webapp.models
from django.contrib.auth.models import User

# Create your models here.

# Representing guest to a restaurant 
class Guest(models.Model) :
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)

    def __str__(self):
        return self.user.username


# Representing manager to a restaurant 
class Manager(models.Model) :
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    restaurant = models.ForeignKey("webapp.Restaurant",on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username