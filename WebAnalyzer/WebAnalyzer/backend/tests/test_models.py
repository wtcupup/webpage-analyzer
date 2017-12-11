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
        self.assertEqual(w.name, "someName") #check name is assigned correctly
    def create_default_websitelist(self):
        return WebsiteList.objects.create()
    def test_default_websitelist_creation(self):
        w=self.create_default_websitelist()
        self.assertTrue(isinstance(w, WebsiteList))
        self.assertEqual(w.name, "Basic") #check name is set to default correctly

class WebsiteTest(TestCase):
    def create_website(self, list=WebsiteList.objects.create(name="aName"), url= "http://www.disney.com",
                       was_searched=False,count=5):
        return Website.objects.create(list=list, url=url, was_searched=was_searched, count=count)
    def test_website_creation(self):
        w = self.create_website()
        self.assertTrue(isinstance(w, Website))
        self.assertEqual(w.url, "http://www.disney.com")
        self.assertEqual(False, w.was_searched)
        self.assertEqual(5, w.count)
        self.assertEqual(w.list.name, "aName") #check name of WebsiteList is unchanged
    def create_default_website(self, list=WebsiteList.objects.create(), url= "http://www.disney.com"):
        return Website.objects.create(list=list, url=url)
    def test_default_website_creation(self):
        w = self.create_default_website()
        self.assertTrue(isinstance(w, Website))
        self.assertEqual(w.url, "http://www.disney.com")  #check that url is correct
        self.assertEqual(True, w.was_searched) #check that was_searched is True by default
        self.assertEqual(0, w.count) #check that count is 0 by default
        self.assertEqual(w.list.name, "Basic") #check name of WebsiteList is unchanged



