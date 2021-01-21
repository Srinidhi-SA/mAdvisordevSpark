# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import csv
from django.contrib.auth.models import User
from django.test import TestCase
# Create your tests here.
from rest_framework import status
from rest_framework.test import APIClient


class TestDatasetUpload(TestCase):
    """
    class for unit test cases concerning OCRImage upload.
    """

    def setUp(self):
        # Every test needs access to the request factory.
        """
        Setup User and Authentication
        UserType: Superuser
        """

        self.credentials = {
            'username': 'frontend',
            'password': 'password@123',
            'email': 'test@mail.com'}
        User.objects.create_superuser(**self.credentials)

        self.client = APIClient()
        response = self.client.post('http://localhost:8000/api-token-auth/',
                                    {'username': 'frontend', "password": "password@123"}, format='json')
        self.token = response.json()['token']
        self.client.credentials(HTTP_AUTHORIZATION=self.token)

    def test_Dataset_create_multiple(self):
        """
        TestCase1: "Test single image upload."
        TestCase2: "Test multiple image upload."
        TestCase3: "Test valid/Invalid file extensions."
        """

        dataset_list = list()
        for i in range(3):
            row_list = [["SN", "Name", "Contribution"],
                        [1, "Linus Torvalds", "Linux Kernel"],
                        [2, "Tim Berners-Lee", "World Wide Web"],
                        [3, "Guido van Rossum", "Python Programming"]]
            with open('protagonist{}.csv'.format(i), 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(row_list)
            dataset_list.append('protagonist{}.csv'.format(i))

        response = self.client.post('http://localhost:8000/api/datasets/',
                                    {'input_file': dataset_list, 'datasource_type': 'fileUpload'}, format='multipart')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        # self.assertEqual(response.json()['imageset_message'], response.json()['message'])
