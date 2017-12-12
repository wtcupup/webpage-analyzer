from django.test import TestCase

#views tests
#higher-level functional tests. not isolating views.
class HomepageTests(TestCase):
    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
class TonePageTest(TestCase):
    def test_homepage(self):
        response = self.client.get('/tone-analyzer')
        self.assertEqual(response.status_code, 200)