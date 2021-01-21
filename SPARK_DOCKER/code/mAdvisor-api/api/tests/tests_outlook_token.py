from __future__ import print_function

from django.contrib.auth.models import User
from django.test import TestCase
from django.conf import settings
from rest_framework import status
from rest_framework.test import APIClient
import requests
import time


class TestOutlookTokens(TestCase):
    """
    Unit Test case class for Outlook Tokens.
    """
    OUTLOOK_AUTH_CODE = settings.OUTLOOK_AUTH_CODE
    OUTLOOK_REFRESH_TOKEN = settings.OUTLOOK_REFRESH_TOKEN
    OUTLOOK_DETAILS = {
        "client_id": '2e36be5f-0040-4f0d-bbef-12787ddc158b',
        "client_secret": '.5JwU-O9E_lY~uYUha5.3~dAUx3_0p_wu2',
        "tenant_id": 'cc6b2eea-c864-4839-85f5-94736facc3be',
        "redirect_uri": 'http://localhost:8000/get_request/'
    }
    OUTLOOK_SCOPES = ['openid', 'User.Read', 'Mail.Read', 'offline_access']

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

    def test_outlook_token(self):
        """
        Unit test cases for token generation.
        """
        post_data_auth_code = {
            'grant_type': 'authorization_code',
            'code': self.OUTLOOK_AUTH_CODE,
            'redirect_uri': self.OUTLOOK_DETAILS['redirect_uri'],
            'scope': self.OUTLOOK_SCOPES,
            'client_id': self.OUTLOOK_DETAILS['client_id'],
            'client_secret': self.OUTLOOK_DETAILS['client_secret']
        }
        post_data_refresh_token = {'grant_type': 'refresh_token',
                                   'redirect_uri': self.OUTLOOK_DETAILS['redirect_uri'],
                                   'scope': self.OUTLOOK_SCOPES,
                                   'refresh_token': self.OUTLOOK_REFRESH_TOKEN,
                                   'client_id': self.OUTLOOK_DETAILS['client_id'],
                                   'client_secret': self.OUTLOOK_DETAILS['client_secret']
                                   }
        if self.OUTLOOK_REFRESH_TOKEN is not None:
            r = requests.post(settings.OUTLOOK_TOKEN_URL, data=post_data_refresh_token)
            response = r.json()
            token_response = "Token Generated" if 'refresh_token' in response.keys() else "Token Not Generated"
        else:
            r = requests.post(settings.OUTLOOK_TOKEN_URL, data=post_data_auth_code)
            response = r.json()

        self.assertEqual(token_response, "Token Generated")
        self.assertEqual(status.HTTP_200_OK, r.status_code)

    def test_outlook_invalid_token(self):
        """
        Unit test cases for expired token.
        """
        OUTLOOK_REFRESH_INVALID_TOKEN = "0.AAAA6i5rzGTIOUiF9ZRzb6zDvl--Ni5AAA1Pu-8SeH3cFYtYAPE.AgABAAAAAAAGV_bv21oQQ4ROqh0_1-tAAQDs_wIA9P_OGYOVkWs4tpIDhO-WGf7nByalMDx2UuJbtBaJbIK0DCEM2pWIsrQDjP7ilTC2fNH_qtuETWAfQV1FincmGBBJ_CHP00qAwvfOAuv488gTSCU4eezpajvAIER2LC50q6HghAEBJRLZ2t-EdHD9KeJYsASzwpYMODUMLug7c1geD_oTI_est_6hHdTnn8nUrLo5jwUJWiWLLlwTzcQUswYnMjTCmr3tACvWi5gaRxJJwsQ3CQJQOye6v9g6lDpyqLC8OweL1ZsvwW4-xabeov8NKeFYLTIblt0CV9NApsog6ncexWQ0HRdrkmxiMLZv3jrD5FiFL0JywgekwxJtJyR47MPbZzjpJb6RkZs3tKPYUA9NT3NRqDBeVIDYD7aQfGNLB0zDn-ux41tuqjo7CtieBv7CwQb-9KrcSMXszlKvmMgbHikesUX2JFFF3QrXXY7yaKaQaI3h9cgUkJdf6WgkyZAnoqFZlqtFgxp3TWnO-x2mfT27fcKwxiAlbnG6XsXvtivXu7YHSjSFfhqNvgRCqbw0IDkeGTJIdsmCSh1NNtCy4iVE7d4uarmSh3I27selzPTOqZVoMAHvUd5I6TMzCNV-s1Rj0Ov5dTX5n33QYIG4LKxSWYL-gdGgZlAtQkW74o7e9CWggt2dpbziEsCyDgf-OufRmSqPHZruDOUqmJCdGroT5kvicydQBOObKPz5RbU8pelI_T5JVWQxJA1CMIrBlt8ihtKtrpKbI-BSsUJiYSJ65A0sTYMHVcvk_gcjzgkX4Ifi4ULQHzF9zlyCRdJAb8g2ccWaoCmUdm6kVY_iBt6XrhQ8PC1s0kriSi-fPkyj7-xYGXZrOR26Zv7r4Fgq1KFsbC0O79GnkMrOD_x4Szu0wHYQAzdOk37uAFOg93BRbbHf3RBXZqDfLlEJr_h4YIut6qW8zzRHgwK0ARMm4D3juhtCShyMrA0G1TjuRhUEsMWef4ALXA"
        post_data_auth_code = {
            'grant_type': 'authorization_code',
            'code': self.OUTLOOK_AUTH_CODE,
            'redirect_uri': self.OUTLOOK_DETAILS['redirect_uri'],
            'scope': self.OUTLOOK_SCOPES,
            'client_id': self.OUTLOOK_DETAILS['client_id'],
            'client_secret': self.OUTLOOK_DETAILS['client_secret']
        }
        post_data_refresh_token = {'grant_type': 'refresh_token',
                                   'redirect_uri': self.OUTLOOK_DETAILS['redirect_uri'],
                                   'scope': self.OUTLOOK_SCOPES,
                                   'refresh_token': OUTLOOK_REFRESH_INVALID_TOKEN,
                                   'client_id': self.OUTLOOK_DETAILS['client_id'],
                                   'client_secret': self.OUTLOOK_DETAILS['client_secret']
                                   }
        if self.OUTLOOK_REFRESH_TOKEN is not None:
            r = requests.post(settings.OUTLOOK_TOKEN_URL, data=post_data_refresh_token)
            response = r.json()
            token_response = "invalid_grant" if 'error' in response.keys() else "Valid Token"
        else:
            r = requests.post(settings.OUTLOOK_TOKEN_URL, data=post_data_auth_code)
            response = r.json()

        self.assertEqual(token_response, "invalid_grant")
        self.assertNotEqual(status.HTTP_200_OK, r.status_code)

    def test_outlook_token_negative(self):
        """
        Unit test case for token repeatation
        """
        post_data_auth_code = {
            'grant_type': 'authorization_code',
            'code': self.OUTLOOK_AUTH_CODE,
            'redirect_uri': self.OUTLOOK_DETAILS['redirect_uri'],
            'scope': self.OUTLOOK_SCOPES,
            'client_id': self.OUTLOOK_DETAILS['client_id'],
            'client_secret': self.OUTLOOK_DETAILS['client_secret']
        }
        post_data_refresh_token = {'grant_type': 'refresh_token',
                                   'redirect_uri': self.OUTLOOK_DETAILS['redirect_uri'],
                                   'scope': self.OUTLOOK_SCOPES,
                                   'refresh_token': self.OUTLOOK_REFRESH_TOKEN,
                                   'client_id': self.OUTLOOK_DETAILS['client_id'],
                                   'client_secret': self.OUTLOOK_DETAILS['client_secret']
                                   }
        if self.OUTLOOK_REFRESH_TOKEN is not None:
            r = requests.post(settings.OUTLOOK_TOKEN_URL, data=post_data_refresh_token)
            token_before = r.json()
            time.sleep(10)
            r = requests.post(settings.OUTLOOK_TOKEN_URL, data=post_data_refresh_token)
            token_after = r.json()
        else:
            r = requests.post(settings.OUTLOOK_TOKEN_URL, data=post_data_auth_code)
            response = r.json()

        self.assertNotEqual(token_before['refresh_token'], token_after['refresh_token'])
        self.assertEqual(status.HTTP_200_OK, r.status_code)
