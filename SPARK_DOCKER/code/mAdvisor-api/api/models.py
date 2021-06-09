# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import

from builtins import str
from builtins import range
from builtins import object
import csv
import simplejson as json
import os
import random
import string
import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from api.helper import update_stock_sense_message

from .StockAdvisor.crawling.common_utils import get_regex
from .StockAdvisor.crawling.crawl_util import crawl_extract, \
    generate_urls_for_crawl_news, \
    convert_crawled_data_to_metadata_format, \
    generate_urls_for_historic_data, \
    fetch_news_article_from_nasdaq, \
    generate_url_for_historic_data, \
    generate_urls_for_historic_data, fetch_news_sentiments_from_newsapi
from api.helper import convert_json_object_into_list_of_object, get_schedule
from api.lib import hadoop, fab_helper

THIS_SERVER_DETAILS = settings.THIS_SERVER_DETAILS
from auditlog.registry import auditlog
from django.conf import settings
from .helper import convert_fe_date_format
from django_celery_beat.models import PeriodicTask

from guardian.shortcuts import assign_perm

# Create your models here.


STATUS_CHOICES = (
    ('0', 'Not Started Yet'),
    ('1', 'Signal Creation Started.'),
    ('2', 'Trend Created'),
    ('3', 'ChiSquare Created'),

    ('4', 'Decision Tree Created'),
    ('5', 'Density Histogram Created'),
    ('6', 'Regression Created'),
    ('7', 'Signal Creation Done'),
)


class Job(models.Model):
    job_type = models.CharField(max_length=300, null=False)
    object_id = models.CharField(max_length=300, null=False)
    name = models.CharField(max_length=300, null=False, default="")
    slug = models.SlugField(null=True, max_length=300)
    config = models.TextField(default="{}")
    results = models.TextField(default="{}")
    url = models.TextField(default="")
    status = models.CharField(max_length=100, default="")
    command_array = models.TextField(default="{}")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    deleted = models.BooleanField(default=False)
    submitted_by = models.ForeignKey(User, null=False)
    error_report = models.TextField(default="{}")
    messages = models.TextField(default="{}")
    message_log = models.TextField(default="{}")

    def generate_slug(self):
        if not self.slug:
            self.slug = slugify(str(self.name) + "-" + ''.join(
                random.choice(string.ascii_uppercase + string.digits) for _ in range(10)))

    def save(self, *args, **kwargs):
        self.generate_slug()
        super(Job, self).save(*args, **kwargs)

    def __str__(self):
        return " : ".join(["{}".format(x) for x in [self.name, self.job_type, self.created_at, self.slug]])

    def kill(self):
        from api.tasks import kill_application_using_fabric
        if self.url == "":
            return False

        if self.url is None:
            return False
        kill_application_using_fabric.delay(self.url)
        original_object = self.get_original_object()

        if original_object is not None:
            original_object.status = 'FAILED'
            original_object.save()
        self.status = 'KILLED'
        self.save()
        return True

    def start(self):
        command_array = json.loads(self.command_array)
        from .tasks import submit_job_separate_task1, submit_job_separate_task

        if settings.SUBMIT_JOB_THROUGH_CELERY:
            submit_job_separate_task.delay(command_array, self.slug)
        else:
            submit_job_separate_task1(command_array, self.slug)
        original_object = self.get_original_object()

        if original_object is not None:
            original_object.status = 'INPROGRESS'
            original_object.save()

        self.save()

    def update_status(self):
        import yarn_api_client
        try:
            ym = yarn_api_client.resource_manager.ResourceManager(address=settings.YARN.get("host"),
                                                                  port=settings.YARN.get("port"),
                                                                  timeout=settings.YARN.get("timeout"))
            app_status = ym.cluster_application(self.url)
            self.status = app_status.data['app']["state"]
            self.save()
        except Exception as err:
            print(err)

    def get_original_object(self):
        original_object = None
        if self.job_type in ["metadata", "subSetting"]:
            original_object = Dataset.objects.get(slug=self.object_id)
        elif self.job_type == "master":
            original_object = Insight.objects.get(slug=self.object_id)
        elif self.job_type == "model":
            original_object = Trainer.objects.get(slug=self.object_id)
        elif self.job_type == 'score':
            original_object = Score.objects.get(slug=self.object_id)
        elif self.job_type == 'robo':
            original_object = Robo.objects.get(slug=self.object_id)
        elif self.job_type == 'stockAdvisor':
            original_object = StockDataset.objects.get(slug=self.object_id)
        else:
            print("No where to write")

        return original_object

    def reset_message(self):
        empty_dict = dict()
        self.message_log = json.dumps(empty_dict)
        self.save()


class Dataset(models.Model):
    name = models.CharField(max_length=100, null=True)
    slug = models.SlugField(null=True, max_length=300)
    auto_update = models.BooleanField(default=False)
    auto_update_duration = models.IntegerField(default=99999)

    input_file = models.FileField(upload_to='datasets', null=True)
    datasource_type = models.CharField(max_length=100, null=True)
    datasource_details = models.TextField(default="{}")
    preview = models.TextField(default="{}")

    meta_data = models.TextField(default="{}")

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    created_by = models.ForeignKey(User, null=True, db_index=True)
    deleted = models.BooleanField(default=False)
    subsetting = models.BooleanField(default=False, blank=True)

    job = models.ForeignKey(Job, null=True)

    bookmarked = models.BooleanField(default=False)
    file_remote = models.CharField(max_length=100, null=True)
    analysis_done = models.BooleanField(default=False)
    status = models.CharField(max_length=100, null=True, default="Not Registered")
    viewed = models.BooleanField(default=False)
    shared = models.BooleanField(default=False)
    shared_by = models.CharField(max_length=100, null=True)
    shared_slug = models.SlugField(null=True, max_length=300)

    class Meta(object):
        ordering = ['-created_at', '-updated_at']
        permissions = settings.PERMISSIONS_RELATED_TO_DATASET

    def __str__(self):
        return " : ".join(["{}".format(x) for x in [self.name, self.datasource_type, self.slug]])

    def as_dict(self):
        return {
            'name': self.name,
            'slug': self.slug,
            'auto_update': self.auto_update,
            'datasource_type': self.datasource_type,
            'datasource_details': self.datasource_details,
            'created_on': self.created_at,  # TODO: depricate this value
            'created_at': self.created_at,
            'bookmarked': self.bookmarked
        }

    def generate_slug(self):
        if not self.slug:
            self.slug = slugify(str(self.name) + "-" + ''.join(
                random.choice(string.ascii_uppercase + string.digits) for _ in range(10)))

    def save(self, *args, **kwargs):
        self.generate_slug()
        super(Dataset, self).save(*args, **kwargs)

    def create(self):
        if self.datasource_type in ['file', 'fileUpload']:
            self.csv_header_clean()
            self.copy_file_to_destination()
        self.add_to_job()

    def get_upload_to(self, field_attname):
        """Get upload_to path specific to this photo."""
        return 'photos/%d' % self.id

    def create_for_subsetting(
            self,
            filter_subsetting,
            transformation_settings,
            inputfile,
            original_metadata_url_info

    ):
        self.set_subesetting_true()
        jobConfig = self.add_subsetting_to_config(
            filter_subsetting
        )
        jobConfig = self.add_transformation_settings_to_config(jobConfig=jobConfig,
                                                               transformation_settings=transformation_settings)

        if inputfile:
            jobConfig = self.add_inputfile_outfile_to_config(
                inputfile,
                jobConfig
            )
        if original_metadata_url_info:
            jobConfig = self.add_previous_dataset_metadata_url_info(
                original_metadata_url_info=original_metadata_url_info,
                jobConfig=jobConfig
            )

        job = job_submission(
            instance=self,
            jobConfig=jobConfig,
            job_type='subSetting'
        )

        self.job = job

        if job is None:
            self.status = "FAILED"
        else:
            self.status = "INPROGRESS"

        self.save()

    def set_subesetting_true(self):
        self.subsetting = True
        self.save()

    def add_to_job(self):

        jobConfig = self.generate_config()

        job = job_submission(
            instance=self,
            jobConfig=jobConfig,
            job_type='metadata'
        )

        self.job = job

        if job is None:
            self.status = "FAILED"
        else:
            self.status = "INPROGRESS"
        self.save()

    def add_subsetting_to_config(self, filter_subsetting):

        jobConfig = self.generate_config()
        jobConfig["config"]["FILTER_SETTINGS"] = filter_subsetting

        return jobConfig

    def add_transformation_settings_to_config(self, jobConfig, transformation_settings):

        jobConfig["config"]["TRANSFORMATION_SETTINGS"] = transformation_settings

        return jobConfig

    def add_inputfile_outfile_to_config(self, inputfile, jobConfig):
        jobConfig["config"]["FILE_SETTINGS"] = {
            "inputfile": [inputfile],
            "outputfile": [self.get_output_file()],
        }

        return jobConfig

    def add_previous_dataset_metadata_url_info(self, original_metadata_url_info, jobConfig):

        if "FILE_SETTINGS" in jobConfig["config"]:
            jobConfig["config"]["FILE_SETTINGS"]['metadata'] = original_metadata_url_info

        return jobConfig

    def generate_config(self, *args, **kwrgs):
        inputFile = ""
        datasource_details = ""
        try:
            inputFileSize = os.stat(self.input_file.path).st_size
        except:
            inputFileSize = ""
        if self.datasource_type in ['file', 'fileUpload']:
            inputFile = self.get_input_file()

        else:
            datasource_details = json.loads(self.datasource_details)

        return {
            "config": {
                "FILE_SETTINGS": {
                    "inputfile": [inputFile],
                    "inputfilesize": inputFileSize,
                },
                "COLUMN_SETTINGS": {
                    "analysis_type": ["metaData"],
                },
                "DATE_SETTINGS": {

                },
                "DATA_SOURCE": {
                    "datasource_type": self.datasource_type,
                    "datasource_details": datasource_details
                }
            }
        }

    def csv_header_clean(self):
        CLEAN_DATA = []
        cleaned_header = []
        os.chmod(self.input_file.path, 0o777)
        with open(self.input_file.path) as file:
            rows = csv.reader(file)
            for (i, row) in enumerate(rows):
                row = [self.clean_restriced_chars(item) for item in row]
                if i == 0:
                    cleaned_header = self.clean_column_names(row)
                else:
                    CLEAN_DATA.append(row)

        with open(self.input_file.path, 'w') as file:
            writer = csv.writer(file)
            writer.writerow(cleaned_header)

            for row in CLEAN_DATA:
                writer.writerow(row)

        return cleaned_header

    def clean_column_names(self, colname_list):
        special_chars = [".", "*", "$", "#"]
        cleaned_list = []

        for col in colname_list:
            for x in special_chars:
                col = col.replace(x, "")
            col = col.strip(' ')
            cleaned_list.append(col)
        return cleaned_list

    def clean_restriced_chars(self, line):
        restricted_chars = string.printable
        return "".join([c for c in line if c in restricted_chars])

    def copy_file_to_destination(self):
        try:
            self.copy_file_to_hdfs()
            self.file_remote = "hdfs"
        except:
            try:
                self.copy_file_to_hdfs_local()
                self.file_remote = "emr_file"
            except:
                pass

    def copy_file_to_hdfs(self):
        file_size = os.stat(self.input_file.path).st_size
        try:
            if file_size > 128000000:
                hadoop.hadoop_put(self.input_file.path, self.get_hdfs_relative_path())
        except:
            raise Exception("Failed to copy file to HDFS.")

    def copy_file_to_hdfs_local(self):
        try:
            pass
            fab_helper.mkdir_remote(self.get_hdfs_relative_path())
            fab_helper.put_file(self.input_file.path, self.get_hdfs_relative_path())
        except:
            raise Exception("Failed to copy file to EMR Local")

    def get_hdfs_relative_path(self):
        return os.path.join(settings.HDFS.get('base_path'), self.slug)

    def get_hdfs_relative_file_path(self):

        if self.shared is True:
            return os.path.join(settings.HDFS.get('base_path'), self.shared_slug)
        if self.subsetting is True:
            return os.path.join(settings.HDFS.get('base_path'), self.slug)

        return os.path.join(settings.HDFS.get('base_path'), self.slug, os.path.basename(self.input_file.path))

    def emr_local(self):
        return "/home/marlabs" + self.get_hdfs_relative_path()

    def get_input_file(self):
        print("File Upload in container logs- New Demo 12-04-2021")
        if self.datasource_type in ['file', 'fileUpload']:
            type = self.file_remote
            if type == 'emr_file':
                return "file://{}".format(self.input_file.path)
            elif type == 'hdfs':
                file_size = os.stat(self.input_file.path).st_size
                if file_size < 128000000:
                    if settings.USE_HTTPS:
                        protocol = 'https'
                    else:
                        protocol = 'http'
                    dir_path = "{0}://{1}".format(protocol, THIS_SERVER_DETAILS.get('host'))

                    path = str(self.input_file)
                    if '/home/' in path:
                        file_name = path.split("/config")[-1]
                    else:
                        file_name = os.path.join('/media/', str(self.input_file))
                else:
                    dir_path = "hdfs://{}:{}".format(
                        settings.HDFS.get("host"),
                        settings.HDFS.get("hdfs_port")
                    )
                    file_name = self.get_hdfs_relative_file_path()
                return dir_path + file_name

            elif type == 'fake':
                return "file:///asdasdasdasd"
        else:
            return ""

    def get_output_file(self):
        from api.helper import encrypt_url
        HDFS = settings.HDFS
        if self.datasource_type in ['file', 'fileUpload']:
            type = self.file_remote
            if type == 'emr_file':
                final_url = "file://{}".format(self.input_file.path)
                encrypted_url = encrypt_url(final_url)
                return encrypted_url
            elif type == 'hdfs':

                if 'password' in HDFS:
                    dir_path = "hdfs://{}:{}@{}:{}".format(
                        HDFS.get("user.name"),
                        HDFS.get("password"),
                        HDFS.get("host"),
                        HDFS.get("hdfs_port")
                    )
                else:
                    dir_path = "hdfs://{}:{}".format(
                        HDFS.get("host"),
                        HDFS.get("hdfs_port")
                    )
                file_name = self.get_hdfs_relative_file_path()
                final_url = dir_path + file_name
                encrypted_url = encrypt_url(final_url)
                return encrypted_url

            elif type == 'fake':
                return "file:///asdasdasdasd"
        else:
            return ""

    def get_datasource_info(self):
        datasource_details = ""
        if self.datasource_type in ['file', 'fileUpload']:
            inputFile = self.get_input_file()
        else:
            datasource_details = json.loads(self.datasource_details)

        return {
            "datasource_type": self.datasource_type,
            "datasource_details": datasource_details
        }

    def common_config(self):

        ignore_column_suggestion = []
        utf8_column_suggestions = []
        dateTimeSuggestions = []

        if self.analysis_done is True:
            meta_data = json.loads(self.meta_data)
            dataset_meta_data = meta_data.get('metaData')

            for variable in dataset_meta_data:
                if variable['name'] == 'ignoreColumnSuggestions':
                    ignore_column_suggestion += variable['value']

                if variable['name'] == 'utf8ColumnSuggestion':
                    utf8_column_suggestions += variable['value']

                if variable['name'] == 'dateTimeSuggestions':
                    dateTimeSuggestions += [variable['value']]
        else:
            print("How the hell reached here!. Metadata is still not there. Please Wait.")

        return {
            'ignore_column_suggestion': ignore_column_suggestion,
            'utf8_column_suggestions': utf8_column_suggestions,
            'dateTimeSuggestions': dateTimeSuggestions,
        }

    def get_config(self):
        config = json.loads(self.meta_data)
        if config is None:
            return {}
        return config

    def get_number_of_row_size(self):
        config = self.get_config()
        if 'metaData' in config:
            metad = config['metaData']
            for data in metad:
                if 'displayName' not in data:
                    continue
                if data['displayName'] == 'Rows':
                    return int(data['value'])
        return -1

    def get_brief_info(self):
        list_objects = []
        brief_info = dict()
        config = self.get_config()
        sample = {
            'Rows': 'number of rows',
            'Columns': 'number of columns',
            'Measures': 'number of measures',
            'Measure': 'number of measures',
            'Dimensions': 'number of dimensions',
            'Dimension': 'number of dimensions',
            'Time Dimension': 'number of time dimension',
        }
        if 'metaData' in config:
            metad = config['metaData']
            for data in metad:
                if 'displayName' not in data:
                    continue
                if data['displayName'] in sample:
                    brief_info.update(
                        {
                            sample[data['displayName']]: data['value']
                        }
                    )
        if self.shared is True:

            brief_info.update(
                {
                    'shared_by': self.shared_by,
                    'updated_at': self.updated_at,
                    'dataset': self.name
                }
            )
        else:
            brief_info.update(
                {
                    'created_by': self.created_by.username,
                    'updated_at': self.updated_at,
                    'dataset': self.name
                }
            )
        return convert_json_object_into_list_of_object(brief_info, 'dataset')

    def get_metadata_url_config(self):
        if settings.USE_HTTPS:
            ip_port = "https://{0}".format(THIS_SERVER_DETAILS.get('host'))
        else:
            ip_port = "http://{0}".format(THIS_SERVER_DETAILS.get('host'))
        url = "/api/get_metadata_for_mlscripts/"
        slug_list = [
            self.slug
        ]
        return {
            "url": ip_port + url,
            "slug_list": slug_list
        }


