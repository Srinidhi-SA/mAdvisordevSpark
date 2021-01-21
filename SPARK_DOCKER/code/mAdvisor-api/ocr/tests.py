"""
OCR AUTOMATED TESTCASES
"""

# -------------------------------------------------------------------------------
# pylint: disable=too-many-ancestors
# pylint: disable=no-member
# pylint: disable=too-many-return-statements
# pylint: disable=too-many-locals
# pylint: disable=invalid-name
# pylint: disable=unused-argument
# pylint: disable=line-too-long
# -------------------------------------------------------------------------------

import tempfile
from PIL import Image
from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.contrib.auth.models import User
from ocr.models import OCRImage


class TestOCRImageUpload(TestCase):
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
            'username': 'dladmin',
            'password': 'thinkbig',
            'email': 'test@mail.com'}
        User.objects.create_superuser(**self.credentials)

        self.client = APIClient()
        response = self.client.post('http://localhost:8000/api-token-auth/',
                                    {'username': 'dladmin', "password": "thinkbig"}, format='json')
        self.token = response.json()['token']
        self.client.credentials(HTTP_AUTHORIZATION=self.token)

    def test_OCRImage_create(self):
        """
        METHOD: [CREATE]
            TestCase1: "Test single image upload."
            TestCase2: "Test multiple image upload."
            TestCase3: "Test valid/Invalid file extensions."
        METHOD: [GET]
            TestCase1: "List of image uploaded."
        METHOD: [RETRIEVE]
            TestCase1: "Retrieve image uploaded with particular slug."
        METHOD: [PUT/UPDATE]
            TestCase1: "Update image uploaded with particular slug."
        METHOD: [DELETE]
            TestCase1: "Delete image uploaded with particular slug."
        """

        response = self.client.post('http://localhost:8000/ocr/project/', {'name': 'new'})
        projectslug = response.json()['project_serializer_data']['slug']

        image = Image.new('RGB', (100, 100))

        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file, format='jpeg')
        tmp_file.seek(0)
        response = self.client.post('http://localhost:8000/ocr/ocrimage/',
                                    {'imagefile': tmp_file, 'dataSourceType': 'fileUpload', 'projectslug': projectslug}, format='multipart')

        # self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.json()['imageset_message'], response.json()['message'])

    def test_OCRImage_create_multiple(self):
        """
        TestCase1: "Test single image upload."
        TestCase2: "Test multiple image upload."
        TestCase3: "Test valid/Invalid file extensions."
        """
        response = self.client.post('http://localhost:8000/ocr/project/', {'name': 'new'})
        projectslug = response.json()['project_serializer_data']['slug']

        img_list = list()
        for _ in range(3):
            image = Image.new('RGB', (100, 100), color='red')
            tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
            image.save(tmp_file, format=image.format)
            tmp_file.seek(0)
            img_list.append(tmp_file)

        response = self.client.post('http://localhost:8000/ocr/ocrimage/',
                                    {'imagefile': img_list, 'dataSourceType': 'fileUpload', 'projectslug': projectslug}, format='multipart')

        # self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.json()['imageset_message'], response.json()['message'])

    def test_OCRImage_extension_validation(self):
        """
        TestCase1: "Test single image upload."
        TestCase2: "Test multiple image upload."
        TestCase3: "Test valid/Invalid file extensions."
        """

        response = self.client.post('http://localhost:8000/ocr/project/', {'name': 'new'})
        projectslug = response.json()['project_serializer_data']['slug']

        tmp_file = tempfile.NamedTemporaryFile(suffix='.txt')
        tmp_file.write(b'test')
        tmp_file.seek(0)
        response = self.client.post('http://localhost:8000/ocr/ocrimage/',
                                    {'imagefile': tmp_file, 'dataSourceType': 'fileUpload', 'projectslug': projectslug}, format='multipart')
        res = response.json()
        self.assertEqual('Unsupported file extension.' in res['serializer_error'], True)

    def test_OCRImage_list(self):
        """
        Unit test cases concerning OCRImage list view.
        """

        response = self.client.post('http://localhost:8000/ocr/project/', {'name': 'new'})
        projectslug = response.json()['project_serializer_data']['slug']

        img_list = list()
        for _ in range(3):
            image = Image.new('RGB', (100, 100), color='red')
            tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
            image.save(tmp_file, format=image.format)
            tmp_file.seek(0)
            img_list.append(tmp_file)

        self.client.post('http://localhost:8000/ocr/ocrimage/', {'imagefile': img_list, 'dataSourceType': 'fileUpload', 'projectslug': projectslug}, format='multipart')
        response = self.client.get('http://localhost:8000/ocr/ocrimage/', format='json')

        self.assertEqual(response.json()['current_item_count'], 3)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_OCRImage_update(self):
        """
        Unit test cases concerning OCRImage update view.
        """

        response = self.client.post('http://localhost:8000/ocr/project/', {'name': 'new'})
        projectslug = response.json()['project_serializer_data']['slug']

        image = Image.new('RGB', (100, 100))

        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file, format='jpeg')
        tmp_file.seek(0)
        self.client.post('http://localhost:8000/ocr/ocrimage/', {'imagefile': tmp_file, 'dataSourceType': 'fileUpload', 'projectslug': projectslug},
                         format='multipart')
        imagequery = OCRImage.objects.all().first()
        slug = imagequery.slug
        response = self.client.put('http://localhost:8000/ocr/ocrimage/{}/'.format(slug), {'name': 'unit-test'})

        self.assertEqual(response.json()['name'], 'unit-test')

    def test_OCRImage_retrieve(self):
        """
        Unit test cases concerning OCRImage retrieve view.
        """

        response = self.client.post('http://localhost:8000/ocr/project/', {'name': 'new'})
        projectslug = response.json()['project_serializer_data']['slug']

        image = Image.new('RGB', (100, 100))

        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file, format='jpeg')
        tmp_file.seek(0)
        response = self.client.post('http://localhost:8000/ocr/ocrimage/',
                                    {'imagefile': tmp_file, 'dataSourceType': 'fileUpload', 'projectslug': projectslug}, format='multipart')

        data = response.json()['serializer_data'][0]
        slug = data['slug']
        response = self.client.get('http://localhost:8000/ocr/ocrimage/{}/'.format(slug))

        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_OCRImage_extract2(self):
        """
        Unit test cases concerning OCRImage extract async view.
        """
        response = self.client.post('http://localhost:8000/ocr/project/', {'name': 'new'})
        projectslug = response.json()['project_serializer_data']['slug']
        image = Image.new('RGB', (100, 100))

        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file, format='jpeg')
        tmp_file.seek(0)
        response = self.client.post('http://localhost:8000/ocr/ocrimage/',
                                    {'imagefile': tmp_file, 'dataSourceType': 'fileUpload', 'projectslug': projectslug}, format='multipart')

        data = response.json()['serializer_data'][0]
        slug = data['slug']
        response = self.client.post('http://localhost:8000/ocr/ocrimage/extract2/', {'slug': [slug]})
        self.assertEqual(status.HTTP_200_OK, response.status_code)


