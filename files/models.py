from django.db import models
from django.contrib.auth.models import User

class Projects(models.Model):
    name = models.CharField(max_length=500)
    users = models.ManyToManyField(User, related_name='project')

class Document(models.Model):
    def __str__(self):
        return self.filename + ' ' + self.md5sum

    filename = models.CharField(max_length=500)
    type = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now=True)
    uploader = models.CharField(max_length=30)
    md5sum = models.CharField(max_length=32)
    filesize = models.CharField(max_length=20)
    projects = models.ManyToManyField(Projects)


class Contact(models.Model):
    def __str__(self):
        return self.name

    name = models.CharField(max_length=1000)
    email = models.EmailField(max_length=1000)
    text = models.CharField(max_length=5000)
    date = models.DateTimeField(auto_now=True)