class Insight(models.Model):
    name = models.CharField(max_length=300, null=True)
    slug = models.SlugField(null=False, blank=True, max_length=300)
    type = models.CharField(max_length=300, null=True)  # dimension/measure
    target_column = models.CharField(max_length=300, null=True, blank=True)

    dataset = models.ForeignKey(Dataset, null=True)  # get all dataset related detail

    compare_with = models.CharField(max_length=300, default="", null=True, blank=True)
    compare_type = models.CharField(max_length=300, null=True, blank=True)
    column_data_raw = models.TextField(default="{}")
    config = models.TextField(default="{}")

    live_status = models.CharField(max_length=300, default='0', choices=STATUS_CHOICES)
    analysis_done = models.BooleanField(default=False)
    # state -> job submitted, job started, job ...

    data = models.TextField(default="{}")

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    created_by = models.ForeignKey(User, null=False, db_index=True)
    deleted = models.BooleanField(default=False, )

    bookmarked = models.BooleanField(default=False)

    job = models.ForeignKey(Job, null=True)
    status = models.CharField(max_length=100, null=True, default="Not Registered")
    viewed = models.BooleanField(default=False)
    shared = models.BooleanField(default=False)
    shared_by = models.CharField(max_length=100, null=True)
    shared_slug = models.SlugField(null=True, max_length=300)

    class Meta(object):
        ordering = ['-created_at', '-updated_at']
        verbose_name = "Signal"
        verbose_name_plural = "Signals"
        permissions = settings.PERMISSIONS_RELATED_TO_SIGNAL

    def __str__(self):
        return " : ".join(["{}".format(x) for x in [self.name, self.slug, self.status, self.created_at]])

    def generate_slug(self):
        if not self.slug:
            self.slug = slugify(self.name + "-" + ''.join(
                random.choice(string.ascii_uppercase + string.digits) for _ in range(10)))

    def save(self, *args, **kwargs):
        self.generate_slug()
        super(Insight, self).save(*args, **kwargs)

    def create(self, *args, **kwargs):
        self.add_to_job(*args, **kwargs)

    def add_to_job(self, *args, **kwargs):

        jobConfig = self.generate_config(*args, **kwargs)

        job = job_submission(
            instance=self,
            jobConfig=jobConfig,
            job_type='master'
        )

        self.job = job
        if job is None:
            self.status = "FAILED"
        else:
            self.status = "INPROGRESS"

        self.save()

    def generate_config(self, *args, **kwargs):
        config = {
            "config": {}
        }
        advanced_settings = kwargs.get('advanced_settings')
        config['config']["FILE_SETTINGS"] = self.create_configuration_url_settings(advanced_settings=advanced_settings)
        #
        try:
            config['config']["COLUMN_SETTINGS"] = self.make_config_for_colum_setting()
        except:
            config['config']["COLUMN_SETTINGS"] = self.create_configuration_column_settings()
        config['config']["DATA_SOURCE"] = self.dataset.get_datasource_info()

        if 'advanced_settings' in kwargs:
            config['config']["ADVANCED_SETTINGS"] = kwargs.get('advanced_settings')
        else:
            config['config']["ADVANCED_SETTINGS"] = {}
        # config['config']["DATE_SETTINGS"] = self.create_configuration_filter_settings()
        # config['config']["META_HELPER"] = self.create_configuration_meta_data()

        self.config = json.dumps(config)
        self.save()
        return config

    def get_config(self):
        return json.loads(self.config)

    def make_config_for_colum_setting(self):
        config = self.get_config()
        return {
            'variableSelection': config['variableSelection']
        }

    def create_configuration_column_settings(self):
        analysis_type = [self.type]
        result_column = [self.target_column]

        ret = {
            'result_column': result_column,
            'analysis_type': analysis_type,
            'date_format': None,
        }

        get_config_from_config = self.get_config_from_config()
        meta_data_related_config = self.dataset.common_config()

        ret.update(get_config_from_config)
        ret.update(meta_data_related_config)
        return ret

    def get_config_from_config(self):
        config = json.loads(self.config)
        consider_columns_type = ['including']
        data_columns = config.get("timeDimension", None)

        if data_columns is None:
            consider_columns = config.get('dimension', []) + config.get('measures', [])
            data_columns = ""
        else:
            if data_columns is "":
                consider_columns = config.get('dimension', []) + config.get('measures', [])
            else:
                consider_columns = config.get('dimension', []) + config.get('measures', []) + [data_columns]

        if len(consider_columns) < 1:
            consider_columns_type = ['excluding']

        ret = {
            'consider_columns_type': consider_columns_type,
            'consider_columns': consider_columns,
            'date_columns': [] if data_columns is "" else [data_columns],
            'customAnalysisDetails': config.get('customAnalysisDetails', []),
            'polarity': config.get('polarity', [])
        }
        return ret

    def create_configuration_url_settings(self, advanced_settings):
        default_scripts_to_run = [
            'Descriptive analysis',
            'Measure vs. Dimension',
            'Dimension vs. Dimension',
            'Trend'
        ]

        from django.conf import settings
        REVERSE_ANALYSIS_LIST = settings.REVERSE_ANALYSIS_LIST

        script_to_run = []
        analysis = advanced_settings['analysis']
        for data in analysis:
            if data['status'] == True:
                script_to_run.append(REVERSE_ANALYSIS_LIST[data['name']])

        if len(script_to_run) < 1:
            script_to_run = default_scripts_to_run

        return {
            'script_to_run': script_to_run,
            'inputfile': [self.dataset.get_input_file()],
            'metadata': self.dataset.get_metadata_url_config()
        }

    def create_configuration_filter_settings(self):
        return {}

    def create_configuration_meta_data(self):
        return {}

    def get_list_of_scripts_to_run(self, analysis_list):
        analysis_list_sequence = settings.ANALYSIS_LIST_SEQUENCE
        temp_list = []
        for item in analysis_list_sequence:
            if item in analysis_list:
                temp_list.append(item)
        return temp_list

    def get_variable_details_from_variable_selection(self):
        config = self.get_config()
        COLUMN_SETTINGS = config['config']['COLUMN_SETTINGS']
        variableSelection = COLUMN_SETTINGS.get('variableSelection')

        variable_selected = []
        analysis_type = []

        for variables in variableSelection:
            if 'targetColumn' in variables:
                if variables['targetColumn'] is True:
                    variable_selected.append(variables['name'])
                    analysis_type.append(variables['columnType'])
                    break

        return {
            'variable selected': variable_selected,
            'variable type': analysis_type
        }

    def get_brief_info(self):
        brief_info = dict()
        config = self.get_config()
        config = config.get('config')
        if config is not None:
            if 'COLUMN_SETTINGS' in config:
                try:
                    brief_info.update(self.get_variable_details_from_variable_selection())
                except:
                    column_settings = config['COLUMN_SETTINGS']
                    brief_info.update({
                        'variable selected': column_settings.get('result_column')[0],
                        'variable type': column_settings.get('analysis_type')[0]
                    })

            if 'FILE_SETTINGS' in config:
                file_setting = config['FILE_SETTINGS']
                try:
                    brief_info.update({
                        'analysis list': set(file_setting.get('script_to_run'))
                    })
                except:
                    brief_info.update({
                        'analysis list': []
                    })
        if self.shared is True:
            brief_info.update(
                {
                    'shared_by': self.shared_by,
                    'updated_at': self.updated_at,
                    'dataset': self.dataset.name
                }
            )
        else:
            brief_info.update(
                {
                    'created_by': self.created_by.username,
                    'updated_at': self.updated_at,
                    'dataset': self.dataset.name
                }
            )

        return convert_json_object_into_list_of_object(brief_info, 'signal')


def convert2native(dict_input):
    for k, v in dict_input.items():
        if isinstance(v, dict):
            v = convert2native(v)
        else:
            if v in ['true', 'True']:
                dict_input[k] = True
            if v in ['false', 'False']:
                dict_input[k] = False
            if v in ['none', 'None']:
                dict_input[k] = None
    return dict_input


