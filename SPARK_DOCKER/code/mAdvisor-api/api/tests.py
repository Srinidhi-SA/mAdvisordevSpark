from django.test import TestCase

# Create your tests here.
from rest_framework.test import APIRequestFactory

class APILoginTest(TestCase):
    def testLogin(self):
        # factory = APIRequestFactory()
        # request = factory.post('/api-token-auth/', {'username': 'marlabs', "password" : "password123"}, format='json')
        from rest_framework.test import APIClient

        client = APIClient()
        response = client.post('/api-token-auth/', {'username': 'marlabs', "password" : "password123"}, format='json')

        print(response.data)

        pass

class APIDatasetsTest(TestCase):
    def testDatasetListing(self):
        self.assertIs(1+2,3, "addition failed")

