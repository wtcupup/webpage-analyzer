from django.test import TestCase
from backend.models import Website, WebsiteList
# from django.core.urlresolvers import reverse

"""
Use this website to help build tests:
https://realpython.com/blog/python/testing-in-django-part-1-best-practices-and-examples/
The website refers to this repo:
https://github.com/mjhea0/testing-in-django
"""


# models tests
class WebsiteListTest(TestCase):
    def create_websitelist(self, name= "someName"):
        return WebsiteList.objects.create(name=name)
    # test if name is as expected
    def test_websitelist_creation(self):
        w=self.create_websitelist()
        self.assertTrue(isinstance(w, WebsiteList))
        self.assertEqual(w.__unicode__(), w.name)

class WebsiteTest(TestCase):
    def create_website(self, list=WebsiteList.objects.create(name="aName"), url= "http://www.disney.com", was_searched=True,count=0):
        return Website.objects.create(list=list, url=url, was_searched=was_searched, count=count)
    def test_website_creation(self):
        w = self.create_website()
        self.assertTrue(isinstance(w, Website))
        self.assertEqual(w.__unicode__(), w.url)  #check that url is correct
        self.assertEqual(True, w.was_searched) #check that was_searched is True
        self.assertEqual(0, w.count) #check that count is 0
        self.assertEqual(w.list.name, "aName") #check name of WebsiteList is unchanged


# from backend.models import Whatever
# class WhateverTest(TestCase):
#
#     def create_whatever(self, title="only a test", body="yes, this is only a test"):
#         return Whatever.objects.create(title=title, body=body, created_at=timezone.now())
#
#     def test_whatever_creation(self):
#         w = self.create_whatever()
#         self.assertTrue(isinstance(w, Whatever))
#         self.assertEqual(w.__unicode__(), w.title)