class Trainer(models.Model):
    name = models.CharField(max_length=300, null=True)
    slug = models.SlugField(null=False, blank=True, max_length=300)
    dataset = models.ForeignKey(Dataset, null=False)
    column_data_raw = models.TextField(default="{}")
    config = models.TextField(default="{}")
    app_id = models.IntegerField(null=True, default=0)
    mode = models.CharField(max_length=10, null=True, blank=True)

    data = models.TextField(default="{}")
    fe_config = models.TextField(default="{}")

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    created_by = models.ForeignKey(User, null=False, db_index=True)
    deleted = models.BooleanField(default=False)

    bookmarked = models.BooleanField(default=False)
    analysis_done = models.BooleanField(default=False)

    job = models.ForeignKey(Job, null=True)
    status = models.CharField(max_length=100, null=True, default="Not Registered")
    live_status = models.CharField(max_length=300, default='0', choices=STATUS_CHOICES)
    viewed = models.BooleanField(default=False)
    email = models.EmailField(null=True, blank=True)
    shared = models.BooleanField(default=False)
    shared_by = models.CharField(max_length=100, null=True, blank=True)
    shared_slug = models.SlugField(null=True, max_length=300, blank=True)

    class Meta(object):
        ordering = ['-created_at', '-updated_at']
        permissions = settings.PERMISSIONS_RELATED_TO_TRAINER

    def __str__(self):
        return " : ".join(["{}".format(x) for x in [self.name, self.created_at, self.slug, self.app_id]])

    def generate_slug(self):
        if not self.slug:
            self.slug = slugify(self.name + "-" + ''.join(
                random.choice(string.ascii_uppercase + string.digits) for _ in range(10)))

    def save(self, *args, **kwargs):
        self.generate_slug()
        super(Trainer, self).save(*args, **kwargs)

    def create(self):
        self.add_to_job()

    def generate_config(self, *args, **kwargs):

        # changes in UI given config

        if self.mode == 'analyst':
            self.apply_changes_of_selectedVariables_into_variable_selection()

        config = {
            "config": {}
        }

        if self.mode == 'autoML':
            config['config']["TRAINER_MODE"] = "autoML"
            dataset_slug = self.dataset.slug
            # print "#############################"
            # print dataset_slug
            # print "#############################"
            self.get_targetColumn_for_variableSelection_autoML()
        else:
            config['config']["TRAINER_MODE"] = "analyst"
        # creating new config for ML/API using UI given config
        config['config']["FILE_SETTINGS"] = self.create_configuration_url_settings()

        try:
            config['config']["COLUMN_SETTINGS"] = self.make_config_for_colum_setting()
        except:
            config['config']["COLUMN_SETTINGS"] = self.create_configuration_column_settings()

        config['config']["DATA_SOURCE"] = self.dataset.get_datasource_info()
        # config['config']["DATE_SETTINGS"] = self.create_configuration_filter_settings()
        # config['config']["META_HELPER"] = self.create_configuration_meta_data()
        if (self.app_id in settings.REGRESSION_APP_ID):
            config['config']["ALGORITHM_SETTING"] = self.make_config_algorithm_setting()
        elif self.app_id in settings.CLASSIFICATION_APP_ID:
            config['config']["ALGORITHM_SETTING"] = self.make_config_algorithm_setting()

        # this part is related to FS
        if self.mode == 'autoML':
            from config.settings import feature_engineering_settings
            fe_default_settings = copy.deepcopy(feature_engineering_settings.feature_engineering_ml_settings)
            dc_default_settings = copy.deepcopy(feature_engineering_settings.data_cleansing_final_config_format)
            config['config']['FEATURE_SETTINGS'] = {"DATA_CLEANSING": dc_default_settings,
                                                    "FEATURE_ENGINEERING": fe_default_settings}
        else:
            config['config']['FEATURE_SETTINGS'] = self.create_configuration_fe_settings()

        # we are updating ColumnsSetting using add_newly_generated_column_names calculated in create_configuration_fe_settings
        try:
            configUI = self.get_config()
            configAPI = self.dataset.get_config()
            try:
                if 'TENSORFLOW' in configUI:
                    if (self.app_id in settings.REGRESSION_APP_ID):
                        config['config']["ALGORITHM_SETTING"][4].update({'tensorflow_params': configUI['TENSORFLOW']})
                    elif self.app_id in settings.CLASSIFICATION_APP_ID:
                        if config['config']["ALGORITHM_SETTING"][4]["algorithmName"] == "Neural Network (TensorFlow)":
                            config['config']["ALGORITHM_SETTING"][4].update(
                                {'tensorflow_params': configUI['TENSORFLOW']})
                        else:
                            config['config']["ALGORITHM_SETTING"][5].update(
                                {'tensorflow_params': configUI['TENSORFLOW']})
                if 'nnptc_parameters' in config['config']["ALGORITHM_SETTING"][6]:
                    config['config']["ALGORITHM_SETTING"][6]['nnptc_parameters'] = convert2native(
                        config['config']["ALGORITHM_SETTING"][6]['nnptc_parameters'])
            except Exception as err:
                print("Error adding Tesorflow Selection to Algorithm")
                print(err)
            # Unselect original
            if 'featureEngineering' in configUI:
                for colSlug in self.collect_column_slugs_which_all_got_transformations:
                    for i in config['config']['COLUMN_SETTINGS']['variableSelection']:
                        if i['slug'] == colSlug:
                            print(colSlug)
                            i['selected'] = False
                            break
                config['config']['COLUMN_SETTINGS']['variableSelection'] += self.add_newly_generated_column_names

            # Updating datatypes
            if 'newDataType' in configUI:
                for colSlug in configUI['newDataType']:
                    for i in config['config']['COLUMN_SETTINGS']['variableSelection']:
                        if i['slug'] == colSlug:
                            i['columnType'] = configUI['newDataType'][colSlug]['newColType']
                            break

            # Select or not to Select columns on basis of selectedVariables given on UI config
            if 'selectedVariables' in configUI:
                for colSlug in configUI['selectedVariables']:
                    for i in config['config']['COLUMN_SETTINGS']['variableSelection']:
                        if i['slug'] == colSlug:

                            # If selectedVariable has got any transformation, it should be kept selected False. else True
                            if colSlug in self.collect_column_slugs_which_all_got_transformations:
                                pass
                            else:
                                i['selected'] = configUI['selectedVariables'][colSlug]
                            break
            # Selected value to be True/False on basis of ignoreSuggestionFlag & ignoreSuggestionPreviewFlag
            if 'featureEngineering' in configUI:
                if len(configUI['selectedVariables']) > 0:
                    for SV_slug in configUI['selectedVariables']:
                        # if user perform featureEngineering actions
                        if len(configUI['featureEngineering']['columnsSettings']) > 0:
                            for fe_slug in configUI['featureEngineering']['columnsSettings']:
                                if SV_slug == fe_slug:
                                    pass
                                else:
                                    for i in configAPI['columnData']:
                                        if SV_slug == i['slug']:
                                            if i['ignoreSuggestionFlag'] == True and i[
                                                'ignoreSuggestionPreviewFlag'] == False:
                                                for colSlug in config['config']['COLUMN_SETTINGS']['variableSelection']:
                                                    if colSlug['slug'] == i['slug']:
                                                        colSlug['selected'] = False
                                            else:
                                                pass
                        # if featureEngineering config is empty
                        else:
                            for i in configAPI['columnData']:
                                if SV_slug == i['slug']:
                                    if i['ignoreSuggestionFlag'] == True and i['ignoreSuggestionPreviewFlag'] == False:
                                        for colSlug in config['config']['COLUMN_SETTINGS']['variableSelection']:
                                            if colSlug['slug'] == i['slug']:
                                                colSlug['selected'] = False
                # For AutoML mode when there will be no Selected Variables
                else:
                    for i in configAPI['columnData']:
                        if i['ignoreSuggestionFlag'] == True and i['ignoreSuggestionPreviewFlag'] == False:
                            for colSlug in config['config']['COLUMN_SETTINGS']['variableSelection']:
                                if colSlug['slug'] == i['slug']:
                                    colSlug['selected'] = False
                        else:
                            pass
            else:
                print("Feature featureEngineering config Not found !")
        except Exception as err:
            print(err)
            pass

        # first UI config was saved <-> this is ML config got saved in place of UI config
        self.config = json.dumps(config)
        self.save()
        return config

    # Changes to be done on variable_selection of UI given config before using it for ML/API config
    # In selectedVariables key of UI config, we selected/unselected columns
    def get_targetColumn_for_variableSelection_autoML(self):
        config = self.get_config()
        targetColumn = config['targetColumn']
        variablesSelection = config['variablesSelection']
        for variable in variablesSelection:
            if variable['name'] == targetColumn:
                variable['targetColumn'] = True
                break
        self.config = json.dumps(config)
        self.save()

    def apply_changes_of_selectedVariables_into_variable_selection(self):
        config = self.get_config()
        selectedVariables = config['selectedVariables']
        variablesSelection = config['variablesSelection']
        for col_slug in selectedVariables:
            for col_json in variablesSelection:
                if col_slug == col_json['slug']:
                    col_json['selected'] = selectedVariables[col_slug]
                    break
        self.config = json.dumps(config)
        self.save()

    def make_config_for_colum_setting(self):
        config = self.get_config()
        return {
            'variableSelection': config['variablesSelection']
        }

    def get_config_from_config(self):
        config = json.loads(self.config)
        consider_columns_type = ['including']
        data_columns = config.get("timeDimension", None)

        if data_columns is None:
            consider_columns = config.get('dimension', []) + config.get('measures', [])
            data_columns = ""
        else:
            if data_columns is "":
                consider_columns = config.get('dimension', []) + config.get('measures', [])
            else:
                consider_columns = config.get('dimension', []) + config.get('measures', []) + [data_columns]

        if len(consider_columns) < 1:
            consider_columns_type = ['excluding']

        ret = {
            'consider_columns_type': consider_columns_type,
            'consider_columns': consider_columns,
            'date_columns': [] if data_columns is "" else [data_columns],
        }
        return ret

    def create_configuration_url_settings(self):

        config = json.loads(self.config)
        targetLevel = None
        if 'targetLevel' in config:
            targetLevel = config.get('targetLevel')
        if (self.app_id in settings.REGRESSION_APP_ID):
            validationTechnique = config.get('validationTechnique')
            return {
                'inputfile': [self.dataset.get_input_file()],
                'modelpath': [self.slug],
                'validationTechnique': [validationTechnique],
                'analysis_type': ['training'],
                'metadata': self.dataset.get_metadata_url_config(),
                'targetLevel': targetLevel,
                'app_type': 'regression'
            }
        elif self.app_id in settings.CLASSIFICATION_APP_ID:

            validationTechnique = config.get('validationTechnique')
            return {
                'inputfile': [self.dataset.get_input_file()],
                'modelpath': [self.slug],
                'validationTechnique': [validationTechnique],
                'analysis_type': ['training'],
                'metadata': self.dataset.get_metadata_url_config(),
                'targetLevel': targetLevel,
                'app_type': 'classification'
            }

    def create_configuration_column_settings(self):
        config = json.loads(self.config)
        result_column = config.get('analysisVariable')

        ret = {
            'polarity': ['positive'],
            'result_column': [result_column],
            'date_format': None,
        }

        get_config_from_config = self.get_config_from_config()
        meta_data_related_config = self.dataset.common_config()

        ret.update(get_config_from_config)
        ret.update(meta_data_related_config)

        return ret

    def add_to_job(self, *args, **kwargs):
        jobConfig = self.generate_config(*args, **kwargs)

        job = job_submission(
            instance=self,
            jobConfig=jobConfig,
            job_type='model'
        )

        self.job = job
        if job is None:
            self.status = "FAILED"
        else:
            self.status = "INPROGRESS"
        self.save()

    def get_config(self):
        return json.loads(self.config)

    def get_variable_details_from_variable_selection(self):
        config = self.get_config()
        COLUMN_SETTINGS = config['config']['COLUMN_SETTINGS']
        variableSelection = COLUMN_SETTINGS.get('variableSelection')

        variable_selected = []

        for variables in variableSelection:
            if 'targetColumn' in variables:
                if variables['targetColumn'] is True:
                    variable_selected.append(variables['name'])
                    break

        return {
            'variable selected': variable_selected
        }

    def get_brief_info(self):
        brief_info = dict()
        config = self.get_config()
        config = config.get('config')
        if config is not None:
            if 'COLUMN_SETTINGS' in config:
                try:
                    brief_info.update(self.get_variable_details_from_variable_selection())
                except:
                    column_settings = config['COLUMN_SETTINGS']
                    brief_info.update({
                        'variable selected': column_settings.get('result_column')[0]
                    })

            if 'FILE_SETTINGS' in config:
                file_setting = config['FILE_SETTINGS']
                brief_info.update({
                    'analysis type': file_setting.get('analysis_type')[0],
                })

                if 'train_test_split' in file_setting:
                    brief_info.update({
                        'train_test_split': file_setting.get('train_test_split')[0]
                    })
                elif 'validationTechnique' in file_setting:
                    validationTechnique = file_setting.get('validationTechnique')[0]
                    valueKey = validationTechnique
                    brief_info.update({
                        valueKey['name']: valueKey['value']
                    })
                else:
                    brief_info.update({
                        'train_test_split': 0
                    })
        if self.shared is True:
            brief_info.update(
                {
                    'shared_by': self.shared_by,
                    'updated_at': self.updated_at,
                    'dataset': self.dataset.name
                }
            )
        else:
            brief_info.update(
                {
                    'created_by': self.created_by.username,
                    'updated_at': self.updated_at,
                    'dataset': self.dataset.name
                }
            )

        return convert_json_object_into_list_of_object(brief_info, 'trainer')

    def make_config_algorithm_setting(self):
        '''
        If grid search is True for an Algo.
        make metric_name  True in that Algo.
        :return:
        '''
        # config = self.get_config()

        # only checks if fit_intercept and solver has atleast something selected=True
        config = self.check_if_fit_intercept_is_true()

        if 'metric' in config:
            metric_name = config['metric']['name']
            for algo in config['ALGORITHM_SETTING']:
                for hps in algo['hyperParameterSetting']:
                    if hps['name'] == 'gridsearchcv':
                        if hps['selected'] == True:
                            params = hps['params']
                            if len(params) > 0:
                                params_0 = params[0]
                                if 'defaultValue' in params_0:
                                    default_value = params_0['defaultValue']
                                    for default in default_value:
                                        if default['name'] == metric_name:
                                            default['selected'] = True
                                            break

                            break

        return config['ALGORITHM_SETTING']

    def check_if_fit_intercept_is_true(self):
        '''
        If grid search is True for an Algo.
        make metric_name  True in that Algo.
        :return:
        '''
        config = self.get_config()

        for algo in config['ALGORITHM_SETTING']:

            # only checking for Neural Network
            if algo['algorithmName'] == 'Neural Network':
                # checking for learning_rate
                for params in algo['parameters']:
                    if params['name'] == 'learning_rate':
                        make_some_one_false = True
                        for default_values in params['defaultValue']:
                            if default_values['selected'] == True:
                                make_some_one_false = False
                                break
                        if make_some_one_false == True:
                            for default_values in params['defaultValue']:
                                default_values['selected'] = True
                                break

            for params in algo['parameters']:

                # checking for fit_intercept
                if params['name'] == 'fit_intercept':
                    make_some_one_false = True
                    for default_values in params['defaultValue']:
                        if default_values['selected'] == True:
                            make_some_one_false = False
                            break
                    if make_some_one_false == True:
                        for default_values in params['defaultValue']:
                            default_values['selected'] = True
                            break

                # checking for solver
                if params['name'] == 'solver':
                    make_some_one_false = True
                    for default_values in params['defaultValue']:
                        if default_values['selected'] == True:
                            make_some_one_false = False
                            break
                    if make_some_one_false == True:
                        for default_values in params['defaultValue']:
                            default_values['selected'] = True
                            break

                # checking for booster
                if params['name'] == 'booster':
                    make_some_one_false = True
                    for default_values in params['defaultValue']:
                        if default_values['selected'] == True:
                            make_some_one_false = False
                            break
                    if make_some_one_false == True:
                        for default_values in params['defaultValue']:
                            default_values['selected'] = True
                            break

                # checking for criterion
                if params['name'] == 'criterion':
                    make_some_one_false = True
                    for default_values in params['defaultValue']:
                        if default_values['selected'] == True:
                            make_some_one_false = False
                            break
                    if make_some_one_false == True:
                        for default_values in params['defaultValue']:
                            default_values['selected'] = True
                            break

                # checking for tree_method
                if params['name'] == 'tree_method':
                    make_some_one_false = True
                    for default_values in params['defaultValue']:
                        if default_values['selected'] == True:
                            make_some_one_false = False
                            break
                    if make_some_one_false == True:
                        for default_values in params['defaultValue']:
                            default_values['selected'] = True
                            break

                ## NEURAL NETWORK CONFIG PARAMETERS
                # checking for activation
                if params['name'] == 'activation':
                    make_some_one_false = True
                    for default_values in params['defaultValue']:
                        if default_values['selected'] == True:
                            make_some_one_false = False
                            break
                    if make_some_one_false == True:
                        for default_values in params['defaultValue']:
                            default_values['selected'] = True
                            break

                # checking for shuffle
                if params['name'] == 'shuffle':
                    make_some_one_false = True
                    for default_values in params['defaultValue']:
                        if default_values['selected'] == True:
                            make_some_one_false = False
                            break
                    if make_some_one_false == True:
                        for default_values in params['defaultValue']:
                            default_values['selected'] = True
                            break

                # checking for verbose
                if params['name'] == 'verbose':
                    make_some_one_false = True
                    for default_values in params['defaultValue']:
                        if default_values['selected'] == True:
                            make_some_one_false = False
                            break
                    if make_some_one_false == True:
                        for default_values in params['defaultValue']:
                            default_values['selected'] = True
                            break

                # checking for warm_start
                if params['name'] == 'warm_start':
                    make_some_one_false = True
                    for default_values in params['defaultValue']:
                        if default_values['selected'] == True:
                            make_some_one_false = False
                            break
                    if make_some_one_false == True:
                        for default_values in params['defaultValue']:
                            default_values['selected'] = True
                            break

                # checking for nesterovs_momentum
                if params['name'] == 'nesterovs_momentum':
                    make_some_one_false = True
                    for default_values in params['defaultValue']:
                        if default_values['selected'] == True:
                            make_some_one_false = False
                            break
                    if make_some_one_false == True:
                        for default_values in params['defaultValue']:
                            default_values['selected'] = True
                            break

                # checking for early_stopping
                if params['name'] == 'early_stopping':
                    make_some_one_false = True
                    for default_values in params['defaultValue']:
                        if default_values['selected'] == True:
                            make_some_one_false = False
                            break
                    if make_some_one_false == True:
                        for default_values in params['defaultValue']:
                            default_values['selected'] = True
                            break
        return config

    def create_configuration_fe_settings(self):
        config = self.get_config()
        data_cleansing_config = dict()
        feature_engineering_config = dict()
        variable_selection = config['variablesSelection']
        column_data = self.convert_variable_selection_config_into_dict(data=variable_selection)
        self.add_newly_generated_column_names = []
        self.collect_column_slugs_which_all_got_transformations = []
        if 'dataCleansing' in config:
            data_cleansing_config = self.data_cleansing_adaptor_for_ml(config['dataCleansing'], column_data)
        if 'featureEngineering' in config:
            feature_engineering_config = self.feature_engineering_config_for_ml(config['featureEngineering'],
                                                                                column_data)

        self.collect_column_slugs_which_all_got_transformations = list(
            set(self.collect_column_slugs_which_all_got_transformations))
        return {
            'DATA_CLEANSING': data_cleansing_config,
            'FEATURE_ENGINEERING': feature_engineering_config
        }

    def data_cleansing_adaptor_for_ml(self, data_cleansing_config_ui, column_data):
        '''
        sample json:
        data_cleansing_config = {
            "overall_settings": [
                {
                  "name": "duplicate_row",
                  "displayName": "Duplicate row treatment",
                  "selected": True,
                  "slug": ""
                },
                {
                  "name": "duplicate_column",
                  "displayName": "Duplicate columns treatment",
                  "selected": True,
                  "slug": ""
                }
            ],
            "columns_wise_settings": {
                "missing_value_treatment": {
                        "column_name1": {
                            "datatype": "measure",
                            "name": "mean_imputation",
                        },
                        "column_name2": {
                            "datatype": "measure",
                            "name": "mean_imputation",
                        }
                },
                "outlier_treatment":  {
                        "column_name1": {
                            "datatype": "measure",
                            "name": "mean_imputation",
                        },
                        "column_name2": {
                            "datatype": "measure",
                            "name": "mean_imputation",
                        }
                }

            }
        }

        '''

        from config.settings import feature_engineering_settings
        import copy
        data_cleansing = copy.deepcopy(feature_engineering_settings.data_cleansing_final_config_format)
        columns_wise_settings = data_cleansing['columns_wise_settings']
        overall_settings = data_cleansing['overall_settings']
        # pass
        columns_wise_data_ui = data_cleansing_config_ui['columnsSettings']

        # overall_settings
        if 'overallSettings' in data_cleansing_config_ui:

            overall_data = data_cleansing_config_ui['overallSettings']
            overall_settings_ui_ml_name_mapping = feature_engineering_settings.overall_settings_data_cleasing_ui_ml_mapping
            for d in overall_data:
                for i in overall_settings:
                    if i['name'] == overall_settings_ui_ml_name_mapping[d]:
                        if overall_data[d] == 'true' or overall_data[d] == True:
                            i['selected'] = True
                            data_cleansing['selected'] = True

        name_mapping = {
            'missingValueTreatment': 'missing_value_treatment',
            'outlierRemoval': 'outlier_removal'
        }

        # column_wise_settings
        for fkey in columns_wise_data_ui:
            columns_wise_data_f = columns_wise_data_ui[fkey]

            for slug in columns_wise_data_f:
                value = columns_wise_data_f[slug]

                column_name_as_per_variable_selection = column_data[slug]['name']
                if 'datatype' in value:
                    column_datatype = value['datatype']
                else:
                    column_datatype = column_data[slug]['columnType']

                column_dict = {
                    "name": column_name_as_per_variable_selection,
                    "datatype": column_datatype,
                    "mvt_value": 0,
                    "ol_lower_range": 0,
                    "ol_upper_range": 0,
                    "ol_lower_value": 0,
                    "ol_upper_value": 0
                }

                columns_wise_settings[name_mapping[fkey]]['selected'] = True
                data_cleansing['selected'] = True
                operations = columns_wise_settings[name_mapping[fkey]]['operations']
                print([op['name'] for op in operations])
                treatment = value['treatment']
                treatment = "_".join(treatment.split(' '))
                for op in operations:
                    if treatment == op['name']:
                        print('match')
                        op['selected'] = True
                        op['columns'].append(column_dict)

        data_cleansing['overall_settings'] = overall_settings
        return data_cleansing

    def convert_variable_selection_config_into_dict(self, data):
        new_dict = {}
        for item in data:
            name = item.pop('slug')
            new_dict[name] = item

        return new_dict

    def feature_engineering_config_for_ml(self, feature_engineering_config_ui, column_data):
        from config.settings import feature_engineering_settings
        import copy
        feature_engineering_ml_config = copy.deepcopy(feature_engineering_settings.feature_engineering_ml_settings)
        columns_wise_settings = feature_engineering_ml_config['column_wise_settings']
        overall_settings = feature_engineering_ml_config['overall_settings']
        transformation_settings = columns_wise_settings['transformation_settings']
        level_creation_settings = columns_wise_settings['level_creation_settings']

        columns_wise_data = feature_engineering_config_ui['columnsSettings']

        if 'overallSettings' in feature_engineering_config_ui:

            overall_data = feature_engineering_config_ui['overallSettings']

            # if 'yesNoValue' in overall_data and (overall_data['yesNoValue'] == True or overall_data['yesNoValue'] == 'true'):
            if 'yesNoValue' in overall_data:
                if overall_data['yesNoValue'] == True or overall_data['yesNoValue'] == 'true':
                    feature_engineering_ml_config['selected'] = True
                    overall_settings[0]['selected'] = True
                    if 'numberOfBins' in overall_data:
                        try:
                            overall_settings[0]['number_of_bins'] = int(overall_data['numberOfBins'])
                            for col in column_data:
                                if column_data[col]['columnType'] == 'measure' and column_data[col][
                                    'selected'] == True and column_data[col]['targetColumn'] == False:
                                    self.collect_column_slugs_which_all_got_transformations.append(col)
                                    self.generate_new_column_name_based_on_transformation(
                                        column_data[col],
                                        'binning_all_measures',
                                        # overall_data['numberOfBins']
                                    )
                        except Exception as err:
                            print(err)
        self.collect_column_slugs_which_all_got_transformations += list(columns_wise_data.keys())

        for slug in columns_wise_data:
            feature_engineering_ml_config['selected'] = True
            columns_wise_data_f = columns_wise_data[slug]

            for fkey in columns_wise_data_f:
                uiJson = columns_wise_data_f[fkey]

                if fkey == 'transformationData':
                    mlJson = self.transformationUiJsonToMLJsonAdapter(uiJson=uiJson,
                                                                      variable_selection_column_data=column_data[slug]
                                                                      )
                    self.add_to_feature_engineering_transformation_settings(transformation_settings, mlJson)

                if fkey == 'binData':
                    mlJson = self.binningAdapter(uiJson=uiJson,
                                                 variable_selection_column_data=column_data[slug]
                                                 )
                    self.add_to_feature_engineering_bin_creation_settings(level_creation_settings, mlJson)
                elif fkey == 'levelData':
                    mlJson, is_datetime_level = self.levelsAdapter(uiJson=uiJson,
                                                                   variable_selection_column_data=column_data[slug]
                                                                   )
                    self.add_to_feature_engineering_level_creation_settings(level_creation_settings, mlJson,
                                                                            is_datetime_level)

        return feature_engineering_ml_config

    def add_to_feature_engineering_transformation_settings(self, transformation_settings, mlJson):

        for transformation_function_names in mlJson:

            for op in transformation_settings['operations']:
                if op['name'] == transformation_function_names:
                    op['selected'] = True
                    op['columns'].append(mlJson[transformation_function_names])
                    transformation_settings['selected'] = True

    def add_to_feature_engineering_bin_creation_settings(self, level_creation_settings, mlJson):
        try:
            for key in level_creation_settings['operations']:
                if key['name'] == mlJson['selectBinType']:
                    level_creation_settings['selected'] = True
                    key['selected'] = True
                    key['columns'].append(mlJson['colStructure'])
        except:
            pass

    def add_to_feature_engineering_level_creation_settings(self, level_creation_settings, mlJson, is_datetime_level):

        try:
            for key in level_creation_settings['operations']:
                if key['name'] == 'create_new_levels' and is_datetime_level is False:
                    level_creation_settings['selected'] = True
                    key['selected'] = True
                    key['columns'].append(mlJson)
                if key['name'] == 'create_new_datetime_levels' and is_datetime_level is True:
                    level_creation_settings['selected'] = True
                    key['selected'] = True
                    key['columns'].append(mlJson)
        except:
            pass

    def transformationUiJsonToMLJsonAdapter(self, uiJson, variable_selection_column_data):
        mlJson = {}
        list_of_transformations = [
            # Measure Transformations
            "replace_values_with", "add_specific_value", "subtract_specific_value",
            "multiply_specific_value", "divide_specific_value",
            "perform_standardization", "variable_transformation",
            # Dimension Transformations
            "encoding_dimensions", "is_custom_string_in", "return_character_count", "feature_scaling",
            "is_date_weekend", "extract_time_feature", "time_since"
        ]

        for key in list_of_transformations:
            if key not in uiJson or uiJson[key] == False or uiJson[key] == "false":
                continue

            colStructure = {}
            user_given_name = ''
            # Measures Transformations

            if key == 'is_date_weekend':
                colStructure = {

                }
                user_given_name = self.generate_new_column_name_based_on_transformation(
                    variable_selection_column_data,
                    key
                )

            if key == 'extract_time_feature':
                colStructure = {
                    'time_feature_to_extract': uiJson.get("extract_time_feature_select", "day_of_week"),
                }
                user_given_name = self.generate_new_column_name_based_on_transformation(
                    variable_selection_column_data,
                    key,
                    str(uiJson.get("extract_time_feature_select", "day_of_week"))
                )

            if key == 'time_since':

                uiJson.get("time_since_input")
                time_since_input_date = None
                if "time_since_input" in uiJson:
                    try:
                        time_since_input_date = uiJson.get("time_since_input")
                        time_since_input_date = convert_fe_date_format(time_since_input_date)
                    except:
                        time_since_input_date = datetime.datetime.now().date().strftime('%d/%m/%Y')
                else:
                    time_since_input_date = datetime.datetime.now().date().strftime('%d/%m/%Y')
                colStructure = {
                    'time_since': time_since_input_date,
                }
                user_given_name = self.generate_new_column_name_based_on_transformation(
                    variable_selection_column_data,
                    key
                )

            if key == "replace_values_with":
                colStructure = {
                    "replace_by": uiJson.get("replace_values_with_selected", "Mean"),
                    "replace_value": uiJson.get("replace_values_with_input", 0)
                }
                user_given_name = self.generate_new_column_name_based_on_transformation(
                    variable_selection_column_data,
                    key,
                    str(uiJson.get("replace_values_with_input", 0)),
                    uiJson.get("replace_values_with_selected", "mean")
                )
            if key == "add_specific_value":
                colStructure = {
                    "value_to_be_added": uiJson.get("add_specific_value_input", 0),
                }
                user_given_name = self.generate_new_column_name_based_on_transformation(
                    variable_selection_column_data,
                    key,
                    str(uiJson.get("add_specific_value_input", 0))
                )
            if key == "subtract_specific_value":
                colStructure = {
                    "value_to_be_subtracted": uiJson.get("subtract_specific_value_input", 0),
                }

                user_given_name = self.generate_new_column_name_based_on_transformation(
                    variable_selection_column_data,
                    key,
                    str(uiJson.get("subtract_specific_value_input", 0))
                )
            if key == "multiply_specific_value":
                colStructure = {
                    "value_to_be_multiplied": uiJson.get("multiply_specific_value_input", 1),
                }
                user_given_name = self.generate_new_column_name_based_on_transformation(
                    variable_selection_column_data,
                    key,
                    str(uiJson.get("multiply_specific_value_input", 1))
                )

            if key == "divide_specific_value":
                colStructure = {
                    "value_to_be_divided": uiJson.get("divide_specific_value_input", 1),
                }
                user_given_name = self.generate_new_column_name_based_on_transformation(
                    variable_selection_column_data,
                    key,
                    str(uiJson.get("divide_specific_value_input", 1))
                )

            if key == "perform_standardization":
                colStructure = {
                    "standardization_type": uiJson.get("perform_standardization_select", "min_max_scaling"),
                }

                name_mapping = {
                    'standardization': 'standardized',
                    'normalization': 'normalized'
                }
                user_given_name = self.generate_new_column_name_based_on_transformation(
                    variable_selection_column_data,
                    key,
                    name_mapping[str(uiJson.get("perform_standardization_select", "min_max_scaling"))]
                )
            if key == "feature_scaling":
                key = "perform_standardization"
                colStructure = {
                    "standardization_type": uiJson.get("perform_standardization_select", "min_max_scaling"),
                }

                name_mapping = {
                    'standardization': 'standardized',
                    'normalization': 'normalized'
                }
                user_given_name = self.generate_new_column_name_based_on_transformation(
                    variable_selection_column_data,
                    key,
                    name_mapping[str(uiJson.get("perform_standardization_select", "min_max_scaling"))]
                )
            if key == "variable_transformation":
                colStructure = {
                    "transformation_type": uiJson.get("variable_transformation_select", "log_transformation"),
                }
                name_mapping = {
                    'log_transform': 'log_transformed',
                    'modulus_transform': 'modulus_transformed',
                    'cube_root_transform': 'cuberoot_transformed',
                    'square_root_transform': 'squareroot_transformed'
                }
                user_given_name = self.generate_new_column_name_based_on_transformation(
                    variable_selection_column_data,
                    key,
                    name_mapping[str(uiJson.get("variable_transformation_select", "log_transform"))]
                )
            # Dimensioins Transformations
            if key == "return_character_count":
                colStructure = {}
                user_given_name = self.generate_new_column_name_based_on_transformation(
                    variable_selection_column_data,
                    key
                )
            if key == "encoding_dimensions":
                colStructure = {
                    "encoding_type": uiJson.get("encoding_type", "one_hot_encoding"),
                }
                name_mapping = {
                    'one_hot_encoding': 'one_hot_encoded',
                    'label_encoding': 'label_encoded'
                }
                user_given_name = self.generate_new_column_name_based_on_transformation(
                    variable_selection_column_data,
                    key,
                    name_mapping[str(uiJson.get("encoding_type", "one_hot_encoding"))]
                )
            if key == "is_custom_string_in":
                colStructure = {
                    "user_given_string": uiJson.get("is_custom_string_in_input", "error"),
                }
                user_given_name = self.generate_new_column_name_based_on_transformation(
                    variable_selection_column_data,
                    key,
                    str(uiJson.get("is_custom_string_in_input", "error"))
                )

            colStructure["name"] = variable_selection_column_data['name']
            colStructure["user_given_name"] = user_given_name
            colStructure["datatype"] = variable_selection_column_data['columnType']
            mlJson[key] = colStructure
        return mlJson

    def binningAdapter(self, uiJson, variable_selection_column_data):
        '''
        columnName=column_data[slug]['name'],
        columnType=column_data[slug]['columnType']
        :param uiJson:
        :param columnName:
        :param columnType:
        :return:
        '''
        mlJson = {}

        if uiJson and "selectBinType" in uiJson:

            colStructure = {}
            colStructure["name"] = variable_selection_column_data['name']
            colStructure["datatype"] = variable_selection_column_data['columnType']
            mlJson['selectBinType'] = uiJson["selectBinType"]
            user_given_name = ""
            # Measures Transformations
            if uiJson["selectBinType"] == "create_equal_sized_bins":
                user_given_name = self.generate_new_column_name_based_on_transformation(
                    variable_selection_column_data,
                    uiJson["selectBinType"]
                )
                colStructure.update({
                    # "number_of_bins": int(uiJson.get("numberofbins", "10").strip()),
                    "number_of_bins": int(str(uiJson.get("numberofbins", "10")).strip()),
                    "user_given_name": user_given_name,
                    "actual_col_name": uiJson["newcolumnname"]
                })
                mlJson["colStructure"] = colStructure

            if uiJson["selectBinType"] == "create_custom_bins":
                user_given_name = self.generate_new_column_name_based_on_transformation(
                    variable_selection_column_data,
                    uiJson["selectBinType"]
                )
                colStructure.update({
                    "list_of_intervals": [int(token.strip()) for token in
                                          uiJson.get("specifyintervals", "").split(",")],
                    "user_given_name": user_given_name,
                    "actual_col_name": uiJson["newcolumnname"]
                })
                mlJson["colStructure"] = colStructure

        return mlJson

    def levelsAdapter(self, uiJson, variable_selection_column_data):

        is_datetime_level = False
        mlJson = {
            "name": variable_selection_column_data['name'],
            "datatype": variable_selection_column_data['columnType'],
            "user_given_name": '',
            "mapping_dict": {}
        }

        for item in uiJson:
            if "inputValue" in item and "multiselectValue" in item:
                if item['multiselectValue'] == '':
                    '''
                    if multiselectValue is "" , then this is a datetime thing
                    convert this start_date/endDate from yyyy-mm-dd to dd/mm/yyyy
                    save it back in start_date/endDate
                    '''
                    start_date = convert_fe_date_format(item['startDate'])
                    end_date = convert_fe_date_format(item['endDate'])
                    mlJson["mapping_dict"][item["inputValue"]] = [start_date, end_date]
                    is_datetime_level = True
                else:
                    is_datetime_level = False
                    mlJson["mapping_dict"][item["inputValue"]] = item["multiselectValue"]

        if is_datetime_level is True:
            user_given_name = self.generate_new_column_name_based_on_transformation(
                variable_selection_column_data,
                'create_new_datetime_levels'
            )
        else:
            user_given_name = self.generate_new_column_name_based_on_transformation(
                variable_selection_column_data,
                'create_new_levels'
            )

        mlJson['user_given_name'] = user_given_name

        return mlJson, is_datetime_level

    def generate_new_column_name_based_on_transformation(self, variable_selection_column_data, function_name, *args):

        name_mapping = {
            'create_equal_sized_bins': {
                'name': 'bin',
                'type': 'dimension'
            },
            'create_custom_bins': {
                'name': 'c_bin',
                'type': 'dimension'
            },
            'create_new_levels': {
                'name': 'level',
                'type': 'dimension'
            },
            'create_new_datetime_levels': {
                'name': 't_level',
                'type': 'dimension'
            },
            'replace_values_with': {
                'name': 'treated',
                'type': 'measure'
            },
            'variable_transformation': {
                'name': 'vt',
                'type': 'measure'
            },
            'label_encoding': {
                'name': 'le',
                'type': 'dimension'
            },
            'onehot_encoding': {
                'name': 'onehot_encoded',
                'type': 'dimension'
            },
            'return_character_count': {
                'name': 'character_count',
                'type': 'measure'
            },
            'is_custom_string_in': {
                'name': 'contains',
                'type': 'dimension'
            },
            'is_date_weekend': {
                'name': 'is_weekend',
                'type': 'boolean'
            },
            'extract_time_feature': {
                'name': 'etf',
                'type': 'dimension'
            },
            'time_since': {
                'name': 'time_since',
                'type': 'measure'
            },
            'standardization': {
                'name': 'fs',
                'type': 'measure'
            },
            'normalization': {
                'name': 'normalized',
                'type': 'measure'
            },
            'encoding_dimensions': {
                'name': 'ed',
                'type': 'measure'
            },
            'binning_all_measures': {
                'name': 'bin',
                'type': 'dimension'
            },
            'perform_standardization': {
                'name': 'fs',
                'type': 'measure'
            },
            'feature_scaling': {
                'name': 'fs',
                'type': 'measure'
            }
        }
        original_col_nam = variable_selection_column_data['name']
        if function_name in name_mapping:
            new_name = "_".join([original_col_nam, name_mapping[function_name]['name']] + list(args))
        else:
            new_name = "_".join([original_col_nam, function_name] + list(args))
        self.add_newly_generated_column_names_into_column_settings(
            newly_generated_column_name=new_name,
            columnType=name_mapping[function_name]['type'],
            variable_selection_column_data=variable_selection_column_data,
            original_column_name=original_col_nam
        )

        return new_name

    def add_newly_generated_column_names_into_column_settings(self,
                                                              newly_generated_column_name,
                                                              columnType,
                                                              variable_selection_column_data,
                                                              original_column_name
                                                              ):
        remove_these = ['name', 'columnType', 'actualColumnType', 'selected']
        temp = copy.deepcopy(variable_selection_column_data)
        for i in remove_these:
            del temp[i]
        slug = slugify(self.name + "-" + ''.join(
            random.choice(string.ascii_uppercase + string.digits) for _ in range(10)))
        custom_dict = {
            'columnType': columnType,
            'actualColumnType': columnType,
            'originalColumnName': original_column_name,
            'name': newly_generated_column_name,
            'selected': True,
            'slug': slug,
            'isFeatureColumn': True
        }
        custom_dict.update(temp)
        custom_dict['dateSuggestionFlag'] = False
        self.add_newly_generated_column_names.append(custom_dict)

    def delete(self):
        try:
            self.deleted = True
            self.save()
            train_algo_instance = TrainAlgorithmMapping.objects.filter(trainer_id=self.id)
            for iter in train_algo_instance:
                iter.delete()

        except Exception as err:
            print(err)


