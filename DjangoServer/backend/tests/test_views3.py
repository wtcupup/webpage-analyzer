from django.test import TestCase
# from django.core.urlresolvers import reverse
# from backend.models import Website, WebsiteList
# from backend.views import delete_url_view


#test homepage
class HomepageTests(TestCase):

    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

#test delete_url_view
# def test_website_delete_url_view
#     list=WebsiteList.objects.create(name="aName")
#     url="http://www.disney.com",
#     was_searched=True
#     count=0
#     w=Website.objects.create(list=list, url=url, was_searched=was_searched, count=count)