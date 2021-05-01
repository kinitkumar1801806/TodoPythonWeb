from django.db import models
from django.contrib.auth.models import User

class Customers(models.Model):
    customer=models.OneToOneField(User,unique=True,on_delete=models.CASCADE)

class Moderators(models.Model):
    moderator=models.OneToOneField(User,unique=True,on_delete=models.CASCADE)

# Create your models here.
class Todos(models.Model):
    Customer=models.CharField(max_length=30)
    Moderators=models.CharField(max_length=30)
    title=models.CharField(max_length=50)
    description=models.TextField()
    Status=models.BooleanField(default=False)