# TODO: Add generate config
# TODO: Add set_result function: it will be contain many things.
class Score(models.Model):
    name = models.CharField(max_length=300, null=True)
    slug = models.SlugField(null=False, blank=True, max_length=300)
    trainer = models.ForeignKey(Trainer, null=False)
    dataset = models.ForeignKey(Dataset, null=False, default="")
    config = models.TextField(default="{}")
    data = models.TextField(default="{}")
    model_data = models.TextField(default="{}")
    column_data_raw = models.TextField(default="{}")
    app_id = models.IntegerField(null=True, default=1)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    created_by = models.ForeignKey(User, null=False, db_index=True)
    deleted = models.BooleanField(default=False)
    analysis_done = models.BooleanField(default=False)

    bookmarked = models.BooleanField(default=False)

    job = models.ForeignKey(Job, null=True)
    status = models.CharField(max_length=100, null=True, default="Not Registered")
    live_status = models.CharField(max_length=300, default='0', choices=STATUS_CHOICES)
    viewed = models.BooleanField(default=False)
    shared = models.BooleanField(default=False)
    shared_by = models.CharField(max_length=100, null=True)
    shared_slug = models.SlugField(null=True, max_length=300)

    class Meta(object):
        ordering = ['-created_at', '-updated_at']
        permissions = settings.PERMISSIONS_RELATED_TO_SCORE

    def __str__(self):
        return " : ".join(["{}".format(x) for x in [self.name, self.created_at, self.slug, self.trainer]])

    def generate_slug(self):
        if not self.slug:
            self.slug = slugify(self.name + "-" + ''.join(
                random.choice(string.ascii_uppercase + string.digits) for _ in range(10)))

    def save(self, *args, **kwargs):
        self.generate_slug()
        super(Score, self).save(*args, **kwargs)

    def create(self):
        self.add_to_job()

    def add_to_job(self, *args, **kwargs):
        jobConfig = self.generate_config(*args, **kwargs)
        job = job_submission(
            instance=self,
            jobConfig=jobConfig,
            job_type='score'
        )
        self.job = job
        if job is None:
            self.status = "FAILED"
        else:
            self.status = "INPROGRESS"
        self.save()

    def generate_config(self, *args, **kwargs):
        config = {
            "config": {}
        }

        config['config']["FILE_SETTINGS"] = self.create_configuration_url_settings()
        # try:
        config['config']["COLUMN_SETTINGS"] = self.create_configuration_for_column_setting_from_variable_selection()
        # except:
        #     config['config']["COLUMN_SETTINGS"] = self.create_configuration_column_settings()
        config['config']["DATA_SOURCE"] = self.dataset.get_datasource_info()
        # config['config']["DATE_SETTINGS"] = self.create_configuration_filter_settings()
        # config['config']["META_HELPER"] = self.create_configuration_meta_data()
        config['config']['FEATURE_SETTINGS'] = self.get_trainer_feature_settings()
        try:
            config['config']['one_click'] = json.loads(self.trainer.fe_config)
        except Exception as e:
            print('Could not add one click config as {}'.format(e))

        if self.trainer.mode == "autoML":
            config['config']["TRAINER_MODE"] = "autoML"
        else:
            config['config']["TRAINER_MODE"] = "analyst"

        self.config = json.dumps(config)
        self.save()
        return config

    def create_configuration_url_settings(self):

        config = json.loads(self.config)
        selectedModel = config['selectedModel']
        algorithmslug = selectedModel.get('slug')

        trainer_slug = self.trainer.slug
        score_slug = self.slug
        model_data = json.loads(self.trainer.data)
        model_config = json.loads(self.trainer.config)
        model_config_from_results = model_data['config']
        targetVariableLevelcount = model_config_from_results.get('targetVariableLevelcount', None)
        modelFeaturesDict = model_config_from_results.get('modelFeatures', None)
        labelMappingDictAll = model_config_from_results.get('labelMappingDict', None)
        modelTargetLevel = model_config['config']['FILE_SETTINGS']['targetLevel']

        modelfeatures = modelFeaturesDict.get(algorithmslug, None)
        if labelMappingDictAll != None:
            labelMappingDict = labelMappingDictAll.get(algorithmslug, None)
        else:
            labelMappingDict = None

        return {
            'inputfile': [self.dataset.get_input_file()],
            'modelpath': [trainer_slug],
            'selectedModel': [selectedModel],
            'scorepath': [score_slug],
            'analysis_type': ['score'],
            'levelcounts': targetVariableLevelcount if targetVariableLevelcount is not None else [],
            'algorithmslug': [algorithmslug],
            'modelfeatures': modelfeatures if modelfeatures is not None else [],
            'metadata': self.dataset.get_metadata_url_config(),
            'labelMappingDict': [labelMappingDict],
            'targetLevel': modelTargetLevel
        }

    def create_configuration_for_column_setting_from_variable_selection(self):
        # Trainer related variable selection

        trainer_config = json.loads(self.trainer.config)
        trainer_config_config = trainer_config.get('config')
        trainer_column_setting_config = trainer_config_config.get('COLUMN_SETTINGS')
        trainer_variable_selection_config = trainer_column_setting_config.get('variableSelection')

        # Score related variable selection
        main_config = json.loads(self.config)

        score_variable_selection_config = main_config.get('variablesSelection')
        output = {
            'modelvariableSelection': trainer_variable_selection_config,
            'variableSelection': score_variable_selection_config
        }
        return output

    def get_config_from_config(self):
        trainer_config = json.loads(self.trainer.config)
        trainer_config_config = trainer_config.get('config')
        file_column_config = trainer_config_config.get('COLUMN_SETTINGS')
        trainer_consider_column_type = file_column_config.get('consider_columns_type')
        trainer_consider_columns = file_column_config.get('consider_columns')

        config = json.loads(self.config)
        consider_columns_type = ['including']
        data_columns = config.get("timeDimension", None)

        if data_columns is None:
            consider_columns = config.get('dimension', []) + config.get('measures', [])
            data_columns = ""
        else:
            if data_columns is "":
                consider_columns = config.get('dimension', []) + config.get('measures', [])
            else:
                consider_columns = config.get('dimension', []) + config.get('measures', []) + [data_columns]

        if len(consider_columns) < 1:
            consider_columns_type = ['excluding']

        # app_id = config.get('app_id', 1)
        app_id = self.trainer.app_id
        self.app_id = app_id
        self.save()

        ret = {
            'consider_columns_type': trainer_consider_column_type,
            'consider_columns': trainer_consider_columns,
            'score_consider_columns_type': consider_columns_type,
            'score_consider_columns': consider_columns,
            'date_columns': [] if data_columns is "" else [data_columns],
            'app_id': [app_id]
        }
        return ret

    def create_configuration_column_settings(self):
        config = json.loads(self.config)
        model_data = json.loads(self.trainer.data)
        model_config_from_results = model_data['config']
        result_column = model_config_from_results.get('target_variable')[0]

        ret = {
            'polarity': ['positive'],
            'result_column': [result_column],
            'date_format': None,
        }

        get_config_from_config = self.get_config_from_config()
        meta_data_related_config = self.dataset.common_config()

        ret.update(get_config_from_config)
        ret.update(meta_data_related_config)

        return ret

    def get_trainer_feature_settings(self):
        model_config = json.loads(self.trainer.config)
        model_config_feature_settings = model_config['config']['FEATURE_SETTINGS']
        return model_config_feature_settings

    def get_local_file_path(self):
        return '/tmp/' + self.slug

    def get_config(self):

        return json.loads(self.config)

    def get_variable_details_from_variable_selection(self):
        config = self.get_config()
        COLUMN_SETTINGS = config['config']['COLUMN_SETTINGS']
        variableSelection = COLUMN_SETTINGS.get('variableSelection')

        variable_selected = []

        for variables in variableSelection:
            if 'targetColumn' in variables:
                if variables['targetColumn'] is True:
                    variable_selected.append(variables['name'])
                    break

        return {
            'variable selected': variable_selected
        }

    def get_brief_info(self):
        brief_info = dict()
        config = self.get_config()
        config = config.get('config')

        model_data = json.loads(self.trainer.data)
        if 'model_dropdown' in model_data:
            model_config_from_results = model_data['model_dropdown']
        else:
            model_config_from_results = []

        if config is not None:
            if 'COLUMN_SETTINGS' in config:
                try:
                    brief_info.update(self.trainer.get_variable_details_from_variable_selection())
                except:
                    column_settings = config['COLUMN_SETTINGS']
                    brief_info.update({
                        'variable selected': column_settings.get('result_column')[0]
                    })

            if 'FILE_SETTINGS' in config:
                file_setting = config['FILE_SETTINGS']
                algorithm_name = None
                for slug_name in model_config_from_results:
                    if slug_name['slug'] == file_setting.get('algorithmslug')[0]:
                        algorithm_name = slug_name['name']
                        break

                brief_info.update({
                    'analysis type': file_setting.get('analysis_type')[0],
                    'algorithm name': algorithm_name,
                })

        if self.shared is True:
            brief_info.update(
                {
                    'shared_by': self.shared_by,
                    'updated_at': self.updated_at,
                    'dataset': self.dataset.name,
                    'model': self.trainer.name
                }
            )
        else:
            brief_info.update(
                {
                    'created_by': self.created_by.username,
                    'updated_at': self.updated_at,
                    'dataset': self.dataset.name,
                    'model': self.trainer.name
                }
            )

        return convert_json_object_into_list_of_object(brief_info, 'score')


class Robo(models.Model):
    name = models.CharField(max_length=300, default="", blank=True)
    slug = models.SlugField(null=False, blank=True, max_length=300)

    customer_dataset = models.ForeignKey(Dataset, null=False, default="", related_name='customer_dataset')
    historical_dataset = models.ForeignKey(Dataset, null=False, default="", related_name='historical_dataset')
    market_dataset = models.ForeignKey(Dataset, null=False, default="", related_name='market_dataset')

    config = models.TextField(default="{}")
    data = models.TextField(default="{}")
    column_data_raw = models.TextField(default="{}")

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    created_by = models.ForeignKey(User, null=False)
    deleted = models.BooleanField(default=False)
    analysis_done = models.BooleanField(default=False)
    dataset_analysis_done = models.BooleanField(default=False)
    robo_analysis_done = models.BooleanField(default=True)

    bookmarked = models.BooleanField(default=False)
    job = models.ForeignKey(Job, null=True)
    status = models.CharField(max_length=100, null=True, default="Not Registered")
    live_status = models.CharField(max_length=300, default='0', choices=STATUS_CHOICES)
    viewed = models.BooleanField(default=False)

    class Meta(object):
        ordering = ['-created_at', '-updated_at']
        # permissions = settings.NEW_PERMISSIONS

    def __str__(self):
        return " : ".join(["{}".format(x) for x in [self.name, self.created_at, self.slug]])

    def generate_slug(self):
        if not self.slug:
            self.slug = slugify(self.name + "-" + ''.join(
                random.choice(string.ascii_uppercase + string.digits) for _ in range(10)))

    def save(self, *args, **kwargs):
        self.generate_slug()
        super(Robo, self).save(*args, **kwargs)

    def create(self, *args, **kwargs):
        # self.add_to_job()
        pass

    def generate_config(self, *args, **kwargs):
        return {

        }

    def add_to_job(self, *args, **kwargs):
        jobConfig = self.generate_config(*args, **kwargs)

        job = job_submission(
            instance=self,
            jobConfig=jobConfig,
            job_type='robo'
        )

        self.job = job
        if job is None:
            self.status = "FAILED"
        else:
            self.status = "INPROGRESS"
        self.save()

    def get_brief_info(self):
        brief_info = dict()
        customer_dataset_name = ""
        historical_dataset_name = ""
        market_dataset_name = ""
        try:
            customer_dataset_name = self.customer_dataset.name
        except:
            pass
        try:
            historical_dataset_name = self.historical_dataset.name
        except:
            pass
        try:
            market_dataset_name = self.market_dataset.name
        except:
            pass

        brief_info.update(
            {
                'created_by': self.created_by.username,
                'updated_at': self.updated_at,
                'customer_dataset': customer_dataset_name,
                'historical_dataset': historical_dataset_name,
                'market_dataset': market_dataset_name
            }
        )

        return convert_json_object_into_list_of_object(brief_info, 'robo')


class CustomApps(models.Model):
    app_id = models.IntegerField(null=False)
    name = models.CharField(max_length=300, null=False, default="App")
    slug = models.SlugField(null=False, blank=True, max_length=300)
    displayName = models.CharField(max_length=300, null=True, default="App")
    description = models.CharField(max_length=300, null=True)
    tags = models.CharField(max_length=500, null=True)
    iconName = models.CharField(max_length=300, null=True)
    app_url = models.CharField(max_length=300, null=True)
    # data = models.TextField(default="{}")
    # model_data = models.TextField(default="{}")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    # updated_at = models.DateTimeField(auto_now=True, null=True)
    created_by = models.ForeignKey(User, null=False)
    # deleted = models.BooleanField(default=False)
    status = models.CharField(max_length=100, null=True, default="Inactive")
    live_status = models.CharField(max_length=300, default='0', choices=STATUS_CHOICES)
    viewed = models.BooleanField(default=False)
    app_type = models.CharField(max_length=300, null=True, default="")
    rank = models.IntegerField(unique=True, null=True)

    class Meta(object):
        ordering = ['rank']

    def __str__(self):
        return " : ".join(["{}".format(x) for x in [self.name, self.slug, self.app_id]])

    def generate_slug(self):
        if not self.slug:
            self.slug = slugify(self.name + "-" + ''.join(
                random.choice(string.ascii_uppercase + string.digits) for _ in range(10)))

    def save(self, *args, **kwargs):
        self.generate_slug()
        super(CustomApps, self).save(*args, **kwargs)

    def create(self, *args, **kwargs):
        self.add_to_job()

    def generate_config(self, *args, **kwargs):
        return {

        }

    def add_to_job(self, *args, **kwargs):
        # jobConfig = self.generate_config(*args, **kwargs)

        # job = job_submission(
        #     instance=self,
        #     jobConfig=jobConfig,
        #     job_type='robo'
        # )
        #
        # self.job = job
        # if job is None:
        #     self.status = "FAILED"
        # else:
        #     self.status = "INPROGRESS"
        self.status = "Active"
        self.save()

        # def get_brief_info(self):
        #     brief_info = dict()
        #     brief_info.update(
        #         {
        #             'created_by': self.created_by.username,
        #         })
        #     return convert_json_object_into_list_of_object(brief_info, 'apps')

    def adjust_rank(self, index):
        self.rank = index
        self.save()

    def null_the_rank(self):
        self.rank = None
        self.save()


class CustomAppsUserMapping(models.Model):
    user = models.ForeignKey(User)
    app = models.ForeignKey(CustomApps)
    active = models.BooleanField(default=True)
    rank = models.IntegerField(null=True)

    class Meta(object):
        unique_together = (('user', 'app'),)


auditlog.register(Dataset)
auditlog.register(Insight)
auditlog.register(Score)
auditlog.register(Robo)
auditlog.register(Trainer)
auditlog.register(CustomApps)


