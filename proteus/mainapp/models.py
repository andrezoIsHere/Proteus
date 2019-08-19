from django.db import models

# Create your models here.

class siteUsers(models.Model):

    login = models.CharField(unique=True, max_length = 100)
    email = models.CharField(max_length = 150)
    password = models.CharField(max_length = 200)

    def __str__(self):
        return self.login

class rssPosts(models.Model):

    token = models.TextField(unique=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
