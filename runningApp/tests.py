from django.test import TestCase

# Create your tests here.
class TestTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        self.assertIs(1, 1)
    
class RouteTests(TestCase):
    pass