def job_submission(instance=None, jobConfig=None, job_type=None):
    """Submit job to jobserver"""
    # Job Book Keeping
    job = Job()
    job.name = "-".join([job_type, instance.slug])
    job.job_type = job_type
    job.object_id = str(instance.slug)
    job.submitted_by = instance.created_by

    if jobConfig is None:
        jobConfig = json.loads(instance.config)
    job.config = json.dumps(jobConfig)
    if 'stockAdvisor' == job_type:
        from api.helper import create_message_log_and_message_for_stocksense
        job.message_log, job.messages = create_message_log_and_message_for_stocksense(instance.stock_symbols)
    job.save()
    queue_name = None
    try:
        data_size = None
        if job_type in ['metadata', 'subSetting']:
            data_size = instance.get_number_of_row_size()
        elif job_type in ['master', 'model', 'score']:
            data_size = instance.dataset.get_number_of_row_size()
        else:
            data_size = 3000

        queue_name = get_queue_to_use(job_type=job_type, data_size=data_size)
    except Exception as e:
        print(e)

    if not queue_name:
        queue_name = "default"

    from api.redis_access import AccessFeedbackMessage
    ac = AccessFeedbackMessage()
    message_slug = get_message_slug(job)
    ac.delete_this_key(message_slug)
    app_id = None
    if 'score' == job_type:
        app_id = instance.app_id
    elif 'model' == job_type:
        app_id = instance.app_id
    '''
    job_type = {
            "metadata": "metaData",
            "master": "story",
            "model":"training",
            "score": "prediction",
            "robo": "robo",
            "subSetting": "subSetting",
            "stockAdvisor": "stockAdvisor"
        }
    '''
    # Submitting JobServer
    from .utils import submit_job
    try:
        job_return_data = submit_job(
            slug=job.slug,
            class_name=job_type,
            job_config=jobConfig,
            job_name=instance.name,
            message_slug=message_slug,
            queue_name=queue_name,
            app_id=app_id
        )

        job.url = job_return_data.get('application_id')
        job.command_array = json.dumps(job_return_data.get('command_array'))

        readable_job_config = {
            'job_config': job_return_data.get('config')['job_config']['job_config'],
            'config': job_return_data.get('config')['job_config']['config']
        }
        job.config = json.dumps(readable_job_config)
        job.save()
    except Exception as exc:
        # send_alert_through_email(exc)
        return None

    return job


def get_queue_deployment_env_name():
    return settings.DEPLOYMENT_ENV


def get_queue_job_type_name(job_type):
    return "." + get_queue_deployment_env_name() + '-' + settings.YARN_QUEUE_NAMES.get(job_type)


def get_queue_to_use(job_type, data_size=None):
    if settings.USE_YARN_DEFAULT_QUEUE:
        return "default"
    else:
        return get_queue_deployment_env_name() + '-' + settings.YARN_QUEUE_NAMES.get(job_type) + get_queue_size_name(
            job_type, data_size)


def get_queue_size_name(job_type, data_size):
    job_type = job_type.lower()
    if job_type in ['metadata', 'subsetting', 'score', 'stockadvisor']:
        return ''

    data_size_name = None
    if data_size < settings.DATASET_ROW_SIZE_LIMITS.get('small'):
        data_size_name = 'small'
    elif data_size < settings.DATASET_ROW_SIZE_LIMITS.get('medium'):
        data_size_name = 'medium'
    else:
        data_size_name = 'large'
    if data_size_name:
        return "-" + data_size_name
    else:
        return ''


def get_message_slug(instance):
    from api.redis_access import AccessFeedbackMessage
    ac = AccessFeedbackMessage()
    slug = ac.get_cache_name(instance)
    return slug


def get_slug_from_message_url(url):
    split_with_underscore = url.split('_')
    return "_".join(split_with_underscore[1:-1])


class StockDataset(models.Model):
    name = models.CharField(max_length=100, null=True)
    stock_symbols = models.CharField(max_length=500, null=True, blank=True)
    domains = models.CharField(max_length=500, null=True, blank=True, default='')
    start_date = models.DateTimeField(auto_now_add=False, null=True)
    slug = models.SlugField(null=True, max_length=300)
    auto_update = models.BooleanField(default=False)

    input_file = models.FileField(upload_to='conceptsfiles', null=True)

    meta_data = models.TextField(default="{}")
    data = models.TextField(default="{}")

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    created_by = models.ForeignKey(User, null=False)
    deleted = models.BooleanField(default=False)
    bookmarked = models.BooleanField(default=False)

    job = models.ForeignKey(Job, null=True)
    analysis_done = models.BooleanField(default=False)
    status = models.CharField(max_length=100, null=True, default="Not Registered")
    live_status = models.CharField(max_length=300, default='0', choices=STATUS_CHOICES)
    viewed = models.BooleanField(default=False)

    crawled_data = models.TextField(default="{}")

    class Meta(object):
        ordering = ['-created_at', '-updated_at']
        permissions = settings.PERMISSIONS_RELATED_TO_STOCK

    def __str__(self):
        return " : ".join(["{}".format(x) for x in [self.name, self.slug]])

    def generate_slug(self):
        if not self.slug:
            self.slug = slugify(str(self.name) + "-" + ''.join(
                random.choice(string.ascii_uppercase + string.digits) for _ in range(10)))

    def save(self, *args, **kwargs):
        self.generate_slug()
        super(StockDataset, self).save(*args, **kwargs)

    def create(self):
        from api.tasks import stock_sense_crawl
        self.create_folder_in_scripts_data()
        self.crawl_for_historic_data()
        self.add_to_job()
        stock_sense_crawl.delay(self.slug)

    def stock_sense_crawl(self):
        self.generate_meta_data()
        self.save()

    def crawl_news_data(self):
        from api.StockAdvisor.crawling.news_parser import NewJsonParse
        extracted_data = []
        stock_symbols = json.loads(self.stock_symbols)
        for key in stock_symbols:
            company_name = stock_symbols[key]
            self.job.messages = update_stock_sense_message(self.job, company_name)
            self.job.save()
            stock_data = fetch_news_sentiments_from_newsapi(company_name, self.domains)
            try:
                obj = NewJsonParse(stock_data)
                stock_data = obj.remove_attributes()
            except:
                print("Issue while removing unwanted IBM watson attributes")

            self.write_to_concepts_folder(
                stockDataType="news",
                stockName=key,
                data=stock_data,
                type='json'
            )
            extracted_data.extend(stock_data)

        if len(extracted_data) < 1:
            return {}
        print("Total News Article are {0}".format(len(extracted_data)))
        meta_data = convert_crawled_data_to_metadata_format(
            news_data=extracted_data,
            other_details={
                'type': 'news_data'
            },
            slug=self.slug,
            symbols=self.get_stock_company_names(),
            created_at=self.created_at,
            start_date=self.start_date
        )

        meta_data['extracted_data'] = extracted_data

        return json.dumps(meta_data)

    def read_stock_json_file(self):

        with open('/home/ubuntu/stock_info.json') as stock_file:
            all_data = []
            for l in stock_file:
                all_data.append(json.loads(l))
            return all_data

    def crawl_for_historic_data(self):
        PRINTPREFIX = "crawl_historic"
        from api.StockAdvisor.crawling.generic_crawler import Cache
        import pickle

        historic_cache = Cache("historic")

        for stock_symbol in self.get_stock_symbol_names():
            stock_data = None
            cache_key = "historic_{}".format(stock_symbol)
            print(PRINTPREFIX, cache_key)

            from api.StockAdvisor.crawling.process import fetch_historical_data_from_alphavintage
            try:
                stock_data = fetch_historical_data_from_alphavintage(stock_symbol)
            except:
                pass

            if not stock_data:
                print(PRINTPREFIX, "Using Nasdaq Site for historic stock data for {0}".format(stock_symbol))
                NASDAQ_REGEX_FILE = "nasdaq_stock.json"
                url = generate_url_for_historic_data(stock_symbol)

                for i in range(10):

                    stock_data = crawl_extract(
                        url=url,
                        regex_dict=get_regex(NASDAQ_REGEX_FILE),
                        slug=self.slug
                    )

                    if len(stock_data) == 0 and i == 0:
                        try:
                            cached_data = historic_cache.get(cache_key)
                            stock_data = pickle.loads(cached_data)
                            print(PRINTPREFIX, "CACHE HIT :: Picked historic data from cache {}".format(stock_symbol))
                        except:

                            pass

                    if len(stock_data) > 0:
                        break

            if stock_data is not None:
                if len(stock_data) > 0:
                    print(PRINTPREFIX, "caching for{}".format(stock_symbol))
                    historic_cache.put(cache_key, pickle.dumps(stock_data))

                self.write_to_concepts_folder(
                    stockDataType="historic",
                    stockName=stock_symbol,
                    data=stock_data,
                    type='json'
                )

    # def crawl_for_historic_data(self):
    #     stock_symbols = self.get_stock_symbol_names()
    #     for stock in stock_symbols:
    #         stock_data = None
    #         from api.StockAdvisor.crawling.process import fetch_historical_data_from_alphavintage
    #         try:
    #             stock_data = fetch_historical_data_from_alphavintage(stock)
    #         except:
    #             NASDAQ_REGEX_FILE = "nasdaq_stock.json"
    #
    #             print "Using Nasdaq Site for historic stock data for {0}".format(stock)
    #             url = generate_url_for_historic_data(stock)
    #             stock_data = crawl_extract(
    #                 url=url,
    #                 regex_dict=get_regex(NASDAQ_REGEX_FILE),
    #                 slug=self.slug
    #             )
    #         if stock_data is not None:
    #             self.write_to_concepts_folder(
    #                 stockDataType="historic",
    #                 stockName=stock,
    #                 data=stock_data,
    #                 type='json'
    #             )

    def get_bluemix_natural_language_understanding(self, name=None):
        from .StockAdvisor.bluemix.process_urls import ProcessUrls
        path = os.path.dirname(os.path.dirname(__file__)) + "/scripts/data/" + "stock_info.csv"
        pu = ProcessUrls(path)
        datas = pu.process()
        self.write_bluemix_data_into_concepts(
            name="bluemix",
            data=datas,
            type='json'
        )

    def copy_file_to_hdfs(self, localpath, extra_path=None):

        hadoop_path = self.get_hdfs_relative_path(extra_path)
        try:
            hadoop.hadoop_put(localpath, hadoop_path)
        except:
            raise Exception("Failed to copy file to HDFS.")

    def get_hdfs_relative_path(self, extra_path=None):

        if extra_path is not None:
            hadoop_path = "/stockdataset/" + self.slug + "/" + extra_path
        else:
            hadoop_path = "/stockdataset/" + self.slug
        if hadoop.hadoop_exists(hadoop_path):
            pass
        else:
            hadoop.hadoop_mkdir(hadoop_path)
        return hadoop_path

    def generate_meta_data(self):
        self.meta_data = self.crawl_news_data()
        self.job.messages = update_stock_sense_message(self.job, "ml-work")
        self.job.save()
        self.stock_sense_job_submission()

    def create_folder_in_scripts_data(self):
        path = os.path.dirname(os.path.dirname(__file__)) + "/scripts/data/" + self.slug
        if not os.path.exists(path):
            os.makedirs(path)

    def paste_essential_files_in_scripts_folder(self):

        import shutil
        file_names = [
            'concepts.json',
            # 'aapl.json',
            # 'aapl_historic.json',
            # 'googl.json',
            # 'googl_historic.json',
            # 'ibm.json',
            # 'ibm_historic.json',
            # 'msft.json',
            # 'msft_historic.json'
        ]
        path = os.path.dirname(os.path.dirname(__file__)) + "/scripts/data"
        path_slug = os.path.dirname(os.path.dirname(__file__)) + "/scripts/data/" + self.slug + "/"
        self.sanitize(path + "/concepts.json")
        for name in file_names:
            path1 = path + "/" + name
            path2 = path_slug + name
            shutil.copyfile(path1, path2)

        self.put_files_into_remote()

    def sanitize(self, path, remove_tags=[]):
        import re
        import sys
        content = open(path, 'r').read()
        for html_tag in remove_tags:
            tag_regex = '(?is)<' + html_tag + '[^>]*?>.*?</' + html_tag + '>'  # (?is) is important to add,as it ignores case and new lines in text
            content = re.sub(tag_regex, '', content)
        text = ''
        text = re.sub('<.*?>', ' ', content)
        if text:
            text = text.replace("\n", "").replace("&nbsp;", "").replace("\t", " ").replace("\\u", " ").replace("\r",
                                                                                                               " ").strip()
        text = text.encode('utf-8')

        f = open(path, 'w')
        f.write(text)
        f.close()

    def put_files_into_remote(self):

        path_slug = os.path.dirname(os.path.dirname(__file__)) + "/scripts/data/" + self.slug + "/"

        from os import listdir
        from os.path import isfile, join
        file_names = listdir(path_slug)
        print(file_names)
        # onlyfiles = [f for f in listdir(path_slug) if isfile(join(path_slug, f))]

        from api.lib.fab_helper import mkdir_remote, put_file, remote_uname
        remote_path = '/home/hadoop/stock' + "/" + self.slug
        remote_path = str(remote_path)
        mkdir_remote(dir_paths=remote_path)
        remote_uname()
        for name in file_names:
            dest_path = remote_path + "/" + name
            src_path = path_slug + name
            print(src_path, dest_path)
            put_file(src_path, dest_path)

    def create_folder_in_remote(self):
        from api.lib.fab_helper import mkdir_remote, put_file, remote_uname
        remote_path = '/home/hadoop/stock' + "/" + self.slug
        mkdir_remote(dir_paths=remote_path)

    def stats(self, file):
        self.input_file = file
        self.data = self.generate_stats()
        self.analysis_done = True
        self.status = 'SUCCESS'
        self.save()

    def crawl_stats(self):
        crawled_stats = {
            "stats_sample": {
                "a": "a",
                "b": "b"
            }
        }
        return json.dumps(crawled_stats)

    def generate_stats(self):
        return self.crawl_stats()

    def get_stock_symbol_names(self):
        stock_symbols = json.loads(self.stock_symbols)
        return [key.lower() for key in stock_symbols.keys()]

    def get_stock_company_names(self):
        # list_of_stock = self.stock_symbols.split(', ')
        # return [stock_name.lower() for stock_name in list_of_stock]
        stock_symbols = json.loads(self.stock_symbols)
        return [value for value in stock_symbols.values()]

    def get_brief_info(self):
        brief_info = dict()
        brief_info.update(
            {
                'created_by': self.created_by.username,
                'updated_at': self.updated_at,
                'name': self.name,
                'stock_symbols': self.stock_symbols.upper()
                # 'file_size': convert_to_humanize(self.input_file.size)
            })
        return convert_json_object_into_list_of_object(brief_info, 'stockdataset')

    def call_mlscripts(self):
        self.add_to_job()
        self.analysis_done = False
        self.status = 'INPROGRESS'
        self.save()

    def fake_call_mlscripts(self):
        # self.data = json.dumps(sample_stockdataset_data)
        self.data = json.dumps(sample_dummy_data_for_stock)
        # self.data = json.dumps(anothersample_stock_dummy_data)
        self.analysis_done = True
        self.status = 'SUCCESS'
        self.save()

    def generate_config(self, *args, **kwargs):
        inputFile = ""
        datasource_details = ""
        datasource_type = ""
        stockSymbolList = self.get_stock_symbol_names()

        if settings.USE_HTTPS:
            protocol = 'https'
        else:
            protocol = 'http'

        THIS_SERVER_DETAILS = settings.THIS_SERVER_DETAILS

        data_api = "{3}://{0}/api/stockdatasetfiles/{2}/".format(THIS_SERVER_DETAILS.get('host'),
                                                                 THIS_SERVER_DETAILS.get('port'),
                                                                 self.get_data_api(), protocol)

        hdfs_path = self.get_hdfs_relative_path()

        return {
            "config": {
                "FILE_SETTINGS": {
                    "inputfile": [inputFile],
                },
                "COLUMN_SETTINGS": {
                    "analysis_type": ["metaData"],
                },
                "DATE_SETTINGS": {

                },
                "DATA_SOURCE": {
                    "datasource_details": datasource_details,
                    "datasource_type": datasource_type
                },
                "STOCK_SETTINGS": {
                    "stockSymbolList": stockSymbolList,
                    "dataAPI": data_api,  # + "?" + 'stockDataType = "bluemix"' + '&' + 'stockName = "googl"'
                    "hdfs_path": hdfs_path
                }
            }
        }

    def get_data_api(self):
        return str(self.slug)

    def add_to_job(self, *args, **kwargs):
        job_type = 'stockAdvisor'
        job = Job()
        job.name = "-".join([job_type, self.slug])
        job.job_type = job_type
        job.object_id = str(self.slug)
        job.submitted_by = self.created_by

        from api.helper import create_message_log_and_message_for_stocksense
        job.message_log, job.messages = create_message_log_and_message_for_stocksense(self.stock_symbols)
        job.save()

        self.job = job
        if job is None:
            self.status = "FAILED"
        else:
            self.status = "INPROGRESS"
        self.save()

    def stock_sense_job_submission(self):
        job = self.job
        jobConfig = self.generate_config()
        job.config = json.dumps(jobConfig)
        job.save()

        queue_name = None
        try:
            data_size = 3000
            queue_name = get_queue_to_use(job_type='stockAdvisor', data_size=data_size)
        except Exception as e:
            print(e)

        if not queue_name:
            queue_name = "default"

        from api.redis_access import AccessFeedbackMessage
        ac = AccessFeedbackMessage()
        message_slug = get_message_slug(job)
        ac.delete_this_key(message_slug)

        # Submitting JobServer
        from .utils import submit_job
        try:
            job_return_data = submit_job(
                slug=job.slug,
                class_name='stockAdvisor',
                job_config=jobConfig,
                job_name=self.name,
                message_slug=message_slug,
                queue_name=queue_name,
                app_id=None
            )

            job.url = job_return_data.get('application_id')
            job.command_array = json.dumps(job_return_data.get('command_array'))

            readable_job_config = {
                'job_config': job_return_data.get('config')['job_config']['job_config'],
                'config': job_return_data.get('config')['job_config']['config']
            }
            job.config = json.dumps(readable_job_config)
            job.save()
        except Exception as exc:
            return None

        return job

    def write_to_concepts_folder(self, stockDataType, stockName, data, type='json'):
        print(stockDataType)
        if stockDataType == "historic":
            name = stockName + "_" + stockDataType
        else:
            name = stockName
        path1 = os.path.dirname(os.path.dirname(__file__)) + "/scripts/data/" + self.slug + "/"
        # file_path = path + stockName + "." + type
        semi_path = os.path.dirname(os.path.dirname(__file__)) + "/scripts/data/" + self.slug
        from os import path
        if path.exists(semi_path) is False:
            os.mkdir(semi_path)
            os.chmod(semi_path, 0o777)
        file_path = path1 + name + "." + type
        # file_path = path + stockName + "." + type
        print("Writing {1} for {0}".format(stockName, stockDataType))
        print(file_path)
        with open(file_path, "w") as file_to_write_on:
            if 'csv' == type:
                writer = csv.writer(file_to_write_on)
                writer.writerow(data)
            elif 'json' == type:
                json.dump(data, file_to_write_on)
        self.copy_file_to_hdfs(file_path, stockDataType)

        self.write_crawled_databases(stockDataType, stockName, data)

    def write_crawled_databases(self, stockDataType, stockName, data):

        if stockDataType == "historic":
            name = stockName + "_" + stockDataType
        else:
            name = stockName

        crawled_data = self.crawled_data
        crawled_data = json.loads(crawled_data)

        if stockName in crawled_data:
            stockName_crawled_data = crawled_data[stockName]
            if name in stockName_crawled_data:
                pass
            else:
                stockName_crawled_data[name] = data
        else:
            crawled_data[stockName] = {
                name: data
            }

        if 'concepts' in crawled_data:
            pass
        else:
            path = os.path.dirname(os.path.dirname(__file__)) + "/scripts/data"
            path = path + "/concepts.json"
            self.copy_file_to_hdfs(path, extra_path='concepts')
            with open(path) as fp:
                crawled_data['concepts'] = json.loads(fp.read())

        self.crawled_data = json.dumps(crawled_data)
        self.save()

    def write_bluemix_data_into_concepts(self, name, data, type='json'):

        for key in list(data.keys()):
            name = name + "_" + key
            path = os.path.dirname(os.path.dirname(__file__)) + "/scripts/data/" + self.slug + "/"
            file_path = path + name + "." + type
            print(file_path)
            out_file = open(file_path, "wb")
            json.dump(data[key], out_file)
            out_file.close()


