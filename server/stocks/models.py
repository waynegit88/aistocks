from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    stocks = models.TextField(default="")
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "User"
        verbose_name_plural = "Users"
'''
class Stocklist(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=20, unique=True)
    area = models.CharField(max_length=50)
    industry = models.CharField(max_length=50)
    market = models.CharField(max_length=10)
    list_date = models.CharField(max_length=10)
    update_date = models.DateTimeField(null=True)
'''

class Datastatus(models.Model):
    update_date = models.DateField(null=True)
