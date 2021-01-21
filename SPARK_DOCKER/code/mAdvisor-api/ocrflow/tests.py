from django.test import TestCase

# Create your tests here.
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
from rest_framework.test import APIClient
from rest_framework import status
from django.test import TestCase
from django.contrib.auth.models import User, Group
from ocr.models import OCRImage

class OCRflow(TestCase):
    """
    class for unit test cases concerning OCRflow.
    """

    def setUp(self):
        # Every test needs access to the request factory.
        """
        Setup User and Authentication
        UserType: OCRAdminUser
        """

        self.credentials = {
            'username': 'dladmin',
            'password': 'thinkbig',
            'email': 'test@mail.com',}

         # Group setup
        group_name = "Admin"
        self.group = Group(name=group_name)
        self.group.save()

        user = User.objects.create_superuser(**self.credentials)
        user.groups.add(self.group)
        user.save()

        self.client = APIClient()
        response = self.client.post('http://localhost:8000/api-token-auth/',
                                    {'username': 'dladmin', "password": "thinkbig"}, format='json')
        self.token = response.json()['token']
        self.client.credentials(HTTP_AUTHORIZATION=self.token)

    def test_initial_OCRrules_status(self):
        """
        METHOD : [POST]
            Testcase1: Activate Initial Assignment
            Testcase2: Deactivate Initial Assignment
        """
        #Activate Test
        res = self.client.post('http://localhost:8000/ocrflow/rules/autoAssignment/',
            {'autoAssignment':'True', 'stage':'initial'}, format='json')

        self.assertEqual(res.json()['message'], "Initial Auto-Assignment Active.")

        #De-activate Test
        res = self.client.post('http://localhost:8000/ocrflow/rules/autoAssignment/',
            {'autoAssignment':'False', 'stage':'initial'}, format='json')

        self.assertEqual(res.json()['message'], "Initial Auto-Assignment De-active.")

    def test_secondary_OCRrules_status(self):
        """
        METHOD : [POST]
            Testcase1: Activate Secondary Assignment
            Testcase2: Deactivate Secondary Assignment
        """
        #Activate Test
        res = self.client.post('http://localhost:8000/ocrflow/rules/autoAssignment/',
            {'autoAssignment':'True', 'stage':'secondary'}, format='json')

        self.assertEqual(res.json()['message'], "Secondary Auto-Assignment Active.")

        #De-activate Test
        res = self.client.post('http://localhost:8000/ocrflow/rules/autoAssignment/',
            {'autoAssignment':'False', 'stage':'secondary'}, format='json')

        self.assertEqual(res.json()['message'], "Secondary Auto-Assignment De-active.")


    def test_modifyRules_L1(self):
        """
        METHOD : [POST]
            Testcase: Modify Initial Rules
        """
        data = {
            "custom":{
                "max_docs_per_reviewer": 10,
                "selected_reviewers": [],
                "remainaingDocsDistributionRule": 2,
                "active": "False"
                },
            "auto":{
                "max_docs_per_reviewer": 10,
                "remainaingDocsDistributionRule": 2,
                "active": "True"
                }
            }
        response = self.client.post('http://localhost:8000/ocrflow/rules/modifyRulesL1/',
            data, format='json')

        self.assertEqual(response.json()['message'], "Rules L1 Updated.")

    def test_modifyRules_L2(self):
        """
        METHOD : [POST]
            Testcase: Modify Secondary Rules
        """
        data = {
            "custom":{
                "max_docs_per_reviewer": 10,
                "selected_reviewers": [],
                "remainaingDocsDistributionRule": 2,
                "active": "False"
                },
            "auto":{
                "max_docs_per_reviewer": 10,
                "remainaingDocsDistributionRule": 2,
                "active": "True"
                }
            }
        response = self.client.post('http://localhost:8000/ocrflow/rules/modifyRulesL2/',
            data, format='json')

        self.assertEqual(response.json()['message'], "Rules L2 Updated.")

    def test_getOCRrules(self):
        """
        METHOD : [GET]
            Testcase: Get OCR Rules
        """
        response = self.client.get('http://localhost:8000/ocrflow/rules/get_rules/', format='json')
        self.assertEqual(response.json()['auto_assignmentL1'], True)
