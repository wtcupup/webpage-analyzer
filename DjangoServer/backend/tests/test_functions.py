from django.test import TestCase
from backend.functions import get_tone_words_hashmap, get_current_sites, get_site_list



#functions tests
class GetToneWordsTest(TestCase):
    def create_hashmap(self):
        return get_tone_words_hashmap()
    def test_hashmap(self):
        map=self.create_hashmap()
        self.assertEqual(map, {'good': 0.5, 'better': 0.3, 'best': 0.9, 'excellent': 0.8, 'nice': 0.5,
                         'positive': 0.5, 'cool': 0.4, 'terrific': 0.8, 'fantastic': 0.8, 'perfect': 1,
                         'awesome': 0.8, 'bad': -0.5, 'worse': -0.4, 'worst': -0.9, 'terrible': -0.8,
                         'horrible': -0.8, 'ugly': -0.4, 'negative': -0.5, 'evil': -0.9, 'disgrace': -0.8,
                         'disappoint': -0.4, 'trouble': -0.3})
