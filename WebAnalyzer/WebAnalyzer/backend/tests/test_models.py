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

	def create_website(self, list= "fill in", url= "http://www.disney.com", was_searched=True,count=0):
		return Website.objects.create(list=list, url=url, was_searched=was_searched, count=count)

    # test if url is as expected
    def test_website_creation(self):
         w = self.create_website()
         self.assertTrue(isinstance(w, Website))
         self.assertEqual(w.__unicode__(), w.url) #do we need to use reverse for this url?