class Audioset(models.Model):
    name = models.CharField(max_length=100, null=True)
    slug = models.SlugField(null=True, max_length=300)
    auto_update = models.BooleanField(default=False)
    auto_update_duration = models.IntegerField(default=99999)

    input_file = models.FileField(upload_to='audioset', null=True)
    datasource_type = models.CharField(max_length=100, null=True)
    datasource_details = models.TextField(default="{}")
    preview = models.TextField(default="{}")

    meta_data = models.TextField(default="{}")

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    created_by = models.ForeignKey(User, null=False)
    deleted = models.BooleanField(default=False)

    job = models.ForeignKey(Job, null=True)

    bookmarked = models.BooleanField(default=False)
    file_remote = models.CharField(max_length=100, null=True)
    analysis_done = models.BooleanField(default=False)
    status = models.CharField(max_length=100, null=True, default="Not Registered")
    live_status = models.CharField(max_length=300, default='0', choices=STATUS_CHOICES)
    viewed = models.BooleanField(default=False)

    class Meta(object):
        ordering = ['-created_at', '-updated_at']
        # permissions = settings.NEW_PERMISSIONS

    def __str__(self):
        return " : ".join(["{}".format(x) for x in [self.name, self.datasource_type, self.slug]])

    def generate_slug(self):
        if not self.slug:
            self.slug = slugify(str(self.name) + "-" + ''.join(
                random.choice(string.ascii_uppercase + string.digits) for _ in range(10)))

    def save(self, *args, **kwargs):
        self.generate_slug()
        super(Audioset, self).save(*args, **kwargs)

    def create(self):
        # self.meta_data = json.dumps(dummy_audio_data_3)
        self.meta_data = self.get_speech_data()
        self.analysis_done = True
        self.status = 'SUCCESS'
        self.save()

    def get_speech_data(self):
        from api.lib.speech_analysis import SpeechAnalyzer
        sa = SpeechAnalyzer(self.input_file.path)
        sa.convert_speech_to_text()
        sa.understand_text()
        # sa.nl_understanding = json.loads("""{"semantic_roles": [{"action": {"text": "calling", "verb": {"text": "call", "tense": "present"}, "normalized": "call"}, "sentence": "I am calling regarding my cellphone details regarding the AD and D. center and %HESITATION my bills that's not in proper order can you get back to me", "object": {"text": "regarding my cellphone details regarding the AD and D. center"}, "subject": {"text": "I"}}, {"action": {"text": "get", "verb": {"text": "get", "tense": "future"}, "normalized": "get"}, "sentence": "I am calling regarding my cellphone details regarding the AD and D. center and %HESITATION my bills that's not in proper order can you get back to me", "object": {"text": "to me"}, "subject": {"text": "you"}}], "emotion": {"document": {"emotion": {"anger": 0.128218, "joy": 0.023388, "sadness": 0.039954, "fear": 0.030219, "disgust": 0.022114}}}, "sentiment": {"document": {"score": -0.602607, "label": "negative"}}, "language": "en", "entities": [], "relations": [{"score": 0.941288, "type": "agentOf", "arguments": [{"text": "I", "entities": [{"text": "you", "type": "Person"}]}, {"text": "calling", "entities": [{"text": "calling", "type": "EventCommunication"}]}], "sentence": "I am calling regarding my cellphone details regarding the AD and D. center and %HESITATION my bills that's not in proper order can you get back to me"}], "keywords": [{"relevance": 0.986328, "text": "cellphone details", "emotion": {"anger": 0.128218, "joy": 0.023388, "sadness": 0.039954, "fear": 0.030219, "disgust": 0.022114}, "sentiment": {"score": -0.602607}}, {"relevance": 0.833305, "text": "proper order", "emotion": {"anger": 0.128218, "joy": 0.023388, "sadness": 0.039954, "fear": 0.030219, "disgust": 0.022114}, "sentiment": {"score": -0.602607}}, {"relevance": 0.670873, "text": "D. center", "emotion": {"anger": 0.128218, "joy": 0.023388, "sadness": 0.039954, "fear": 0.030219, "disgust": 0.022114}, "sentiment": {"score": -0.602607}}, {"relevance": 0.552041, "text": "HESITATION", "sentiment": {"score": -0.602607}}, {"relevance": 0.396277, "text": "bills", "emotion": {"anger": 0.128218, "joy": 0.023388, "sadness": 0.039954, "fear": 0.030219, "disgust": 0.022114}, "sentiment": {"score": -0.602607}}, {"relevance": 0.34857, "text": "AD", "emotion": {"anger": 0.128218, "joy": 0.023388, "sadness": 0.039954, "fear": 0.030219, "disgust": 0.022114}, "sentiment": {"score": -0.602607}}], "concepts": [], "usage": {"text_characters": 150, "features": 8, "text_units": 1}, "categories": [{"score": 0.301348, "label": "/finance/personal finance/lending/credit cards"}, {"score": 0.17561, "label": "/business and industrial"}, {"score": 0.165519, "label": "/technology and computing"}]}
        #     """)
        sa.generate_node_structure()
        return json.dumps(sa.nl_understanding_nodestructure)

    def get_brief_info(self):
        brief_info = dict()
        from api.helper import convert_to_humanize
        brief_info.update(
            {
                'created_by': self.created_by.username,
                'updated_at': self.updated_at,
                'audioset': self.name,
                'file_size': convert_to_humanize(self.input_file.size)
            })
        return convert_json_object_into_list_of_object(brief_info, 'audioset')


class SaveData(models.Model):
    slug = models.SlugField(null=False, blank=True, max_length=300)
    data = models.TextField(default="{}")
    object_slug = models.SlugField(null=False, blank=True, max_length=300, default="")

    def get_data(self):
        data = self.data
        json_data = json.loads(data)
        csv_data = json_data.get('data')
        return csv_data

    def set_data(self, data):
        json_data = {
            "data": data
        }
        self.data = json.dumps(json_data)
        self.save()
        return True

    def generate_slug(self):
        if not self.slug:
            self.slug = slugify(''.join(
                random.choice(string.ascii_uppercase + string.digits) for _ in range(16)))

    def save(self, *args, **kwargs):
        self.generate_slug()
        super(SaveData, self).save(*args, **kwargs)

    def get_url(self):
        return "/api/download_data/" + self.slug


class SaveAnyData(models.Model):
    slug = models.SlugField(null=False, blank=True, max_length=255, unique=True)
    data = models.TextField(default="{}")

    def get_url(self):
        return "/api/download_data/" + self.slug

    def get_data(self):
        data = self.data
        json_data = json.loads(data)
        rdata = json_data.get('data')
        return rdata

    def set_slug(self, slug):
        self.slug = slug

    def set_data(self, data):
        json_data = {
            "data": data
        }
        self.data = json.dumps(json_data)
        self.save()
        return True


bar_chart = {
    "dataType": "c3Chart",
    "data": {
        "chart_c3": {
            "bar": {
                "width": 40
            },
            "point": None,
            "color": {
                "pattern": [
                    "#0fc4b5",
                    "#005662",
                    "#148071",
                    "#6cba86",
                    "#bcf3a2"
                ]
            },
            "tooltip": {
                "show": True,
                "format": {
                    "title": ".2s"
                }
            },
            "padding": {
                "top": 40
            },
            "grid": {
                "y": {
                    "show": True
                },
                "x": {
                    "show": True
                }
            },
            "subchart": None,
            "axis": {
                "y": {
                    "tick": {
                        "count": 7,
                        "outer": False,
                        "multiline": True,
                        "format": ".2s"
                    },
                    "label": {
                        "text": "score",
                        "position": "outer-middle"
                    }
                },
                "x": {
                    "height": 90,
                    "tick": {
                        "rotate": -45,
                        "multiline": False,
                        "fit": False,
                        "format": ".2s"
                    },
                    "type": "category",
                    "extent": None,
                    "label": {
                        "text": "keyword",
                        "position": "outer-center"
                    }
                }
            },
            "data": {
                "x": "text",
                "axes": {
                    "score": "y"
                },
                "type": "bar",
                "columns": [
                    [
                        "text",
                        "bank account number",
                        "credit card",
                        "New York",
                        "America",
                        "money",
                        "John",
                        "numbers"
                    ],
                    [
                        "score",
                        0.940398,
                        0.742339,
                        0.737608,
                        0.366456,
                        0.365641,
                        0.361568,
                        0.361102
                    ]
                ]
            },
            "legend": {
                "show": False
            },
            "size": {
                "height": 340
            }
        },
        "yformat": ".2f",
        "table_c3": [
            [
                "text",
                "bank account number",
                "credit card",
                "New York",
                "America",
                "money",
                "John",
                "numbers"
            ],
            [
                "score",
                0.940398,
                0.742339,
                0.737608,
                0.366456,
                0.365641,
                0.361568,
                0.361102
            ]
        ],
        "download_url": "/api/download_data/bkz2oyjih4iczk95",
        "xdata": [
            "bank account number",
            "credit card",
            "New York",
            "America",
            "money",
            "John",
            "numbers"
        ]
    }
}

horizontal_bar_chart = {
    "dataType": "c3Chart",
    "data": {
        "chart_c3": {
            "bar": {
                "width": {
                    "ratio": 0.5
                }
            },
            "point": None,
            "color": {
                "pattern": [
                    "#0fc4b5",
                    "#005662",
                    "#148071",
                    "#6cba86",
                    "#bcf3a2"
                ]
            },
            "tooltip": {
                "show": True,
                "format": {
                    "title": ".2s"
                }
            },
            "padding": {
                "top": 40
            },
            "grid": {
                "y": {
                    "show": True
                },
                "x": {
                    "show": True
                }
            },
            "subchart": None,
            "axis": {
                "y": {
                    "tick": {
                        "count": 7,
                        "outer": False,
                        "multiline": True,
                        "format": ".2s"
                    },
                    "label": {
                        "text": "score",
                        "position": "outer-middle"
                    }
                },
                "x": {
                    "height": 90,
                    "tick": {
                        "rotate": -45,
                        "multiline": False,
                        "fit": False,
                        "format": ".2s"
                    },
                    "type": "category",
                    "extent": None,
                    "label": {
                        "text": "keyword",
                        "position": "outer-center"
                    },
                    "rotated": True
                }
            },
            "data": {
                "x": "Source",
                "axes": {
                    "No. of Articles": "y"
                },
                "type": "bar",
                "columns": [
                    [
                        "text",
                        "bank account number",
                        "credit card",
                        "New York",
                        "America",
                        "money",
                        "John",
                        "numbers"
                    ],
                    [
                        "score",
                        0.940398,
                        0.742339,
                        0.737608,
                        0.366456,
                        0.365641,
                        0.361568,
                        0.361102
                    ]
                ]
            },
            "legend": {
                "show": False
            },
            "size": {
                "height": 340
            }
        },
        "yformat": ".2f",
        "table_c3": [
            [
                "text",
                "bank account number",
                "credit card",
                "New York",
                "America",
                "money",
                "John",
                "numbers"
            ],
            [
                "score",
                0.940398,
                0.742339,
                0.737608,
                0.366456,
                0.365641,
                0.361568,
                0.361102
            ]
        ],
        "download_url": "/api/download_data/bkz2oyjih4iczk95",
        "xdata": [
            "bank account number",
            "credit card",
            "New York",
            "America",
            "money",
            "John",
            "numbers"
        ]
    }
}

line_chart = {
    "dataType": "c3Chart",
    "data": {
        "chart_c3": {
            "point": None,
            "color": {
                "pattern": [
                    "#0fc4b5",
                    "#005662",
                    "#148071",
                    "#6cba86",
                    "#bcf3a2"
                ]
            },
            "padding": {
                "top": 40
            },
            "grid": {
                "y": {
                    "show": True
                },
                "x": {
                    "show": True
                }
            },
            "subchart": {
                "show": True
            },
            "data": {
                "x": "date",
                "axes": {
                    "scaled_total": "y"
                },
                "type": "line",
                "columns": [
                    [
                        "date",
                        "2016-06-01",
                        "2016-06-02",
                        "2016-06-03",
                        "2016-06-06",
                        "2016-06-07",
                        "2016-06-08",
                        "2016-06-09",
                        "2016-06-13",
                        "2016-06-14",
                        "2016-06-15",
                        "2016-06-16",
                        "2016-06-17",
                        "2016-06-20",
                        "2016-06-21",
                        "2016-06-22",
                        "2016-06-23",
                        "2016-06-24",
                        "2016-06-27",
                        "2016-06-28",
                        "2016-06-29",
                        "2016-06-30",
                        "2016-07-01",
                        "2016-07-04",
                        "2016-07-05",
                        "2016-07-07",
                        "2016-07-08",
                        "2016-07-11",
                        "2016-07-12",
                        "2016-07-13",
                        "2016-07-14",
                        "2016-07-15",
                        "2016-07-18",
                        "2016-07-19",
                        "2016-07-20",
                        "2016-07-21",
                        "2016-07-22",
                        "2016-07-25",
                        "2016-07-26",
                        "2016-07-27",
                        "2016-07-28",
                        "2016-07-29",
                        "2016-08-01",
                        "2016-08-03",
                        "2016-08-04",
                        "2016-08-05",
                        "2016-08-08",
                        "2016-08-09",
                        "2016-08-10",
                        "2016-08-11",
                        "2016-08-12",
                        "2016-08-16",
                        "2016-08-17",
                        "2016-08-18",
                        "2016-08-19",
                        "2016-08-22",
                        "2016-08-23",
                        "2016-08-24",
                        "2016-08-25",
                        "2016-08-30",
                        "2016-08-31",
                        "2016-09-01",
                        "2016-09-02",
                        "2016-09-06",
                        "2016-09-07",
                        "2016-09-08",
                        "2016-09-09",
                        "2016-09-12",
                        "2016-09-16",
                        "2016-09-19",
                        "2016-09-20",
                        "2016-09-21",
                        "2016-09-22",
                        "2016-09-23",
                        "2016-09-26",
                        "2016-09-27",
                        "2016-09-28",
                        "2016-09-30",
                        "2016-10-03",
                        "2016-10-04",
                        "2016-10-05",
                        "2016-10-06",
                        "2016-10-07",
                        "2016-10-10",
                        "2016-10-13",
                        "2016-10-14",
                        "2016-10-19",
                        "2016-10-20",
                        "2016-10-21",
                        "2016-10-24",
                        "2016-10-25",
                        "2016-10-26",
                        "2016-10-27",
                        "2016-10-28",
                        "2016-11-01",
                        "2016-11-02",
                        "2016-11-03",
                        "2016-11-04",
                        "2016-11-07",
                        "2016-11-08",
                        "2016-11-09",
                        "2016-11-10",
                        "2016-11-11",
                        "2016-11-17",
                        "2016-11-18",
                        "2016-11-23",
                        "2016-11-24",
                        "2016-11-25",
                        "2016-11-28",
                        "2016-11-29"
                    ],
                    [
                        "scaled_total",
                        100,
                        100.75,
                        101.63,
                        102.14,
                        102.6,
                        102.22,
                        102.34,
                        102.08,
                        103.8,
                        104.44,
                        104.44,
                        104.89,
                        104.52,
                        104.23,
                        104.39,
                        104.86,
                        104.16,
                        104.49,
                        105.5,
                        105.08,
                        105.26,
                        105.9,
                        105.37,
                        105.22,
                        105.14,
                        104.16,
                        104.23,
                        105.49,
                        105.85,
                        105.54,
                        104.48,
                        104.77,
                        105.79,
                        105.48,
                        105.27,
                        105.68,
                        105.51,
                        105.2,
                        105.24,
                        105.49,
                        104.72,
                        104.53,
                        104.94,
                        106.47,
                        106.84,
                        106.76,
                        107.14,
                        108.67,
                        108.48,
                        108.9,
                        108.04,
                        106.51,
                        106.59,
                        106.74,
                        107.4,
                        107.53,
                        107.17,
                        107.13,
                        108.05,
                        107.69,
                        106.39,
                        106.14,
                        106.36,
                        104.77,
                        104.89,
                        106.21,
                        106.52,
                        106.13,
                        105.73,
                        105.58,
                        105.63,
                        104.15,
                        104.24,
                        103.77,
                        105.57,
                        105.34,
                        105.83,
                        105.65,
                        105.99,
                        105.69,
                        104.81,
                        105.1,
                        105.19,
                        104.98,
                        103.78,
                        103.45,
                        102.91,
                        103.54,
                        103.99,
                        102.81,
                        103.72,
                        101.29,
                        99.53,
                        99.52,
                        99.27,
                        99.03,
                        97.68,
                        98.34,
                        98.63,
                        97.94,
                        99.49,
                        99.6,
                        99.76,
                        100.64,
                        100.35,
                        99.22,
                        99.65,
                        99.81,
                        99.25
                    ],
                    [
                        "sensex",
                        100,
                        100.81,
                        101.79,
                        102.34,
                        102.84,
                        102.42,
                        102.55,
                        102.27,
                        104.16,
                        104.84,
                        104.87,
                        105.34,
                        104.95,
                        104.61,
                        104.76,
                        105.25,
                        104.47,
                        104.82,
                        105.92,
                        105.47,
                        105.65,
                        106.35,
                        105.76,
                        105.57,
                        105.49,
                        104.42,
                        104.49,
                        105.86,
                        106.25,
                        105.88,
                        104.71,
                        105.03,
                        106.14,
                        105.81,
                        105.58,
                        106.03,
                        105.85,
                        105.51,
                        105.53,
                        105.79,
                        104.94,
                        104.74,
                        105.2,
                        106.86,
                        107.27,
                        107.16,
                        107.57,
                        109.25,
                        109.05,
                        109.5,
                        108.57,
                        106.9,
                        106.97,
                        107.12,
                        107.82,
                        107.95,
                        107.53,
                        107.48,
                        108.48,
                        108.08,
                        106.67,
                        106.41,
                        106.67,
                        104.91,
                        105.06,
                        106.48,
                        106.82,
                        106.4,
                        105.96,
                        105.79,
                        105.87,
                        104.22,
                        104.33,
                        103.79,
                        105.75,
                        105.5,
                        106.05,
                        105.85,
                        106.24,
                        105.91,
                        104.95,
                        105.25,
                        105.34,
                        105.1,
                        103.78,
                        103.41,
                        102.83,
                        103.52,
                        104.02,
                        102.74,
                        103.74,
                        101.11,
                        99.17,
                        99.15,
                        98.88,
                        98.59,
                        97.14,
                        97.87,
                        98.22,
                        97.5,
                        99.21,
                        99.34,
                        99.51,
                        100.48,
                        100.13,
                        98.89,
                        99.34,
                        99.5,
                        98.92
                    ]
                ]
            },
            "legend": {
                "show": True
            },
            "size": {
                "height": 490
            },
            "bar": {
                "width": {
                    "ratio": 0.5
                }
            },
            "tooltip": {
                "format": {
                    "title": ".2s"
                },
                "show": True
            },
            "axis": {
                "y": {
                    "tick": {
                        "count": 7,
                        "multiline": True,
                        "outer": False,
                        "format": ".2s"
                    },
                    "label": {
                        "text": "",
                        "position": "outer-middle"
                    }
                },
                "x": {
                    "tick": {
                        "rotate": -45,
                        "multiline": False,
                        "fit": False,
                        "format": ".2s"
                    },
                    "type": "category",
                    "label": {
                        "text": "",
                        "position": "outer-center"
                    },
                    "extent": [
                        0,
                        10
                    ],
                    "height": 90
                }
            }
        },
        "yformat": ".2s",
        "table_c3": [
            [
                "date",
                "2016-06-01",
                "2016-06-02",
                "2016-06-03",
                "2016-06-06",
                "2016-06-07",
                "2016-06-08",
                "2016-06-09",
                "2016-06-13",
                "2016-06-14",
                "2016-06-15",
                "2016-06-16",
                "2016-06-17",
                "2016-06-20",
                "2016-06-21",
                "2016-06-22",
                "2016-06-23",
                "2016-06-24",
                "2016-06-27",
                "2016-06-28",
                "2016-06-29",
                "2016-06-30",
                "2016-07-01",
                "2016-07-04",
                "2016-07-05",
                "2016-07-07",
                "2016-07-08",
                "2016-07-11",
                "2016-07-12",
                "2016-07-13",
                "2016-07-14",
                "2016-07-15",
                "2016-07-18",
                "2016-07-19",
                "2016-07-20",
                "2016-07-21",
                "2016-07-22",
                "2016-07-25",
                "2016-07-26",
                "2016-07-27",
                "2016-07-28",
                "2016-07-29",
                "2016-08-01",
                "2016-08-03",
                "2016-08-04",
                "2016-08-05",
                "2016-08-08",
                "2016-08-09",
                "2016-08-10",
                "2016-08-11",
                "2016-08-12",
                "2016-08-16",
                "2016-08-17",
                "2016-08-18",
                "2016-08-19",
                "2016-08-22",
                "2016-08-23",
                "2016-08-24",
                "2016-08-25",
                "2016-08-30",
                "2016-08-31",
                "2016-09-01",
                "2016-09-02",
                "2016-09-06",
                "2016-09-07",
                "2016-09-08",
                "2016-09-09",
                "2016-09-12",
                "2016-09-16",
                "2016-09-19",
                "2016-09-20",
                "2016-09-21",
                "2016-09-22",
                "2016-09-23",
                "2016-09-26",
                "2016-09-27",
                "2016-09-28",
                "2016-09-30",
                "2016-10-03",
                "2016-10-04",
                "2016-10-05",
                "2016-10-06",
                "2016-10-07",
                "2016-10-10",
                "2016-10-13",
                "2016-10-14",
                "2016-10-19",
                "2016-10-20",
                "2016-10-21",
                "2016-10-24",
                "2016-10-25",
                "2016-10-26",
                "2016-10-27",
                "2016-10-28",
                "2016-11-01",
                "2016-11-02",
                "2016-11-03",
                "2016-11-04",
                "2016-11-07",
                "2016-11-08",
                "2016-11-09",
                "2016-11-10",
                "2016-11-11",
                "2016-11-17",
                "2016-11-18",
                "2016-11-23",
                "2016-11-24",
                "2016-11-25",
                "2016-11-28",
                "2016-11-29"
            ],
            [
                "scaled_total",
                100,
                100.75,
                101.63,
                102.14,
                102.6,
                102.22,
                102.34,
                102.08,
                103.8,
                104.44,
                104.44,
                104.89,
                104.52,
                104.23,
                104.39,
                104.86,
                104.16,
                104.49,
                105.5,
                105.08,
                105.26,
                105.9,
                105.37,
                105.22,
                105.14,
                104.16,
                104.23,
                105.49,
                105.85,
                105.54,
                104.48,
                104.77,
                105.79,
                105.48,
                105.27,
                105.68,
                105.51,
                105.2,
                105.24,
                105.49,
                104.72,
                104.53,
                104.94,
                106.47,
                106.84,
                106.76,
                107.14,
                108.67,
                108.48,
                108.9,
                108.04,
                106.51,
                106.59,
                106.74,
                107.4,
                107.53,
                107.17,
                107.13,
                108.05,
                107.69,
                106.39,
                106.14,
                106.36,
                104.77,
                104.89,
                106.21,
                106.52,
                106.13,
                105.73,
                105.58,
                105.63,
                104.15,
                104.24,
                103.77,
                105.57,
                105.34,
                105.83,
                105.65,
                105.99,
                105.69,
                104.81,
                105.1,
                105.19,
                104.98,
                103.78,
                103.45,
                102.91,
                103.54,
                103.99,
                102.81,
                103.72,
                101.29,
                99.53,
                99.52,
                99.27,
                99.03,
                97.68,
                98.34,
                98.63,
                97.94,
                99.49,
                99.6,
                99.76,
                100.64,
                100.35,
                99.22,
                99.65,
                99.81,
                99.25
            ],
            [
                "sensex",
                100,
                100.81,
                101.79,
                102.34,
                102.84,
                102.42,
                102.55,
                102.27,
                104.16,
                104.84,
                104.87,
                105.34,
                104.95,
                104.61,
                104.76,
                105.25,
                104.47,
                104.82,
                105.92,
                105.47,
                105.65,
                106.35,
                105.76,
                105.57,
                105.49,
                104.42,
                104.49,
                105.86,
                106.25,
                105.88,
                104.71,
                105.03,
                106.14,
                105.81,
                105.58,
                106.03,
                105.85,
                105.51,
                105.53,
                105.79,
                104.94,
                104.74,
                105.2,
                106.86,
                107.27,
                107.16,
                107.57,
                109.25,
                109.05,
                109.5,
                108.57,
                106.9,
                106.97,
                107.12,
                107.82,
                107.95,
                107.53,
                107.48,
                108.48,
                108.08,
                106.67,
                106.41,
                106.67,
                104.91,
                105.06,
                106.48,
                106.82,
                106.4,
                105.96,
                105.79,
                105.87,
                104.22,
                104.33,
                103.79,
                105.75,
                105.5,
                106.05,
                105.85,
                106.24,
                105.91,
                104.95,
                105.25,
                105.34,
                105.1,
                103.78,
                103.41,
                102.83,
                103.52,
                104.02,
                102.74,
                103.74,
                101.11,
                99.17,
                99.15,
                98.88,
                98.59,
                97.14,
                97.87,
                98.22,
                97.5,
                99.21,
                99.34,
                99.51,
                100.48,
                100.13,
                98.89,
                99.34,
                99.5,
                98.92
            ]
        ],
        "xdata": [
            "2016-06-01",
            "2016-06-02",
            "2016-06-03",
            "2016-06-06",
            "2016-06-07",
            "2016-06-08",
            "2016-06-09",
            "2016-06-13",
            "2016-06-14",
            "2016-06-15",
            "2016-06-16",
            "2016-06-17",
            "2016-06-20",
            "2016-06-21",
            "2016-06-22",
            "2016-06-23",
            "2016-06-24",
            "2016-06-27",
            "2016-06-28",
            "2016-06-29",
            "2016-06-30",
            "2016-07-01",
            "2016-07-04",
            "2016-07-05",
            "2016-07-07",
            "2016-07-08",
            "2016-07-11",
            "2016-07-12",
            "2016-07-13",
            "2016-07-14",
            "2016-07-15",
            "2016-07-18",
            "2016-07-19",
            "2016-07-20",
            "2016-07-21",
            "2016-07-22",
            "2016-07-25",
            "2016-07-26",
            "2016-07-27",
            "2016-07-28",
            "2016-07-29",
            "2016-08-01",
            "2016-08-03",
            "2016-08-04",
            "2016-08-05",
            "2016-08-08",
            "2016-08-09",
            "2016-08-10",
            "2016-08-11",
            "2016-08-12",
            "2016-08-16",
            "2016-08-17",
            "2016-08-18",
            "2016-08-19",
            "2016-08-22",
            "2016-08-23",
            "2016-08-24",
            "2016-08-25",
            "2016-08-30",
            "2016-08-31",
            "2016-09-01",
            "2016-09-02",
            "2016-09-06",
            "2016-09-07",
            "2016-09-08",
            "2016-09-09",
            "2016-09-12",
            "2016-09-16",
            "2016-09-19",
            "2016-09-20",
            "2016-09-21",
            "2016-09-22",
            "2016-09-23",
            "2016-09-26",
            "2016-09-27",
            "2016-09-28",
            "2016-09-30",
            "2016-10-03",
            "2016-10-04",
            "2016-10-05",
            "2016-10-06",
            "2016-10-07",
            "2016-10-10",
            "2016-10-13",
            "2016-10-14",
            "2016-10-19",
            "2016-10-20",
            "2016-10-21",
            "2016-10-24",
            "2016-10-25",
            "2016-10-26",
            "2016-10-27",
            "2016-10-28",
            "2016-11-01",
            "2016-11-02",
            "2016-11-03",
            "2016-11-04",
            "2016-11-07",
            "2016-11-08",
            "2016-11-09",
            "2016-11-10",
            "2016-11-11",
            "2016-11-17",
            "2016-11-18",
            "2016-11-23",
            "2016-11-24",
            "2016-11-25",
            "2016-11-28",
            "2016-11-29"
        ]
    }
}

