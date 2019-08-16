from django.db import models

# Create your models here.

class Users(models.Model):
    login = models.CharField(max_length = 100)
    email = models.CharField(max_length = 150)
    password = models.CharField(max_length = 200)
    points = models.BigIntegerField()
    regDate = models.DateTimeField()

    def __str__(self):
        return self.login
 
