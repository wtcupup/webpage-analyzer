from django.test import TestCase
from backend.views import main_view, tone_view, delete_url_view
from django.core.urlresolvers import reverse

# views (uses reverse)

def test_whatever_list_view(self):
    w = self.create_whatever()
    url = reverse("whatever.views.whatever")
    resp = self.client.get(url)
    self.assertEqual(resp.status_code, 200)
    self.assertIn(w.title, resp.content)