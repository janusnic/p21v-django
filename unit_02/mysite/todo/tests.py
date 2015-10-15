from django.core.urlresolvers import resolve
from django.test import TestCase
from todo.views import home_page 

class HomePageTest(TestCase):

    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/') 
        self.assertEqual(found.func, home_page) 

# Create your tests here.
class EqualTest(TestCase):

    def test_bad_maths(self):
        # self.assertEqual(1 + 1, 3)
        self.assertEqual(1 + 1, 2)