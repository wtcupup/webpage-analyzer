from django.db import models


class WebsiteList(models.Model):

    # identifier for each different user's list must be unique
    # when user signup functionality is created, variable will be set to user's username
    name = models.TextField(default='AllUsers')


class Website(models.Model):
    list = models.ForeignKey(WebsiteList)   # list that the site belongs to
    url = models.TextField(max_length=200)  # url of the site
    was_searched = models.BooleanField(default=True) # gives ability to hide sites from user's view if errors occur
    count = models.PositiveIntegerField(default=0) # stores word count for most recent search word for the url