combo_chart = {
    "bar": {
        "width": {
            "ratio": 0.5
        }
    },
    "point": None,
    "color": {
        "pattern": [
            "#005662",
            "#0fc4b5",
            "#148071",
            "#6cba86",
            "#bcf3a2"
        ]
    },
    "tooltip": {
        "show": True,
        "format": {
            "title": ".2s"
        }
    },
    "padding": {
        "top": 40
    },
    "grid": {
        "y": {
            "show": True
        },
        "x": {
            "show": True
        }
    },
    "subchart": None,
    "axis": {
        "y": {
            "tick": {
                "count": 7,
                "outer": False,
                "multiline": True,
                "format": ".2s"
            },
            "label": {
                "text": "",
                "position": "outer-middle"
            }
        },
        "x": {
            "height": 90,
            "tick": {
                "rotate": -45,
                "multiline": False,
                "fit": False,
                "format": ".2s"
            },
            "type": "category",
            "label": {
                "text": "",
                "position": "outer-center"
            }
        },
        "y2": {
            "show": True,
            "tick": {
                "count": 7,
                "multiline": True,
                "format": ".2s"
            },
            "label": {
                "text": "",
                "position": "outer-middle"
            }
        }
    },
    "data": {
        "axes": {
            "percentage": "y2"
        },
        "columns": [
            [
                "percentage",
                17.51824817518248,
                8.860759493670885,
                20.297029702970296,
                42.30769230769231,
                0
            ],
            [
                "total",
                72,
                7,
                41,
                11,
                0
            ],
            [
                "key",
                "0 to 3.4",
                "3.4 to 6.8",
                "6.8 to 10.2",
                "10.2 to 13.6",
                "13.6 to 17"
            ]
        ],
        "x": "key",
        "type": "combination",
        "types": {
            "percentage": "line",
            "total": "bar"
        },
        "names": {
            "percentage": "% of Travel_Frequently",
            "total": "# of Travel_Frequently"
        }
    },
    "legend": {
        "show": True
    },
    "size": {
        "height": 340
    }
}

pie_chart = {
    "dataType": "c3Chart",
    "data": {
        "chart_c3": {
            "color": {
                "pattern": [
                    "#0fc4b5",
                    "#005662",
                    "#148071",
                    "#6cba86",
                    "#bcf3a2"
                ]
            },
            "pie": {
                "label": {
                    "format": None
                }
            },
            "padding": {
                "top": 40
            },
            "data": {
                "x": None,
                "type": "pie",
                "columns": [
                    [
                        "Cash",
                        7
                    ],
                    [
                        "Debt",
                        28
                    ],
                    [
                        "Equity",
                        65
                    ]
                ]
            },
            "legend": {
                "show": True
            },
            "size": {
                "height": 340
            }
        },
        "table_c3": [
            [
                "Cash",
                7
            ],
            [
                "Debt",
                28
            ],
            [
                "Equity",
                65
            ]
        ]
    }
}

databox_chart = {
    "dataType": "dataBox",
    "data": [{
        "name": "News Sources",
        "value": "11"
    }, {
        "name": "Articles Crawled",
        "value": "1245"
    }, {
        "name": "Avg. Stock Price Change",
        "value": "15.7 %"
    }, {
        "name": "Market Cap Change",
        "value": "$1.23m"
    }, {
        "name": "Max Change in Stock",
        "value": "AMZN +11.4%"
    }, {
        "name": "Average Sentiment Score",
        "value": "0.89"
    }, {
        "name": "Max Change in Sentiment",
        "value": "GOOGL +0.24"
    }]
}

word_cloud = {
    "dataType": "wordCloud",
    "data": [{
        "text": "facilities",
        "value": 2
    }, {
        "text": "facilities",
        "value": 2
    }, {
        "text": "facilities",
        "value": 2
    }, {
        "text": "facilities",
        "value": 2
    }, {
        "text": "facilities",
        "value": 2
    }, {
        "text": "facilities",
        "value": 2
    }, {
        "text": "facilities",
        "value": 2
    }]
}

