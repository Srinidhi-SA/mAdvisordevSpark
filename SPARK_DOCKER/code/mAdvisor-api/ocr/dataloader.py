""" Get Files from AWS S3 """

import os
import random
import string
import boto3
from botocore.exceptions import ClientError


class S3File:
    """ Description : Used for S3 file Operations"""

    def get_boto_session(self, access_key=None, secret_key=None):
        """ Parameteres : s3 bucket details captured from user as parameter"""
        return boto3.Session(aws_access_key_id=access_key, aws_secret_access_key=secret_key)

    def get_boto_resourse(self, access_key=None, secret_key=None):
        """ Parameteres : s3 bucket details captured from user as parameter"""
        session = self.get_boto_session(access_key, secret_key)
        return session.resource('s3')

    def get_boto_bucket(self, s3_bucket_name=None, access_key=None, secret_key=None):
        """ Parameteres : s3 bucket details captured from user as parameter"""
        resource = self.get_boto_resourse(access_key, secret_key)
        return resource.Bucket(s3_bucket_name)

    def download_file_from_s3(self, **kwargs):
        """
        Description: Used for downloading s3 bucket files
        Parameteres : kwargs will return the details of s3
        """

        file_names = kwargs['file_names']
        access_key = kwargs['access_key_id']
        secret_key = kwargs['secret_key']
        s3_bucket_name = kwargs['bucket_name']

        dir_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))

        sftp_dir = '/tmp/sftp/'
        s3_dir = '/tmp/s3/'

        data_source_directory = [s3_dir + dir_name, sftp_dir]

        for dir in data_source_directory:
            if not os.path.exists(dir):
                os.makedirs(dir)

        try:
            bucket = self.get_boto_bucket(s3_bucket_name, access_key, secret_key)
            for file in file_names:
                file_name_dst = str(random.randint(10000, 99999)) + '_' + file
                bucket.download_file(file, os.path.join(s3_dir, dir_name, file_name_dst))

            return {
                'status': 'SUCCESS',
                'file_path': os.path.join(s3_dir, dir_name)
            }

        except Exception as err:
            return {
                'status': 'FAILED',
                'Exception': str(err)
            }

    def s3_files(self, **kwargs):
        """
        Description: Used for getting list of files from s3 bucket
        Parameteres : kwargs will return the details of s3
        """
        # file_names = kwargs['file_names']
        access_key = kwargs['access_key_id']
        secret_key = kwargs['secret_key']
        s3_bucket_name = kwargs['bucket_name']
        files = []

        try:
            for file in self.get_boto_bucket(s3_bucket_name, access_key, secret_key).objects.all():
                files.append(file.key)

            return {
                'status': 'SUCCESS',
                'file_list': files
            }

        except ClientError as e:
            if e.response['Error']['Code'] == "InvalidAccessKeyId":
                error_message = 'Invalid Access Key'
            elif e.response['Error']['Code'] == "NoSuchBucket":
                error_message = 'Invalid Bucket Name'
            elif e.response['Error']['Code'] == "SignatureDoesNotMatch":
                error_message = 'Invalid Secret key'
            else:
                error_message = 'Invalid Details'
            return {
                'status': 'FAILED',
                'Exception': str(e),
                'message': error_message
            }
