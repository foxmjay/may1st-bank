from django.test import TestCase
from .serializers import CotisationSerializer, CotisationSimplifiedSerializer


class CotisationsTestCase(TestCase):

    def setUP(self):
        pass


    def test_serializer(self):
        self.assertEqual('Hello','Hello')

# Create your tests here.