heat_map = {
    "dataType": "table",
    "data": {
        "topHeader": "Average Elapsed Day",
        "tableData": [
            ["Category", "Batteries & Accessories", "Car Electronics", "Exterior Accessories", "Garage & Car Care",
             "Interior Accessories", "Motorcycle Parts", "Performance Parts", "Replacement Parts", "Shelters & RV",
             "Tires & Wheels", "Towing & Hitches"],
            ["0.0 to 5.0", "73.87", "56.69", "70.8", "60.28", "73.62", "71.49", "73.96", "70.39", "71.71", "79.29",
             "76.68"],
            ["5.0 to 10.0", "69.08", "44.8", "60.21", "61.73", "63.54", "60.64", "58.52", "61.38", "60.7", "76.0",
             "63.56"],
            ["20.0 to 25.0", "41.0", "0.0", "57.0", "78.0", "35.5", "56.57", "54.5", "55.8", "23.0", "18.0", "39.67"],
            ["15.0 to 20.0", "0.0", "0.0", "20.33", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0"],
            ["10.0 to 15.0", "0.0", "0.0", "0.0", "0.0", "0.0", "0.0", "47.0", "0.0", "0.0", "0.0", "0.0"]
        ],
        "tableType": "heatMap"
    }
}

table2 = {
    "dataType": "table",
    "data": {
        "tableType": "decisionTreeTable",
        "tableData": [
            ["PREDICTION", "RULES", "PERCENTAGE"],
            ["High", ["Closing Days <= 37.0,Opportunity Result in (Loss),Closing Days <= 32.0",
                      "Closing Days <= 37.0,Opportunity Result in (Loss),Closing Days > 32.0",
                      "Closing Days <= 37.0,Opportunity Result not in (Loss),Market Route not in (Telesales,Reseller)"],
             [93.09, 69.98, 65.67]
             ],
            ["Medium", ["Closing Days > 37.0,Closing Days <= 59.0,Closing Days <= 45.0",
                        "Closing Days > 37.0,Closing Days <= 59.0,Closing Days > 45.0",
                        "Closing Days > 37.0,Closing Days > 59.0,Sales Stage Change Count <= 4.0"],
             [59.03, 86.34, 56.82]
             ],
            ["Low", ["Closing Days <= 37.0,Opportunity Result not in (Loss),Market Route in (Telesales,Reseller)",
                     "Closing Days > 37.0,Closing Days > 59.0,Sales Stage Change Count > 4.0"],
             [73.77, 65.56]
             ]
        ]
    }
}


def change_html_data(content=''):
    return {
        "dataType": "html",
        "data": content
    }


individual_company = {
    "listOfNodes": [
    ],
    "listOfCards": [
        {
            "cardType": "normal",
            "name": "node2-card1",
            "slug": "node2-card1",
            "cardData": [
                'databox',  # databox_chart
                'articles_and_sentiments_by_source',  # horizontal_bar_chart,
                'articles_and_sentiments_by_concepts',  # horizontal_bar_chart,
                'stock_performance_vs_sentiment_score',  # line_chart,
                # 'statistical_significance_of_keywords', # bar_chart,
                # 'top_entities', # word_cloud
                'stock_word_cloud_title',
                'stock_word_cloud'
            ]
        },
        {
            "cardType": "normal",
            "name": "node2-card2",
            "slug": "node2-card2",
            "cardData": [
                'decisionTreeTable_title',
                'decisionTreeTable',  # decisionTreeTable
                'key_events_title',
                'key_events',
            ]
        }, {
            "cardType": "normal",
            "name": "node2-card3",
            "slug": "node2-card3",
            "cardData": [
                'sentiments_by_concepts_title',
                'sentiments_by_concepts',  # decisionTreeTable
                'factors_that_impact_stock_price',
            ]
        },
        # {
        #     "cardType": "normal",
        #     "name": "node2-card2",
        #     "slug": "node2-card2",
        #     "cardData": [
        #         # 'html_random'# 'top_positive_and_negative_statement', # table2,
        #         # 'articles_with_highest_and_lowest_sentiments_score', #table2
        #     ]
        # },
        # {
        #     "cardType": "normal",
        #     "name": "node2-card3",
        #     "slug": "node2-card3",
        #     "cardData": [
        #         # 'html_random' # "segment_by_concept_and_keyword", # heat_map,
        #         # 'key_parameter_that_impact_stock_prices', # bar_chart
        #     ]
        # }
    ],
    "name": "",
    "slug": ""
}

import copy


def make_combochart(data, chart, x=None, axes=None, widthPercent=None, title=None):
    t_chart = set_axis_and_data(axes, chart, data, x)
    set_label_and_title(axes, t_chart, title, widthPercent, x)
    if len(list(axes.keys())) > 1:
        t_chart["data"]["chart_c3"]["data"]["types"] = {list(axes.keys())[1]: "line"}

    make_y2axis(axes, t_chart)
    return t_chart


def make_y2axis(axes, t_chart):
    if len(list(axes.keys())) > 1:
        t_chart["data"]["chart_c3"]["axis"]["y2"] = {
            "show": True,
            "tick": {
                "count": 7,
                "multiline": True,
                "format": ".2s"
            },
            "label": {
                "text": list(axes.keys())[1],
                "position": "outer-middle"
            }
        }
        t_chart["data"]["y2format"] = ".2s"


def set_axis_and_data(axes, chart, data, x):
    t_chart = copy.deepcopy(chart)
    t_chart["data"]["chart_c3"]["data"]["columns"] = data
    t_chart["data"]["chart_c3"]["data"]["x"] = x
    t_chart["data"]["chart_c3"]["data"]["axes"] = axes
    t_chart["data"]["xdata"] = data[0][1:]
    t_chart["data"]["table_c3"] = data
    return t_chart


def change_data_in_chart(data, chart, x=None, axes=None, widthPercent=None, title=None):
    t_chart = set_axis_and_data(axes, chart, data, x)
    set_label_and_title(axes, t_chart, title, widthPercent, x)

    make_y2axis(axes, t_chart)

    return t_chart


def change_data_in_chart_time_series(data, chart, x=None, axes=None, widthPercent=None, title=None):
    t_chart = change_data_in_chart(data, chart, x, axes, widthPercent, title)
    t_chart["axis"] = {"x": {
        'type': 'timeseries',
        'tick': {
            'format': '%d-%m-%Y'
        }
    }}
    return t_chart


def change_data_in_chart_no_zoom(data, chart, x=None, axes=None, widthPercent=None, title=None):
    t_chart = set_axis_and_data(axes, chart, data, x)
    set_label_and_title(axes, t_chart, title, widthPercent, x)

    make_y2axis(axes, t_chart)

    t_chart["data"]["chart_c3"]["subchart"] = None
    return t_chart


def set_label_and_title(axes, chart, title, widthPercent, x):
    if title:
        chart["data"]["chart_c3"]["title"] = {"text": title}
    if x:
        chart["data"]["chart_c3"]["axis"]["x"]["label"]["text"] = x
    if axes:
        chart["data"]["chart_c3"]["axis"]["y"]["label"]["text"] = list(axes.keys())[0]
    if widthPercent is not None:
        chart["widthPercent"] = widthPercent


def change_data_in_pie_chart(data, chart, widthPercent=None, title=None):
    import copy
    chart = copy.deepcopy(chart)
    chart["data"]["chart_c3"]["data"]["columns"] = data
    chart["data"]["table_c3"] = data

    if title:
        chart["data"]["chart_c3"]["title"] = {"text": title}

    if widthPercent is not None:
        chart["widthPercent"] = widthPercent

    return chart


def change_data_in_databox(data, databox):
    import copy
    databox = copy.deepcopy(databox)
    databox["data"] = data
    return databox


def change_data_in_wordcloud(data, wordcloud=None):
    if wordcloud:
        import copy
        t_wordcloud = copy.deepcopy(wordcloud)
    else:
        t_wordcloud = {
            "dataType": "wordCloud",
            "data": None
        }

    t_wordcloud['data'] = data
    return t_wordcloud


def change_data_inheatmap(data):
    return data


def change_data_in_table(data):
    return {
        "dataType": "table",
        "data": {
            "tableData": data,
            "tableType": "normal",
        }
    }


def change_data_in_decision_tree_table(data):
    return {"dataType": "table", "data": {"tableType": "decisionTreeTable", "tableData": data}}
    pass


def change_data_in_heatmap(data):
    return {
        "dataType": "table",
        "data": {
            "tableData": data,
            "tableType": "textHeatMapTable",
        }
    }

    pass


def change_name_and_slug_in_individual(name):
    card_name = ["Analysis Overview", "Event Analysis", "Impact Analysis"]
    # temp_node = copy.deepcopy(individual_company)
    import copy
    temp_node = copy.deepcopy(individual_company)
    temp_node['name'] = name
    temp_node['slug'] = name
    listOfCards = temp_node['listOfCards']
    new_list_of_cards = []
    final_list_of_cards = []
    for i, cards in enumerate(listOfCards):
        this_card = {}
        cards["name"] = card_name[i]
        cards["slug"] = card_name[i] + ''.join(
            random.choice(string.ascii_uppercase + string.digits) for _ in range(5))

        cardData = cards['cardData']
        temp_card_data = []

        details_data = stock_name_match_with_data[name]
        for cardD in cardData:
            chart = None
            if cardD == "databox":
                chart = change_data_in_databox(
                    data=details_data[cardD],
                    databox=databox_chart
                )
            if cardD == "articles_and_sentiments_by_source":
                chart = make_combochart(
                    data=details_data[cardD],
                    chart=horizontal_bar_chart,
                    x="Source",
                    axes={"No. of Articles": "y", "Average Sentiment Score": "y2"},
                    widthPercent=50,
                    title="Sentiment Score by Source"
                )
            if cardD == "articles_and_sentiments_by_concepts":
                chart = make_combochart(
                    data=details_data[cardD],
                    chart=horizontal_bar_chart,
                    x="Concept",
                    axes={"No. of Articles": "y", 'Average Sentiment Score': "y2"},
                    widthPercent=50,
                    title="Sentiment Score by Concept"

                )
            if cardD == 'stock_performance_vs_sentiment_score':
                chart = change_data_in_chart_time_series(
                    data=details_data[cardD],
                    chart=line_chart,
                    x="Date",
                    axes={'Stock Value': 'y', 'Sentiment Score': 'y2'},
                    widthPercent=100,
                    title="Stock Performance Vs Sentiment Score"
                )
            if cardD == 'statistical_significance_of_concepts':
                chart = change_data_in_chart(
                    data=details_data[cardD],
                    chart=bar_chart,
                    x="Score",
                    axes={"Avg. Sentiment Score": "y"},
                    widthPercent=100
                )
            if cardD == 'top_keywords':
                chart = change_data_in_wordcloud(
                    data=details_data[cardD],
                    wordcloud=word_cloud
                )
            # if cardD == "stock_performance_vs_sentiment_score":
            #     chart = change_data_inheatmap(details_data[cardD])
            if cardD == 'key_parameter_that_impact_stock_prices':
                chart = change_data_in_chart(
                    data=details_data[cardD],
                    chart=bar_chart,
                    x="Score",
                    axes={"Avg. Sentiment Score": "y"},
                    widthPercent=100
                )
            if cardD == "segment_by_concept_and_keyword":
                chart = change_data_inheatmap(details_data[cardD])
            if cardD in ['top_positive_and_negative_statement']:
                chart = change_data_in_table(details_data[cardD])

            if cardD == 'html_random':
                chart = change_html_data('<p><h2>{}</h2>{}</p>'.format("Test", "Test content"))
                return chart

            if cardD == "stock_word_cloud":
                chart = change_data_in_wordcloud(details_data[cardD])

            if cardD == "stock_word_cloud_title":
                chart = change_html_data("<h3>Top Entities</h3>")
            if cardD == "decisionTreeTable_title":
                chart = change_html_data("<h3>Key Days and Impactful Articles</h3>")
            if cardD == "key_events_title":
                chart = change_html_data("<h3>Top Articles</h3>")

            if cardD == 'decisionTreeTable':
                chart = change_data_in_table(details_data[cardD])

            if cardD == "key_events":
                chart = change_data_in_table(details_data[cardD])

            if cardD == "sentiments_by_concepts_title":
                chart = change_html_data("<h3>Sentiment by Concept</h3>")

            if cardD == 'sentiments_by_concepts':
                chart = change_data_in_heatmap(details_data[cardD])

            if cardD == 'factors_that_impact_stock_price':
                chart = change_data_in_chart(
                    data=details_data[cardD],
                    chart=bar_chart,
                    x="Key Factors",
                    axes={"Correlation Coefficient": "y"},
                    widthPercent=100,
                    title="Factors Influencing Stock Price"
                )

            if chart is not None:
                temp_card_data.append(chart)

        cards['cardData'] = temp_card_data
        new_list_of_cards.append(cards)

    temp_node['listOfCards'] = new_list_of_cards

    return temp_node


def smaller_name_and_slug_in_individual(name):
    # import copy
    # temp_node = copy.deepcopy(individual_company)
    temp_node = {}
    temp_node['name'] = name
    temp_node['slug'] = name

    card_1 = {
        "cardType": "normal",
        "name": "node2-caasdasd",
        "slug": "node2-card2asda",
        "display": False,
        "cardData": [
            change_html_data(
                '<br/><br/><div style="text-align:center"><h2>{}</h2></div><br/><br/>'.format(text_overview)),

            change_data_in_databox(
                data=overview_of_second_node_databox_data,
                databox=databox_chart
            )
        ]
    }

    return card_1


node1_databox_data = [{
    "name": "Total Articles",
    "value": "583"
}, {
    "name": "Total Sources",
    "value": "68"
}, {
    "name": "Average Sentiment Score",
    "value": "0.27"
}, {
    "name": "Overall Stock % Change",
    "value": "3.2 %"
}, {
    "name": "Max Increase in Price",
    "value": "13.4% (FB)"
}, {
    "name": "Max Decrease in Price",
    "value": "-2.0% (AMZN)"
}]

number_of_articles_by_stock = [
    ['Stock', "FB", "GOOGL", "IBM", "AMZN", "AAPL"],
    ['No. of Articles', 92, 94, 71, 128, 101]
]

article_by_source1 = [
    ['Source', '24/7 Wall St.', '9to5Mac', 'Amigobulls', 'Argus Journal', 'Benzinga', 'Bloomberg', 'Bloomberg BNA',
     'Business Wire (press release)', 'BZ Weekly', 'Crains Detroit Business', 'DirectorsTalk Interviews',
     'Dispatch Tribunal', 'Economic News', 'Engadget', 'Equities.com', 'Forbes', 'Fox News', 'GuruFocus.com',
     'GuruFocus.com (blog)', 'Inc.com', 'insideBIGDATA', 'Investopedia (blog)', 'Investorplace.com',
     'Investorplace.com (blog)', 'LearnBonds', 'Library For Smart Investors', 'Live Trading News', 'Los Angeles Times',
     'Madison.com', 'Market Exclusive', 'MarketWatch', 'Motley Fool', 'Nasdaq', 'NBC Southern California',
     'New York Law Journal (registration)', 'NY Stock News', 'Post Analyst', 'PR Newswire (press release)',
     'Proactive Investors UK', 'Reuters', 'Reuters Key Development', 'Reuters.com', 'San Antonio Business Journal',
     'Seeking Alpha', 'Silicon Valley Business Journal', 'Simply Wall St', 'Stock Press Daily', 'Stock Talker',
     'StockNews.com (blog)', 'StockNewsGazette', 'StockNewsJournal', 'Street Observer (press release)',
     'The Ledger Gazette', 'The Recorder', 'The Wall Street Transcript', 'TheStreet.com', 'Times of India',
     'TopChronicle', 'TRA', 'Triangle Business Journal', 'TrueBlueTribune', 'USA Commerce Daily', 'ValueWalk',
     'Voice Of Analysts', 'Wall Street Journal', 'Yahoo Finance', 'Yahoo News', 'Zacks.com'],
    ['No. of Articles', 1, 1, 6, 1, 5, 10, 1, 1, 1, 1, 2, 2, 9, 1, 12, 1, 1, 2, 1, 1, 1, 1, 53, 10, 1, 1, 3, 2, 2, 2, 4,
     43, 11, 1, 1, 8, 3, 2, 3, 9, 217, 1, 1, 63, 2, 1, 1, 1, 17, 2, 16, 2, 6, 1, 1, 5, 1, 1, 1, 1, 1, 1, 8, 1, 3, 3, 2,
     2]
]

article_by_source = [
    ['Source', 'Reuters Key Development', 'Seeking Alpha', 'Investorplace.com', 'Motley Fool', 'StockNews.com (blog)',
     'StockNewsJournal', 'Equities.com', 'Nasdaq', 'Bloomberg', 'Investorplace.com (blog)', 'Economic News', 'Reuters',
     'NY Stock News', 'ValueWalk', 'Amigobulls', 'The Ledger Gazette', 'Benzinga', 'TheStreet.com', 'MarketWatch',
     'Live Trading News', 'Post Analyst', 'Proactive Investors UK', 'Wall Street Journal', 'Yahoo Finance',
     'DirectorsTalk Interviews', 'Dispatch Tribunal', 'GuruFocus.com', 'Los Angeles Times', 'Madison.com',
     'Market Exclusive'][:7],
    ['No. of Articles', 217, 63, 53, 43, 17, 16, 12, 11, 10, 10, 9, 9, 8, 8, 6, 6, 5, 5, 4, 3, 3, 3, 3, 3, 2, 2, 2, 2,
     2, 2][:7]
]

from .sample_stock_data import stock_performace_card1, \
    stock_by_sentiment_score, \
    number_of_articles_by_concept, \
    overview_of_second_node_databox_data, \
    stock_name_match_with_data, \
    text_overview

node1 = {
    "listOfNodes": [
    ],
    "listOfCards": [
        {
            "cardType": "normal",
            "name": "node1-card1",
            "slug": "node1-card1",
            "cardData": [
                change_data_in_databox(node1_databox_data, databox_chart),
                change_data_in_chart(
                    data=number_of_articles_by_stock,
                    chart=horizontal_bar_chart,
                    x="Stock",
                    axes={"No. of Articles": "y"},
                    widthPercent=50,
                    title="Articles by Stock"
                ),

                change_data_in_pie_chart(
                    data=number_of_articles_by_concept,
                    chart=pie_chart,
                    widthPercent=50,
                    title="Articles by Concept"
                ),
                change_data_in_chart(
                    data=stock_performace_card1,
                    chart=line_chart,
                    x="DATE",
                    axes={},
                    widthPercent=100,
                    title="Stock Performance Trend"
                ),
                change_data_in_chart(
                    data=article_by_source,
                    chart=horizontal_bar_chart,
                    x="Source",
                    axes={"No. of Articles": "y"},
                    widthPercent=50,
                    title="Top Sources"
                ),

                change_data_in_chart(
                    data=stock_by_sentiment_score,
                    chart=bar_chart,
                    x="Stock",
                    axes={"Avg. Sentiment Score": "y"},
                    widthPercent=50,
                    title="Sentiment Score by Stocks"
                ),
                # change_data_in_wordcloud(card1_total_entities, word_cloud)
            ]
        }
    ],
    "name": "Overview",
    "slug": "node1-overview"
}

node2 = {
    "listOfNodes": [
        change_name_and_slug_in_individual(name='GOOGL'),
        change_name_and_slug_in_individual(name='AMZN'),
        change_name_and_slug_in_individual(name='FB'),
        change_name_and_slug_in_individual(name='AAPL'),
        change_name_and_slug_in_individual(name='IBM'),
    ],
    "listOfCards": [
        smaller_name_and_slug_in_individual(name='unknown')
    ],
    "name": "Single Stock Analysis",
    "slug": "node2-overview"
}

sample_dummy_data_for_stock = {
    "listOfNodes": [
        node1,
        node2
    ],
    "listOfCards": [],
    "name": "Overview card",
    "slug": "fdfdfd_overview"
}

"""
bar_chart = [
[
    "text",
    "bank account number",
    "credit card",
    "New York",
    "America",
    "money",
    "John",
    "numbers"
],
[
    "score",
    0.940398,
    0.742339,
    0.737608,
    0.366456,
    0.365641,
    0.361568,
    0.361102
]
]

pie_chart = [
        [
            "Cash",
            7
        ],
        [
            "Debt",
            28
        ],
        [
            "Equity",
            65
        ]
]
"""

from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _


class Role(Group):
    class Meta(object):
        proxy = True
        app_label = 'auth'
        verbose_name = _('Role')


# model management


class TrainAlgorithmMapping(models.Model):
    name = models.CharField(max_length=300, null=True)
    slug = models.SlugField(null=False, blank=True, max_length=300)
    trainer = models.ForeignKey(Trainer, null=False)
    config = models.TextField(default="{}")
    app_id = models.IntegerField(null=True, default=0)

    data = models.TextField(default="{}")

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    created_by = models.ForeignKey(User, null=False, db_index=True)
    deleted = models.BooleanField(default=False)

    bookmarked = models.BooleanField(default=False)
    viewed = models.BooleanField(default=False)

    class Meta(object):
        ordering = ['-created_at', '-updated_at']
        # Uncomment line below for permission details
        permissions = settings.PERMISSIONS_RELATED_TO_TRAINER

    def __str__(self):
        return " : ".join(["{}".format(x) for x in [self.name, self.created_at, self.slug]])

    def generate_slug(self):
        if not self.slug:
            self.slug = slugify(self.name + "-" + ''.join(
                random.choice(string.ascii_uppercase + string.digits) for _ in range(10)))

    def save(self, *args, **kwargs):
        self.generate_slug()
        super(TrainAlgorithmMapping, self).save(*args, **kwargs)

    def delete(self):
        try:
            self.deleted = True
            self.save()
            deploy_instance = ModelDeployment.objects.filter(deploytrainer_id=self.id)
            for iter in deploy_instance:
                iter.terminate_periodic_task()
        except Exception as err:
            raise (err)


# Deployment for Model management
class ModelDeployment(models.Model):
    name = models.CharField(max_length=300, null=True)
    slug = models.SlugField(null=False, blank=True, max_length=300)
    deploytrainer = models.ForeignKey(TrainAlgorithmMapping, null=False)
    periodic_task = models.ForeignKey(PeriodicTask, null=True)
    config = models.TextField(default="{}")

    data = models.TextField(default="{}")
    status = models.CharField(max_length=100, null=True, default="NOT STARTED")

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    created_by = models.ForeignKey(User, null=False, db_index=True)
    deleted = models.BooleanField(default=False)

    bookmarked = models.BooleanField(default=False)
    viewed = models.BooleanField(default=False)

    class Meta(object):
        ordering = ['-created_at', '-updated_at']
        # Uncomment line below for permission details
        permissions = settings.PERMISSIONS_RELATED_TO_TRAINER

    def __str__(self):
        return " : ".join(["{}".format(x) for x in [self.name, self.created_at, self.slug]])

    def generate_slug(self):
        if not self.slug:
            self.slug = slugify(self.name + "-" + ''.join(
                random.choice(string.ascii_uppercase + string.digits) for _ in range(10)))

    def save(self, *args, **kwargs):
        self.generate_slug()
        super(ModelDeployment, self).save(*args, **kwargs)

    def start_periodically(self):
        '''
        timing_details = {
            'type': 'crontab',
            'crontab': {
                'minute': '30',
                'hour': '*',
                'day_of_week': '*',
                'day_of_month': '*',
                'month_of_year': '*',
                'timezone': 'Kolkata/Asia'
            },
            'interval': {
                'every': 30,
                'period': 'seconds'
            }
        }
        :param timing_details:
        :return:
        '''
        if self.periodic_task is None:
            pass
        else:
            return False
        config = json.loads(self.config)
        config['trainer_details'] = self.add_trainer_details()
        config['modeldeployment_details'] = self.add_modeldeployment_details()
        config['user_details'] = self.add_user_details()
        timing_details = config['timing_details']
        periodic_task = None
        schedule, schedule_type = get_schedule(timing_details)
        if schedule_type == 'crontab':
            periodic_task = PeriodicTask.objects.create(
                crontab=schedule,
                name=self.slug,
                task='call_dataset_then_score',
                args='["hello"]',
                kwargs=json.dumps(config)
            )
        else:
            periodic_task = PeriodicTask.objects.create(
                interval=schedule,
                name=self.slug,
                task='call_dataset_then_score',
                args='["hello"]',
                kwargs=json.dumps(config)
            )

        if periodic_task is not None:
            self.periodic_task = periodic_task
            self.status = 'STARTED'
            self.save()
            return True
        else:
            pass

    def add_trainer_details(self):
        return {
            'trainer_slug': self.deploytrainer.trainer.slug
        }

    def add_modeldeployment_details(self):
        return {
            'modeldeployment_slug': self.slug
        }

    def add_user_details(self):
        return {
            'username': self.created_by.username
        }

    def delete(self):
        try:
            self.deleted = True
            self.disable_periodic_task()

        except Exception as err:
            print(err)

    def disable_periodic_task(self):
        from django_celery_beat.models import PeriodicTask
        try:
            periodic_object = PeriodicTask.objects.get(pk=self.periodic_task_id)
            if periodic_object.enabled == False:
                pass
            else:
                periodic_object.enabled = False
                periodic_object.save()
        except:
            print("Unable to stop Periodic Task !!!")
        self.save()

    def resume_periodic_task(self):
        '''
            >>> periodic_task.enabled = True
            >>> periodic_task.save()
        :return:
        '''
        self.periodic_task.enabled = True
        self.status = 'STARTED'
        self.save()
        self.save()

    def terminate_periodic_task(self):
        '''
            >>> task = PeriodicTask.objects.get(name='simple-add')
            >>> task.delete()
        :return:
        '''
        self.periodic_task.delete()
        self.periodic_task = None
        self.status = 'TERMINATED'
        self.save()
        self.deleted = True
        self.save()

    def get_periodic_task_details(self):

        if self.periodic_task:
            return {
                'name': self.periodic_task.name,
                'status': self.periodic_task.enabled
            }
        else:
            return None

    def change_timings_of_periodic_task(self):
        pass

    def change_config(self):
        pass

    def get_trainer_details_for_score(self, score_name):
        score_details = {
            "name": score_name,
            "config": {
                "selectedModel": {},
                "variablesSelection": {},
                "app_id": ""
            }
        }
        score_details['config'] = json.loads(self.deploytrainer.config)
        return score_details
        trainer_data = json.loads(self.deploytrainer.trainer.data)
        train_algo_mapping_data = json.loads(self.deploytrainer.data)
        model_dropdowns = trainer_data['model_dropdown']
        for model_dropdown in model_dropdowns:
            if model_dropdown['name'] == train_algo_mapping_data['name']:
                score_details['config']['selectModel'] = model_dropdown
                break
        score_details["config"]["app_id"] = self.deploytrainer.trainer.app_id
        return score_details


class DatasetScoreDeployment(models.Model):
    name = models.CharField(max_length=300, null=True)
    slug = models.SlugField(null=False, blank=True, max_length=300
                            )
    deployment = models.ForeignKey(ModelDeployment, null=False)
    dataset = models.ForeignKey(Dataset, null=True)
    score = models.ForeignKey(Score, null=True)

    config = models.TextField(default="{}")

    data = models.TextField(default="{}")
    status = models.CharField(max_length=100, null=True, default="NOT STARTED")

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    created_by = models.ForeignKey(User, null=False, db_index=True)
    deleted = models.BooleanField(default=False)

    bookmarked = models.BooleanField(default=False)
    viewed = models.BooleanField(default=False)

    class Meta(object):
        ordering = ['-created_at', '-updated_at']
        # Uncomment line below for permission details
        permissions = settings.PERMISSIONS_RELATED_TO_TRAINER

    def __str__(self):
        return " : ".join(["{}".format(x) for x in [self.name, self.created_at, self.slug]])

    def generate_slug(self):
        if not self.slug:
            self.slug = slugify(self.name + "-" + ''.join(
                random.choice(string.ascii_uppercase + string.digits) for _ in range(10)))

    def save(self, *args, **kwargs):
        self.generate_slug()
        super(DatasetScoreDeployment, self).save(*args, **kwargs)


class OutlookToken(models.Model):
    refresh_token = models.CharField(max_length=5000, null=True)
    access_token = models.CharField(max_length=5000, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta(object):
        ordering = ['-created_at']
        # Uncomment line below for permission details
        permissions = settings.PERMISSIONS_RELATED_TO_TRAINER

    def __str__(self):
        return " : ".join(["{}".format(x) for x in [self.refresh_token, self.created_at]])
