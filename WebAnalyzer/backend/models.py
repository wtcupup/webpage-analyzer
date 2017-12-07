from django.db import models

# Create your models here.


class WebsiteList(models.Model):
    name = models.TextField(default='Basic')


class Website(models.Model):
    list = models.ForeignKey(WebsiteList)
    url = models.TextField(max_length=200)
    was_searched = models.BooleanField(default=True)
    count = models.PositiveIntegerField(default=0)