class TestOCRImageSetView(TestCase):
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
            'username': 'dladmin',
            'password': 'thinkbig',
            'email': 'test@mail.com'}
        User.objects.create_superuser(**self.credentials)

        self.client = APIClient()
        response = self.client.post('http://localhost:8000/api-token-auth/',
                                    {'username': 'dladmin', "password": "thinkbig"}, format='json')
        self.token = response.json()['token']
        self.client.credentials(HTTP_AUTHORIZATION=self.token)

    def test_OCRImageSet_list(self):
        """
        Unit test cases concerning OCRImageSet list view.
        """

        img_list = list()
        for _ in range(3):
            image = Image.new('RGB', (100, 100), color='red')
            tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
            image.save(tmp_file, format=image.format)
            tmp_file.seek(0)
            img_list.append(tmp_file)
        self.client.post('http://localhost:8000/ocr/ocrimage/',
                                         {'imagefile': img_list, 'dataSourceType': 'fileUpload'}, format='multipart')
        response = self.client.get('http://localhost:8000/ocr/ocrimageset/', format='json')

        self.assertEqual(response.json()['current_item_count'], 1)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_OCRImageSet_retrieve(self):
        """
        Unit test cases concerning OCRImageSet retrieve view.
        """

        image = Image.new('RGB', (100, 100))

        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file, format='jpeg')
        tmp_file.seek(0)
        response = self.client.post('http://localhost:8000/ocr/ocrimage/',
                                    {'imagefile': tmp_file, 'dataSourceType': 'fileUpload'}, format='multipart')
        data = response.json()['imageset_serializer_data']
        slug = data['slug']
        response = self.client.get('http://localhost:8000/ocr/ocrimageset/{}/'.format(slug))

        self.assertEqual(status.HTTP_200_OK, response.status_code)
