from __future__ import print_function

from django.contrib.auth.models import User
from django.test import TestCase
from django.conf import settings
from rest_framework import status
from rest_framework.test import APIClient


class TestAlgorithmSettings(TestCase):
    """
    class for unit test cases concerning Algorithm settings.
    """

    def setUp(self):
        # Every test needs access to the request factory.
        """
        Setup User and Authentication
        UserType: Superuser
        """

        self.credentials = {
            'username': 'dladmin',
            'password': 'thinkbig',
            'email': 'test@mail.com'}
        User.objects.create_superuser(**self.credentials)

        self.client = APIClient()
        response = self.client.post('http://localhost:8000/api-token-auth/',
                                    {'username': self.credentials['username'],
                                     "password": self.credentials['password']}, format='json')
        self.token = response.json()['token']
        self.client.credentials(HTTP_AUTHORIZATION=self.token)


    def test_classification_automl(self):
        """
        Unit test cases concerning Algorithm settings for classification autoML.
        """

        response = self.client.get('http://localhost:8000/api/get_app_algorithm_config_list/',
                                   {'app_type': 'CLASSIFICATION', 'mode': 'autoML'},
                                   format='json')

        self.assertEqual(response.json(), settings.AUTOML_ALGORITHM_LIST_CLASSIFICATION)
        self.assertEqual(status.HTTP_200_OK, response.status_code)


    def test_classification_automl_negative(self):
        """
        Unit test cases concerning Algorithm settings for classification autoML Negative test case.
        """

        response = self.client.get('http://localhost:8000/api/get_app_algorithm_config_list/',
                                   {'app_type': 'CLASSIFICATION', 'mode': 'autoML'},
                                   format='json')

        self.assertEqual(response.json(), "Automl Negative test case")
        self.assertEqual(status.HTTP_200_OK, response.status_code)


    def test_classification_analyst(self):
        """
        Unit test cases concerning Algorithm settings for classification analyst.
        """

        response = self.client.get('http://localhost:8000/api/get_app_algorithm_config_list/',
                                   {'app_type': 'CLASSIFICATION', 'mode': 'ananlyst'},
                                   format='json')

        algorithm_lists = []
        for case in response.json()['ALGORITHM_SETTING']:
            algorithm_lists.append(case['algorithmName'])

        self.assertEqual(algorithm_lists,
                         ['Logistic Regression', 'Random Forest', 'XGBoost', 'naive bayes', 'Neural Network (Sklearn)',
                          'Neural Network (TensorFlow)', 'Neural Network (PyTorch)'])
        self.assertEqual(status.HTTP_200_OK, response.status_code)


    def test_classification_analyst_negative(self):
        """
        Unit test cases concerning Algorithm settings for classification analyst Negative test case.
        """

        response = self.client.get('http://localhost:8000/api/get_app_algorithm_config_list/',
                                   {'app_type': 'CLASSIFICATION', 'mode': 'ananlyst'},
                                   format='json')

        algorithm_lists = []
        for case in response.json()['ALGORITHM_SETTING']:
            algorithm_lists.append(case['algorithmName'])

        self.assertEqual(algorithm_lists,
                         ['Logistic Regression', 'Random Forest', 'XGBoost', 'naive bayes',
                          'Neural Network (TensorFlow)', 'Neural Network (PyTorch)'])
        self.assertEqual(status.HTTP_200_OK, response.status_code)
