from __future__ import print_function
from __future__ import absolute_import
from builtins import zip
from builtins import object
import simplejson as json

import os
import re

import sys
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.utils import humanize_datetime
from sjsclient import client

from api.helper import JobserverDetails, get_job_status, get_message
from api.user_helper import UserSerializer
from .models import Insight, Dataset, Trainer, Score, Job, Robo, Audioset, StockDataset, CustomApps, \
    TrainAlgorithmMapping, ModelDeployment, DatasetScoreDeployment, OutlookToken

from django.conf import settings
import subprocess

# import json
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import HtmlFormatter

from django.utils.safestring import mark_safe


def submit_job_through_yarn(slug, class_name, job_config, job_name=None, message_slug=None, queue_name=None,
                            app_id=None):
    config = generate_job_config(class_name, job_config, job_name, message_slug, slug, app_id)

    # try:
    if hasattr(settings, 'CELERY_SCRIPTS_DIR'):
        scripts_dir = settings.CELERY_SCRIPTS_DIR
    else:
        base_dir = correct_base_dir()
        scripts_dir = os.path.join(base_dir, "scripts")

    egg_file_path = os.path.join(scripts_dir, "marlabs_bi_jobs-0.0.0-py3.6.egg")
    driver_file = os.path.join(scripts_dir, "driver.py")

    print("About to submit job through YARN")
    # Submit_job to YARN
    print(queue_name)

    '''
    if queue_name is None:
        command_array = ["spark-submit", "--name", job_name, "--master", "yarn", "--py-files", egg_file_path,
                         driver_file,
                         json.dumps(config)]
    else:
        command_array = ["spark-submit", "--name", job_name, "--master", "yarn", "--queue", queue_name,
                         "--py-files", egg_file_path, driver_file,
                         json.dumps(config)]
    '''
    '''
    command_array = ["spark-submit", "--driver-java-options", "\"-Dlog4j.configuration=file:/tmp/log4j.properties\"" , "--master", "yarn", "--py-files", egg_file_path,
                        # "--packages com.amazonaws:aws-java-sdk-pom:1.10.34,org.apache.hadoop:hadoop-aws:2.6.0",
                         driver_file,
                         json.dumps(config)]

    '''

    # Why is the subprocess.Popen argument length limit smaller than what the OS reports?
    # xargs --show-limits < /dev/null
    # limit in 131071
    if len(json.dumps(config['job_config']['config'])) > 100000:
        import copy
        temp_config = copy.deepcopy(config)
        temp_config['job_config']['config'] = None
        command_array = ["spark-submit", "--master", "yarn", "--deploy-mode", "client", "--py-files", egg_file_path,
                         # "--packages com.amazonaws:aws-java-sdk-pom:1.10.34,org.apache.hadoop:hadoop-aws:2.6.0",
                         driver_file,
                         json.dumps(temp_config)]
    else:
        command_array = ["spark-submit", "--master", "yarn", "--deploy-mode", "client", "--py-files", egg_file_path,
                         # "--packages com.amazonaws:aws-java-sdk-pom:1.10.34,org.apache.hadoop:hadoop-aws:2.6.0",
                         driver_file,
                         json.dumps(config)]

    application_id = ""

    from .tasks import submit_job_separate_task1, submit_job_separate_task

    if settings.SUBMIT_JOB_THROUGH_CELERY:
        # pass
        submit_job_separate_task.delay(command_array, slug)
    else:
        submit_job_separate_task1(command_array, slug)

    return {
        "application_id": application_id,
        "command_array": command_array,
        "queue_name": queue_name,
        "egg_file_path": egg_file_path,
        "driver_py_file_path": driver_file,
        "config": config
    }

    # except Exception as e:
    #     print 'Error-->submit_job_through_yarn--->'
    #     print e
    #     pass
    # from smtp_email import send_alert_through_email
    # send_alert_through_email(e)


def generate_job_config(class_name, job_config, job_name, message_slug, slug, app_id=None):
    # here
    temp_config = JobserverDetails.get_config(slug=slug,
                                              class_name=class_name,
                                              job_name=job_name,
                                              message_slug=message_slug,
                                              app_id=app_id
                                              )
    config = {}
    config['job_config'] = job_config
    config['job_config'].update(temp_config)

    return config


def submit_job_through_job_server(slug, class_name, job_config, job_name=None, message_slug=None):
    sjs = client.Client(JobserverDetails.get_jobserver_url())
    app = sjs.apps.get(JobserverDetails.get_app())
    ctx = sjs.contexts.get(JobserverDetails.get_context())

    # class path for all class name are same, it is job_type which distinguishes which scripts to run
    # actually not much use of this function for now. things may change in future.
    class_path = JobserverDetails.get_class_path(class_name)

    config = generate_job_config(class_name, job_config, job_name, message_slug, slug)

    try:
        job = sjs.jobs.create(app, class_path, ctx=ctx, conf=json.dumps(config))
    except Exception as e:
        from smtp_email import send_alert_through_email
        send_alert_through_email(e)
        return None

    # print
    job_url = JobserverDetails.print_job_details(job)
    return job_url


def submit_job(slug, class_name, job_config, job_name=None, message_slug=None, queue_name=None, app_id=None):
    """Based on config, submit jobs either through YARN or job server"""
    if settings.SUBMIT_JOB_THROUGH_YARN:
        return submit_job_through_yarn(slug, class_name, job_config, job_name, message_slug, queue_name=queue_name,
                                       app_id=app_id)
    else:
        return submit_job_through_job_server(slug, class_name, job_config, job_name, message_slug)


def convert_to_string(data):
    keys = ['compare_type', 'column_data_raw', 'config', 'data', 'model_data', 'meta_data']

    for key in keys:
        if key in data:
            value = data[key]
            if isinstance(value, str):
                pass
            elif isinstance(value, dict):
                data[key] = json.dumps(value)

    return data


def convert_to_json(data):
    keys = ['compare_type', 'column_data_raw', 'config', 'data', 'model_data', 'meta_data', 'crawled_data', 'stock_symbols1']

    for key in keys:
        if key in data:
            value = data[key]
            data[key] = json.loads(value)

    string_to_list_keys = ['stock_symbols']

    # for key in string_to_list_keys:
    #     if key in data:
    #         value = data[key]
    #         # data[key] = value.split(',')
    #         value = json.loads(value)
    #         data[key] = json.loads(value)
    return data


def convert_time_to_human(data):
    keys = ['created_on', 'updated_on']

    for key in keys:
        if key in data:
            value = data[key]
            data[key] = humanize_datetime.humanize_strptime(value)
    return data


def update_name_in_json_data(ret):
    if 'data' in ret:
        if 'name' in ret['data']:
            ret['data']['name'] = ret['name']
    return ret


# TODO: use dataserializer
class InsightSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        get_job_status(instance)
        ret = super(InsightSerializer, self).to_representation(instance)
        dataset = ret['dataset']
        dataset_object = Dataset.objects.get(pk=dataset)
        # dataset_object = instance.dataset
        ret['dataset'] = dataset_object.slug
        ret['dataset_name'] = dataset_object.name
        ret = convert_to_json(ret)
        ret['created_by'] = UserSerializer(User.objects.get(pk=ret['created_by'])).data
        # ret['created_by'] = UserSerializer(instance.created_by).data
        if instance.viewed == False and instance.status == 'SUCCESS':
            instance.viewed = True
            instance.save()
        try:
            message_list = get_message(instance.job)
            if message_list[-1]['globalCompletionPercentage'] == -1:
                ret['message'] = get_message(instance.job)
            else:
                ret['message'] = json.loads(instance.job.message_log)
            # if message_list is not None:
            #     message_list = [message_list[-1]]
            # ret['message'] = message_list
        except:
            ret['message'] = None
        try:
            initial_messages = instance.job.messages
            ret['initial_messages'] = json.loads(initial_messages)
        except:
            ret['initial_messages'] = None

        if dataset_object.datasource_type == 'fileUpload':
            PROCEED_TO_UPLOAD_CONSTANT = settings.PROCEED_TO_UPLOAD_CONSTANT
            try:
                from api.helper import convert_to_humanize
                ret['file_size'] = convert_to_humanize(dataset_object.input_file.size)
                if (dataset_object.input_file.size < PROCEED_TO_UPLOAD_CONSTANT or ret['status'] == 'SUCCESS'):
                    ret['proceed_for_loading'] = True
                else:
                    ret['proceed_for_loading'] = False
            except:
                ret['file_size'] = -1
                ret['proceed_for_loading'] = True
        try:
            ret['job_status'] = instance.job.status
        except:
            ret['job_status'] = None
        # permission details
        permission_details = get_permissions(
            user=self.context['request'].user,
            model=self.Meta.model.__name__.lower(),
        )
        ret['permission_details'] = permission_details
        ret = update_name_in_json_data(ret)
        return ret

    def update(self, instance, validated_data):
        instance.compare_with = validated_data.get("compare_with", instance.compare_with)
        instance.compare_type = validated_data.get("compare_type", instance.compare_type)
        instance.column_data_raw = validated_data.get("column_data_raw", instance.column_data_raw)
        instance.status = validated_data.get("status", instance.status)
        instance.live_status = validated_data.get("live_status", instance.live_status)
        instance.analysis_done = validated_data.get("analysis_done", instance.analysis_done)
        instance.name = validated_data.get("name", instance.name)
        instance.deleted = validated_data.get("deleted", instance.deleted)

        instance.save()

        return instance

    class Meta(object):
        model = Insight
        exclude = ('compare_with', 'compare_type', 'column_data_raw', 'id')


class InsightListSerializers(serializers.ModelSerializer):

    def to_representation(self, instance):
        get_job_status(instance)
        ret = super(InsightListSerializers, self).to_representation(instance)
        dataset = ret['dataset']
        # dataset_object = Dataset.objects.get(pk=dataset)
        dataset_object = instance.dataset
        ret['dataset'] = dataset_object.slug
        ret['dataset_name'] = dataset_object.name
        ret = convert_to_json(ret)
        # ret['created_by'] = UserSerializer(User.objects.get(pk=ret['created_by'])).data
        ret['created_by'] = UserSerializer(instance.created_by).data
        ret['brief_info'] = instance.get_brief_info()

        # ret['is_viewed'] = False
        try:
            ret['completed_percentage'] = get_message(instance.job)[-1]['globalCompletionPercentage']
            ret['completed_message'] = get_message(instance.job)[-1]['shortExplanation']
        except:
            ret['completed_percentage'] = 0
            ret['completed_message'] = "Analyzing Target Variable"
        try:
            ret['job_status'] = instance.job.status
        except:
            ret['job_status'] = None
        # permission details
        permission_details = get_permissions(
            user=self.context['request'].user,
            model=self.Meta.model.__name__.lower(),
        )
        ret['permission_details'] = permission_details
        return ret

    def get_brief_info(self):
        pass

    class Meta(object):
        model = Insight
        exclude = (
            'compare_with',
            'compare_type',
            'column_data_raw',
            'id',
            'config',
            'data'
        )


class TrainerSerlializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        get_job_status(instance)
        ret = super(TrainerSerlializer, self).to_representation(instance)
        dataset = ret['dataset']
        dataset_object = Dataset.objects.get(pk=dataset)
        ret['dataset'] = dataset_object.slug
        ret['dataset_name'] = dataset_object.name
        ret = convert_to_json(ret)
        ret['created_by'] = UserSerializer(User.objects.get(pk=ret['created_by'])).data
        if instance.viewed == False and instance.status == 'SUCCESS':
            instance.viewed = True
            instance.save()
        try:
            message_list = get_message(instance.job)
            if message_list[-1]['globalCompletionPercentage'] == -1:
                ret['message'] = get_message(instance.job)
            else:
                ret['message'] = json.loads(instance.job.message_log)
            # if message_list is not None:
            #     message_list = [message_list[-1]]
            # ret['message'] = message_list
        except:
            ret['message'] = None
        try:
            initial_messages = instance.job.messages
            ret['initial_messages'] = json.loads(initial_messages)
        except:
            ret['initial_messages'] = None

        if dataset_object.datasource_type == 'fileUpload':
            PROCEED_TO_UPLOAD_CONSTANT = settings.PROCEED_TO_UPLOAD_CONSTANT
            try:
                from api.helper import convert_to_humanize
                ret['file_size'] = convert_to_humanize(dataset_object.input_file.size)
                if (dataset_object.input_file.size < PROCEED_TO_UPLOAD_CONSTANT or ret['status'] == 'SUCCESS'):
                    ret['proceed_for_loading'] = True
                else:
                    ret['proceed_for_loading'] = False
            except:
                ret['file_size'] = -1
                ret['proceed_for_loading'] = True

        if instance.job:
            ret['job_status'] = instance.job.status
        else:
            ret['job_status'] = None

        # Adding TrainAlgorithmMapping details
        try:
            TrainAlgoList = dict()
            TrainAlgo_objects = TrainAlgorithmMapping.objects.filter(trainer_id=instance.id)
            for index, i in enumerate(TrainAlgo_objects):
                TrainAlgoList.update({index: {'model_id': i.name, 'slug': i.slug}})
            ret['TrainAlgorithmMapping'] = TrainAlgoList
        except Exception as err:
            ret['TrainAlgorithmMapping'] = None
            print(err)
        # permission details
        permission_details = get_permissions(
            user=self.context['request'].user,
            model=self.Meta.model.__name__.lower(),
        )
        ret['permission_details'] = permission_details
        ret = update_name_in_json_data(ret)
        return ret

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.column_data_raw = validated_data.get("column_data_raw", instance.column_data_raw)
        instance.deleted = validated_data.get("deleted", instance.deleted)
        instance.bookmarked = validated_data.get("bookmarked", instance.bookmarked)
        instance.data = validated_data.get("data", instance.data)
        instance.live_status = validated_data.get("live_status", instance.live_status)
        instance.status = validated_data.get("status", instance.status)

        instance.save()

        return instance

    class Meta(object):
        model = Trainer
        exclude = ('id', 'job')


class TrainerListSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        # get_job_status(instance)
        ret = super(TrainerListSerializer, self).to_representation(instance)
        dataset = ret['dataset']
        dataset_object = instance.dataset
        ret['dataset'] = dataset_object.slug
        ret['dataset_name'] = dataset_object.name
        ret = convert_to_json(ret)
        ret['created_by'] = UserSerializer(instance.created_by).data
        ret['brief_info'] = instance.get_brief_info()
        try:
            ret['completed_percentage'] = get_message(instance.job)[-1]['globalCompletionPercentage']
            ret['completed_message'] = get_message(instance.job)[-1]['shortExplanation']
        except:
            ret['completed_percentage'] = 0
            ret['completed_message'] = "Analyzing Target Variable"
        try:
            ret['job_status'] = instance.job.status
        except:
            ret['job_status'] = None
        # permission details
        permission_details = get_permissions(
            user=self.context['request'].user,
            model=self.Meta.model.__name__.lower(),
        )
        ret['permission_details'] = permission_details
        return ret

    class Meta(object):
        model = Trainer
        exclude = (
            'column_data_raw',
            'id',
            'config',
            'data'
        )


class ScoreSerlializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        get_job_status(instance)
        ret = super(ScoreSerlializer, self).to_representation(instance)
        trainer = ret['trainer']
        trainer_object = Trainer.objects.get(pk=trainer)
        ret['trainer'] = trainer_object.slug
        ret['trainer_name'] = trainer_object.name
        ret['dataset'] = trainer_object.dataset.slug
        dataset = ret['dataset']
        # dataset_object = Dataset.objects.get(pk=dataset)
        ret['dataset_name'] = trainer_object.dataset.name
        ret = convert_to_json(ret)
        ret['created_by'] = UserSerializer(User.objects.get(pk=ret['created_by'])).data
        if instance.viewed == False and instance.status == 'SUCCESS':
            instance.viewed = True
            instance.save()
        try:
            message_list = get_message(instance.job)
            if message_list[-1]['globalCompletionPercentage'] == -1:
                ret['message'] = get_message(instance.job)
            else:
                ret['message'] = json.loads(instance.job.message_log)
            # if message_list is not None:
            #     message_list = [message_list[-1]]
            # ret['message'] = message_list
        except:
            ret['message'] = None
        try:
            initial_messages = instance.job.messages
            ret['initial_messages'] = json.loads(initial_messages)
        except:
            ret['initial_messages'] = None
        # if dataset_object.datasource_type=='fileUpload':
        # PROCEED_TO_UPLOAD_CONSTANT = settings.PROCEED_TO_UPLOAD_CONSTANT
        # try:
        # from api.helper import convert_to_humanize
        # ret['file_size']=convert_to_humanize(dataset_object.input_file.size)
        # if(dataset_object.input_file.size < PROCEED_TO_UPLOAD_CONSTANT or ret['status']=='SUCCESS'):
        #   ret['proceed_for_loading']=True
        # else:
        #   ret['proceed_for_loading'] = False
        # except:
        #   ret['file_size']=-1
        #  ret['proceed_for_loading'] = True
        try:
            ret['job_status'] = instance.job.status
        except:
            ret['job_status'] = None
        permission_details = get_permissions(
            user=self.context['request'].user,
            model=self.Meta.model.__name__.lower(),
        )
        ret['permission_details'] = permission_details
        ret = update_name_in_json_data(ret)
        return ret

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.config = validated_data.get("config", instance.config)
        instance.deleted = validated_data.get("deleted", instance.deleted)
        instance.bookmarked = validated_data.get("bookmarked", instance.bookmarked)
        instance.data = validated_data.get("data", instance.data)
        instance.model_data = validated_data.get("model_data", instance.model_data)
        instance.column_data_raw = validated_data.get("column_data_raw", instance.column_data_raw)

        instance.save()

        return instance

    class Meta(object):
        model = Score
        exclude = ('id', 'job')


class ScoreListSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        get_job_status(instance)
        ret = super(ScoreListSerializer, self).to_representation(instance)
        trainer = ret['trainer']
        trainer_object = instance.trainer
        ret['trainer'] = trainer_object.slug
        ret['trainer_name'] = trainer_object.name
        ret['dataset'] = instance.dataset.slug
        ret['dataset_name'] = instance.dataset.name
        ret = convert_to_json(ret)
        ret['created_by'] = UserSerializer(instance.created_by).data
        ret['brief_info'] = instance.get_brief_info()
        try:
            ret['completed_percentage'] = get_message(instance.job)[-1]['globalCompletionPercentage']
            ret['completed_message'] = get_message(instance.job)[-1]['shortExplanation']
        except:
            ret['completed_percentage'] = 0
            ret['completed_message'] = "Analyzing Target Variable"
        if instance.job:
            ret['job_status'] = instance.job.status
        else:
            ret['job_status'] = 'Unknown! Job is None.'
        permission_details = get_permissions(
            user=self.context['request'].user,
            model=self.Meta.model.__name__.lower(),
        )
        ret['permission_details'] = permission_details
        return ret

    class Meta(object):
        model = Score
        exclude = (
            'column_data_raw',
            'id',
            'config',
            'data'
        )


class JobSerializer(serializers.Serializer):
    class Meta(object):
        model = Job
        exclude = ("id", "created_at")


class RoboSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Robo
        exclude = ("id", "config", "column_data_raw")

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.analysis_done = validated_data.get('analysis_done', instance.analysis_done)
        instance.deleted = validated_data.get('deleted', instance.deleted)

        instance.save()
        return instance

    def to_representation(self, instance):

        from api.datasets.serializers import DatasetSerializer
        ret = super(RoboSerializer, self).to_representation(instance)

        customer_dataset_object = Dataset.objects.get(pk=ret['customer_dataset'])
        ret['customer_dataset'] = DatasetSerializer(customer_dataset_object).data

        historical_dataset_object = Dataset.objects.get(pk=ret['historical_dataset'])
        ret['historical_dataset'] = DatasetSerializer(historical_dataset_object).data

        market_dataset_object = Dataset.objects.get(pk=ret['market_dataset'])
        ret['market_dataset'] = DatasetSerializer(market_dataset_object).data
        ret['brief_info'] = instance.get_brief_info()
        if instance.dataset_analysis_done is False:
            if customer_dataset_object.analysis_done and \
                    historical_dataset_object.analysis_done and \
                    market_dataset_object.analysis_done:
                instance.dataset_analysis_done = True
                instance.save()

        if instance.robo_analysis_done and instance.dataset_analysis_done:
            instance.analysis_done = True
            instance.status = "SUCCESS"
            instance.save()

        ret = convert_to_json(ret)
        ret['created_by'] = UserSerializer(User.objects.get(pk=ret['created_by'])).data
        ret['analysis_done'] = instance.analysis_done

        if instance.viewed == False and instance.status == 'SUCCESS':
            instance.viewed = True
            instance.save()
        # try:
        #     message_list = get_message(instance)
        #
        #     if message_list is not None:
        #         message_list = [message_list[-1]]
        #     ret['message'] = message_list
        # except:
        #     ret['message'] = None
        ret = update_name_in_json_data(ret)
        return ret


class RoboListSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        from api.datasets.serializers import DatasetSerializer
        ret = super(RoboListSerializer, self).to_representation(instance)

        customer_dataset_object = Dataset.objects.get(pk=ret['customer_dataset'])
        ret['customer_dataset'] = customer_dataset_object.slug

        historical_dataset_object = Dataset.objects.get(pk=ret['historical_dataset'])
        ret['historical_dataset'] = historical_dataset_object.slug

        market_dataset_object = Dataset.objects.get(pk=ret['market_dataset'])
        ret['market_dataset'] = market_dataset_object.slug

        ret['dataset_name'] = market_dataset_object.name + ", " + \
                              customer_dataset_object.name + ", " + \
                              historical_dataset_object.name
        ret['brief_info'] = instance.get_brief_info()

        if instance.analysis_done is False:
            if customer_dataset_object.analysis_done and \
                    historical_dataset_object.analysis_done and \
                    market_dataset_object.analysis_done:
                instance.analysis_done = True
                instance.status = "SUCCESS"
                instance.save()

        ret = convert_to_json(ret)
        ret['created_by'] = UserSerializer(User.objects.get(pk=ret['created_by'])).data
        ret['analysis_done'] = instance.analysis_done
        try:
            ret['completed_percentage'] = get_message(instance)[-1]['globalCompletionPercentage']
            ret['completed_message'] = get_message(instance)[-1]['shortExplanation']
        except:
            ret['completed_percentage'] = 0
            ret['completed_message'] = "Analyzing Target Variable"
        return ret

    class Meta(object):
        model = Robo
        exclude = (
            'id',
            'config',
            'data'
        )


class StockDatasetSerializer(serializers.ModelSerializer):
    # name = serializers.CharField(max_length=100,
    #                              validators=[UniqueValidator(queryset=Dataset.objects.all())]
    #                              )

    input_file = serializers.FileField(allow_null=True)

    def update(self, instance, validated_data):
        instance.meta_data = validated_data.get('meta_data', instance.meta_data)
        instance.name = validated_data.get('name', instance.name)
        instance.created_by = validated_data.get('created_by', instance.created_by)
        instance.deleted = validated_data.get('deleted', instance.deleted)
        instance.bookmarked = validated_data.get('bookmarked', instance.bookmarked)
        instance.auto_update = validated_data.get('auto_update', instance.auto_update)
        # instance.auto_update_duration = validated_data.get('auto_update_duration', instance.auto_update_duration)

        instance.save()
        return instance

    def to_representation(self, instance):
        # print get_job_status(instance)
        ret = super(StockDatasetSerializer, self).to_representation(instance)
        ret = convert_to_json(ret)
        ret = convert_time_to_human(ret)
        ret['created_by'] = UserSerializer(User.objects.get(pk=ret['created_by'])).data
        if instance.viewed == False and instance.status == 'SUCCESS':
            instance.viewed = True
            instance.save()
        # try:
        #     message_list = get_message(instance)
        #
        #     if message_list is not None:
        #         message_list = [message_list[-1]]
        #     ret['message'] = message_list
        # except:
        #     ret['message'] = None

        try:
            ret['message'] = json.loads(instance.job.messages)
            # ret['message'] = get_message(instance.job)
        except:
            ret['message'] = None
        try:
            # initial_messages = instance.job.messages
            initial_messages = instance.job.message_log
            ret['initial_messages'] = json.loads(initial_messages)
            # ret['message_log'] = initial_messages
        except:
            ret['initial_messages'] = None

        if ret['meta_data'] == dict():
            ret['meta_data_status'] = "INPROGRESS"
        else:
            ret['meta_data_status'] = "SUCCESS"

        if 'request' in self.context:
            # permission details
            permission_details = get_permissions(
                user=self.context['request'].user,
                model=StockDataset.__name__.lower(),
            )
            ret['permission_details'] = permission_details
        ret = update_name_in_json_data(ret)
        return ret

    class Meta(object):
        model = StockDataset
        exclude = ('id', 'updated_at')


class StockDatasetListSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        print(get_job_status(instance))
        ret = super(StockDatasetListSerializer, self).to_representation(instance)
        ret['brief_info'] = instance.get_brief_info()
        try:
            ret['completed_percentage'] = get_message(instance)[-1]['globalCompletionPercentage']
            ret['completed_message'] = get_message(instance)[-1]['shortExplanation']
        except:
            ret['completed_percentage'] = 0
            ret['completed_message'] = "Analyzing Target Variable"

        permission_details = get_permissions(
            user=self.context['request'].user,
            model=self.Meta.model.__name__.lower(),
        )
        ret['permission_details'] = permission_details
        return ret

    class Meta(object):
        model = StockDataset
        fields = (
            "slug",
            "name",
            "created_at",
            "updated_at",
            "input_file",
            "bookmarked",
            "analysis_done",
            "status",
            "viewed",
        )


class AudiosetSerializer(serializers.ModelSerializer):
    # name = serializers.CharField(max_length=100,
    #                              validators=[UniqueValidator(queryset=Dataset.objects.all())]
    #                              )

    input_file = serializers.FileField(allow_null=True)

    def update(self, instance, validated_data):
        instance.meta_data = validated_data.get('meta_data', instance.meta_data)
        instance.name = validated_data.get('name', instance.name)
        instance.created_by = validated_data.get('created_by', instance.created_by)
        instance.deleted = validated_data.get('deleted', instance.deleted)
        instance.bookmarked = validated_data.get('bookmarked', instance.bookmarked)
        instance.auto_update = validated_data.get('auto_update', instance.auto_update)
        instance.auto_update_duration = validated_data.get('auto_update_duration', instance.auto_update_duration)
        instance.datasource_details = validated_data.get('datasource_details', instance.datasource_details)
        instance.datasource_type = validated_data.get('datasource_type', instance.datasource_type)

        instance.save()
        return instance

    def to_representation(self, instance):
        print(get_job_status(instance))
        ret = super(AudiosetSerializer, self).to_representation(instance)
        ret = convert_to_json(ret)
        ret = convert_time_to_human(ret)
        ret['created_by'] = UserSerializer(User.objects.get(pk=ret['created_by'])).data
        if instance.viewed == False and instance.status == 'SUCCESS':
            instance.viewed = True
            instance.save()
        try:
            message_list = get_message(instance)

            if message_list is not None:
                message_list = [message_list[-1]]
            ret['message'] = message_list
        except:
            ret['message'] = None
        ret = update_name_in_json_data(ret)
        return ret

    class Meta(object):
        model = Audioset
        exclude = ('id', 'updated_at')


class AudioListSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        ret = super(AudioListSerializer, self).to_representation(instance)
        ret['brief_info'] = instance.get_brief_info()
        try:
            ret['completed_percentage'] = get_message(instance.job)[-1]['globalCompletionPercentage']
            ret['completed_message'] = get_message(instance.job)[-1]['shortExplanation']
        except:
            ret['completed_percentage'] = 0
            ret['completed_message'] = "Analyzing Target Variable"
        return ret

    class Meta(object):
        model = Audioset
        fields = (
            "slug",
            "name",
            "created_at",
            "updated_at",
            "input_file",
            "datasource_type",
            "bookmarked",
            "analysis_done",
            "file_remote"
        )


class AppListSerializers(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super(AppListSerializers, self).to_representation(instance)
        ret['created_by'] = UserSerializer(User.objects.get(pk=ret['created_by'])).data['username']
        # add tags object
        template_tags = settings.APPS_KEYWORD_TEMPLATE
        if ret['tags'] != None:
            tags = ret['tags'].split(",")
            tag_object = []
            for obj in template_tags:
                if obj['name'] in tags:
                    tag_object.append(obj)
            # print tag_object
            ret['tags'] = tag_object
            # add all keys list
            ret['tag_keywords'] = self.add_all_tag_keywords(template_tags)

            CUSTOM_WORD1_APPS = settings.CUSTOM_WORD1_APPS
            CUSTOM_WORD2_APPS = settings.CUSTOM_WORD2_APPS
            upper_case_name = ret['name'].upper()
            # print upper_case_name
            ret['custom_word1'] = CUSTOM_WORD1_APPS[upper_case_name]
            ret['custom_word2'] = CUSTOM_WORD2_APPS[upper_case_name]
        try:
            ret['completed_percentage'] = get_message(instance.job)[-1]['globalCompletionPercentage']
            ret['completed_message'] = get_message(instance.job)[-1]['shortExplanation']
        except:
            ret['completed_percentage'] = 0
            ret['completed_message'] = "Analyzing Target Variable"
        return ret

    def add_all_tag_keywords(self, template_tags):
        tag_keywords = []
        for key in template_tags:
            tag_keywords.append(key['name'])
        return tag_keywords

    class Meta(object):
        model = CustomApps
        fields = '__all__'


class AppSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        # print "in app serializers"
        ret = super(AppSerializer, self).to_representation(instance)
        ret['created_by'] = UserSerializer(User.objects.get(pk=ret['created_by'])).data
        if ret['tags'] != None:
            tags = ret['tags'].split(",")
            tag_object = []

            template_tags = settings.APPS_KEYWORD_TEMPLATE
            for obj in template_tags:
                if obj['name'] in tags:
                    tag_object.append(obj)

            # print tag_object

            ret['tags'] = tag_object

        CUSTOM_WORD1_APPS = settings.CUSTOM_WORD1_APPS
        CUSTOM_WORD2_APPS = settings.CUSTOM_WORD2_APPS
        upper_case_name = ret['name'].upper()
        # print upper_case_name
        ret['CUSTOM_WORD1_APPS'] = CUSTOM_WORD1_APPS[upper_case_name]
        ret['CUSTOM_WORD2_APPS'] = CUSTOM_WORD2_APPS[upper_case_name]
        if instance.viewed == False and instance.status == 'SUCCESS':
            instance.viewed = True
            instance.save()
        try:
            message_list = get_message(instance)

            if message_list is not None:
                message_list = [message_list[-1]]
            ret['message'] = message_list
        except:
            ret['message'] = None
        return ret

    def update(self, instance, validated_data):
        instance.app_id = validated_data.get("app_id", instance.app_id)
        instance.displayName = validated_data.get("displayName", instance.displayName)
        instance.description = validated_data.get("description", instance.description)
        instance.status = validated_data.get("status", instance.status)
        instance.tags = validated_data.get("tags", instance.tags)
        instance.iconName = validated_data.get("iconName", instance.iconName)
        instance.name = validated_data.get("name", instance.name)
        instance.app_url = validated_data.get("app_url", instance.app_url)
        instance.app_type = validated_data.get("app_type", instance.app_type)

        instance.save()

        return instance

    class Meta(object):
        model = CustomApps
        fields = '__all__'

#
# class RegressionSerlializer(serializers.ModelSerializer):
#
#     def to_representation(self, instance):
#         get_job_status(instance)
#         ret = super(RegressionSerlializer, self).to_representation(instance)
#         dataset = ret['dataset']
#         dataset_object = Dataset.objects.get(pk=dataset)
#         ret['dataset'] = dataset_object.slug
#         ret['dataset_name'] = dataset_object.name
#         ret = convert_to_json(ret)
#         ret['created_by'] = UserSerializer(User.objects.get(pk=ret['created_by'])).data
#         if instance.viewed == False and instance.status=='SUCCESS':
#             instance.viewed = True
#             instance.save()
#         try:
#             message_list = get_message(instance.job)
#
#             if message_list is not None:
#                 message_list = [message_list[-1]]
#             ret['message'] = message_list
#         except:
#             ret['message'] = None
#
#         if dataset_object.datasource_type=='fileUpload':
#             PROCEED_TO_UPLOAD_CONSTANT = settings.PROCEED_TO_UPLOAD_CONSTANT
#             try:
#                 from api.helper import convert_to_humanize
#                 ret['file_size']=convert_to_humanize(dataset_object.input_file.size)
#                 if(dataset_object.input_file.size < PROCEED_TO_UPLOAD_CONSTANT or ret['status']=='SUCCESS'):
#                     ret['proceed_for_loading']=True
#                 else:
#                     ret['proceed_for_loading'] = False
#             except:
#                 ret['file_size']=-1
#                 ret['proceed_for_loading'] = True
#         ret['job_status'] = instance.job.status
#         # permission details
#         permission_details = get_permissions(
#             user=self.context['request'].user,
#             model=self.Meta.model.__name__.lower(),
#         )
#         ret['permission_details'] = permission_details
#         return ret
#
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get("name", instance.name)
#         instance.column_data_raw = validated_data.get("column_data_raw", instance.column_data_raw)
#         instance.deleted = validated_data.get("deleted", instance.deleted)
#         instance.bookmarked = validated_data.get("bookmarked", instance.bookmarked)
#         instance.data = validated_data.get("data", instance.data)
#         instance.live_status = validated_data.get("live_status", instance.live_status)
#         instance.status = validated_data.get("status", instance.status)
#
#
#
#         instance.save()
#
#         return instance
#
#     class Meta:
#         model = Regression
#         exclude = ('id', 'job')

#
# class RegressionListSerializer(serializers.ModelSerializer):
#
#     def to_representation(self, instance):
#         get_job_status(instance)
#         ret = super(RegressionListSerializer, self).to_representation(instance)
#         dataset = ret['dataset']
#         dataset_object = Dataset.objects.get(pk=dataset)
#         ret['dataset'] = dataset_object.slug
#         ret['dataset_name'] = dataset_object.name
#         ret = convert_to_json(ret)
#         ret['created_by'] = UserSerializer(User.objects.get(pk=ret['created_by'])).data
#         ret['brief_info'] = instance.get_brief_info()
#         try:
#             ret['completed_percentage']=get_message(instance.job)[-1]['globalCompletionPercentage']
#             ret['completed_message']=get_message(instance.job)[-1]['shortExplanation']
#         except:
#             ret['completed_percentage'] = 0
#             ret['completed_message']="Analyzing Target Variable"
#         ret['job_status'] = instance.job.status
#         # permission details
#         permission_details = get_permissions(
#             user=self.context['request'].user,
#             model=self.Meta.model.__name__.lower(),
#         )
#         ret['permission_details'] = permission_details
#         return ret
#
#
#     class Meta:
#         model = Regression
#         exclude =  (
#             'column_data_raw',
#             'id',
#             'config',
#             'data'
#         )


def correct_base_dir():
    if settings.BASE_DIR.endswith("config") or settings.BASE_DIR.endswith("config/"):
        return os.path.dirname(settings.BASE_DIR)
    else:
        return settings.BASE_DIR


def json_prettify_for_admin(json_val):
    response = json.dumps(json_val, sort_keys=True, indent=2)
    formatter = HtmlFormatter(style='colorful')
    response = highlight(response, JsonLexer(), formatter)
    style = "<style>" + formatter.get_style_defs() + "</style><br>"

    return mark_safe(style + response + "<hr>")


def get_permissions(user, model, type='retrieve'):
    if model == 'dataset':
        if type == 'retrieve':
            return {
                'view_dataset': user.has_perm('api.view_dataset'),
                'rename_dataset': user.has_perm('api.rename_dataset'),
                # 'rename_dataset': get_random_true_false(),
                # 'remove_dataset': get_random_true_false(),
                'remove_dataset': user.has_perm('api.remove_dataset'),
                'data_validation': user.has_perm('api.data_validation'),
                'subsetting_dataset': user.has_perm('api.subsetting_dataset'),
                'create_signal': user.has_perm('api.create_signal'),
                'create_trainer': user.has_perm('api.create_trainer'),
                'create_score': user.has_perm('api.create_score'),
            }
        if type == 'list':
            return {
                'create_dataset': user.has_perm('api.create_dataset'),
                'view_dataset': user.has_perm('api.view_dataset'),
                'share_dataset': user.has_perm('api.share_dataset'),
                'upload_from_file': user.has_perm('api.upload_from_file'),
                'upload_from_mysql': user.has_perm('api.upload_from_mysql'),
                'upload_from_mssql': user.has_perm('api.upload_from_mssql'),
                'upload_from_hana': user.has_perm('api.upload_from_hana'),
                'upload_from_hdfs': user.has_perm('api.upload_from_hdfs'),
            }
    if model == 'insight':
        if type == 'retrieve':
            return {
                'view_signal': user.has_perm('api.view_signal'),
                'rename_signal': user.has_perm('api.rename_signal'),
                'remove_signal': user.has_perm('api.remove_signal'),
            }
        if type == 'list':
            return {
                'create_signal': user.has_perm('api.create_signal'),
                'view_signal': user.has_perm('api.view_signal'),
                'share_signal': user.has_perm('api.share_signal'),
            }
    if model == 'trainer':
        if type == 'retrieve':
            return {
                'create_score': user.has_perm('api.create_score') and user.has_perm('api.view_score') and user.has_perm(
                    'api.view_trainer'),
                'view_trainer': user.has_perm('api.view_trainer'),
                'downlad_pmml': user.has_perm('api.downlad_pmml'),
                'rename_trainer': user.has_perm('api.rename_trainer'),
                'remove_trainer': user.has_perm('api.remove_trainer'),
                'edit_signal': user.has_perm('api.edit_trainer'),
            }
        if type == 'list':
            return {
                'create_trainer': user.has_perm('api.create_trainer') and user.has_perm('api.view_trainer'),
                'share_trainer': user.has_perm('api.share_trainer'),
            }
    if model == 'score':
        if type == 'retrieve':
            return {
                'view_score': user.has_perm('api.view_score'),
                'download_score': user.has_perm('api.download_score') and user.has_perm('api.view_score'),
                'rename_score': user.has_perm('api.rename_score'),
                'remove_score': user.has_perm('api.remove_score'),
            }
        if type == 'list':
            return {
                'create_score': user.has_perm('api.create_score') and user.has_perm('api.view_score') and user.has_perm(
                    'api.view_trainer'),
                'share_score': user.has_perm('api.share_score'),
            }
    if model == 'regression':
        if type == 'retrieve':
            return {
                'create_score': user.has_perm('api.create_score') and user.has_perm('api.view_score') and user.has_perm(
                    'api.view_trainer'),
                'view_regression': user.has_perm('api.view_regression'),
                'downlad_pmml': user.has_perm('api.downlad_pmml'),
                'rename_regression': user.has_perm('api.rename_regression'),
                'remove_regression': user.has_perm('api.remove_regression'),
            }
        if type == 'list':
            return {
                'create_regression': user.has_perm('api.create_regression'),
            }
    if model == 'stockdataset':
        if type == 'retrieve':
            return {
                'view_stock': user.has_perm('api.view_stock'),
                'rename_stock': user.has_perm('api.rename_stock'),
                'remove_stock': user.has_perm('api.remove_stock'),
            }
        if type == 'list':
            return {
                'create_stock': user.has_perm('api.create_stock') and user.has_perm('api.view_stock'),
            }
    if model == 'trainalgorithmmapping':
        if type == 'retrieve':
            return {
                'create_score': user.has_perm('api.create_score') and user.has_perm('api.view_score') and user.has_perm(
                    'api.view_trainer'),
                'view_trainer': user.has_perm('api.view_trainer'),
                'downlad_pmml': user.has_perm('api.downlad_pmml'),
                'rename_trainer': user.has_perm('api.rename_trainer'),
                'remove_trainer': user.has_perm('api.remove_trainer'),
            }
        if type == 'list':
            return {
                'create_trainer': user.has_perm('api.create_trainer') and user.has_perm('api.view_trainer'),
            }
    if model == 'modeldeployment':
        if type == 'retrieve':
            return {
                'create_score': user.has_perm('api.create_score') and user.has_perm('api.view_score') and user.has_perm(
                    'api.view_trainer'),
                'view_trainer': user.has_perm('api.view_trainer'),
                'downlad_pmml': user.has_perm('api.downlad_pmml'),
                'rename_trainer': user.has_perm('api.rename_trainer'),
                'remove_trainer': user.has_perm('api.remove_trainer'),
            }
        if type == 'list':
            return {
                'create_trainer': user.has_perm('api.create_trainer') and user.has_perm('api.view_trainer'),
            }
    if model == 'datasetscoredeployment':
        if type == 'retrieve':
            return {
                'create_score': user.has_perm('api.create_score') and user.has_perm('api.view_score') and user.has_perm(
                    'api.view_trainer'),
                'view_trainer': user.has_perm('api.view_trainer'),
                'downlad_pmml': user.has_perm('api.downlad_pmml'),
                'rename_trainer': user.has_perm('api.rename_trainer'),
                'remove_trainer': user.has_perm('api.remove_trainer'),
            }
        if type == 'list':
            return {
                'create_trainer': user.has_perm('api.create_trainer') and user.has_perm('api.view_trainer'),
            }
    return {}


def get_all_view_permission(user):
    return {
        'view_score': user.has_perm('api.view_score'),
        'view_trainer': user.has_perm('api.view_trainer'),
        'view_signal': user.has_perm('api.view_signal'),
        'view_dataset': user.has_perm('api.view_dataset'),
    }


def get_random_true_false():
    import random
    return True if random.randint(0, 1) else False


def name_check(name):
    if not check_for_empty(name):
        return -1
    if not check_for_length(name):
        return -2
    if not check_for_special_chars(name):
        return -3
    return 1


def check_for_length(name):
    return True if len(name) < settings.MAX_LENGTH_OF_NAME else False


def check_for_special_chars(name):
    import string
    KEEP_CHARACTERS_IN_NAME = string.digits + string.ascii_letters + settings.ALLOWED_SPECIAL_CHARS_IN_NAME
    for chr in name:
        if chr not in KEEP_CHARACTERS_IN_NAME:
            return False
    return True


def check_for_empty(name):
    return False if len(name) == 0 else True


# model management

class TrainAlgorithmMappingListSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        ret = super(TrainAlgorithmMappingListSerializer, self).to_representation(instance)
        ret = convert_to_json(ret)
        ret['created_by'] = UserSerializer(instance.created_by).data
        ret['model_id'] = ret['name']
        ################### Count for deployment ##########################
        deployment_count_obj = ModelDeployment.objects.filter(deploytrainer_id=instance.id, deleted=False)
        ret['deployment'] = len(deployment_count_obj)
        ####################################################################
        ret['created_on'] = ret['created_at']
        raw_data = json.loads(instance.data)
        ret['total_deployment'] = ret['deployment'] + len(
            ModelDeployment.objects.filter(deploytrainer_id=instance.id, deleted=True))
        # Fetching Data from ML
        if raw_data is not dict():
            try:
                list_data = (raw_data['listOfNodes'][0]['listOfCards'][0]['cardData'][1]['data']['tableData'])
                value = [item[1] for item in list_data]
            except:
                value = ['--', '--', '--', '--', '--']
        else:
            value = ['--', '--', '--', '--', '--']
        key = ['project_name', 'algorithm', 'training_status', 'accuracy', 'runtime']
        ret.update(dict(list(zip(key, value))))

        ret['trainer'] = instance.trainer.slug
        # return ret

        # Permission details
        permission_details = get_permissions(
            user=self.context['request'].user,
            model=self.Meta.model.__name__.lower(),
        )
        ret['permission_details'] = permission_details
        return ret

    class Meta(object):
        model = TrainAlgorithmMapping
        exclude = (

            'id',
            'config',
            'data'
        )


class TrainAlgorithmMappingSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        ret = super(TrainAlgorithmMappingSerializer, self).to_representation(instance)
        ret = convert_to_json(ret)
        trainer = ret['trainer']
        trainer_object = Trainer.objects.get(pk=trainer)
        ret['trainer'] = trainer_object.slug
        ret['created_by'] = UserSerializer(instance.created_by).data
        # return ret

        # Permission details
        if 'request' in self.context:
            permission_details = get_permissions(
                user=self.context['request'].user,
                model=self.Meta.model.__name__.lower(),
            )
            ret['permission_details'] = permission_details
        return ret

    class Meta(object):
        model = TrainAlgorithmMapping
        exclude = (
            'id',
            # 'trainer'
        )


class DeploymentListSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        ret = super(DeploymentListSerializer, self).to_representation(instance)
        ret = convert_to_json(ret)
        ret['created_by'] = UserSerializer(instance.created_by).data
        # return ret
        ################### Count for dataset and score #########################
        dataset_score_count_obj = DatasetScoreDeployment.objects.filter(deployment_id=instance.id, deleted=False)
        ret['deployment'] = len(dataset_score_count_obj)
        #########################################################################

        # Permission details
        permission_details = get_permissions(
            user=self.context['request'].user,
            model=self.Meta.model.__name__.lower(),
        )
        ret['permission_details'] = permission_details
        ret['periodic_task'] = instance.get_periodic_task_details()
        return ret

    class Meta(object):
        model = ModelDeployment
        exclude = (
            'id',
            'config',
            'data',
            'deploytrainer',
            # 'periodic_task'
        )


class DeploymentSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        ret = super(DeploymentSerializer, self).to_representation(instance)
        ret = convert_to_json(ret)
        deploytrainer = ret['deploytrainer']
        deployment_object = TrainAlgorithmMapping.objects.get(pk=deploytrainer)
        ret['deploytrainer'] = deployment_object.slug
        ret['periodic_task'] = instance.get_periodic_task_details()
        ret['created_by'] = UserSerializer(instance.created_by).data
        # return ret

        # Permission details
        permission_details = get_permissions(
            user=self.context['request'].user,
            model=self.Meta.model.__name__.lower(),
        )
        ret['permission_details'] = permission_details
        return ret

    class Meta(object):
        model = ModelDeployment
        exclude = (

            'id',
            # 'trainer'
        )


class DatasetScoreDeploymentListSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        ret = super(DatasetScoreDeploymentListSerializer, self).to_representation(instance)
        ret = convert_to_json(ret)
        ret['created_by'] = UserSerializer(instance.created_by).data
        # return ret

        # Permission details
        permission_details = get_permissions(
            user=self.context['request'].user,
            model=self.Meta.model.__name__.lower(),
        )
        ret['permission_details'] = permission_details
        return ret

    class Meta(object):
        model = DatasetScoreDeployment
        exclude = (

            'id',
            'config',
            # 'data',
            # 'dataset',
            # 'score',
            'deployment'
        )


class DatasetScoreDeploymentSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        ret = super(DatasetScoreDeploymentSerializer, self).to_representation(instance)
        ret = convert_to_json(ret)

        dataset = ret['dataset']
        if dataset == None:
            pass
        else:
            dataset_object = Dataset.objects.get(pk=dataset)
            ret['dataset'] = dataset_object.slug

        deployment = ret['deployment']
        deployment_object = ModelDeployment.objects.get(pk=deployment)
        ret['deployment'] = deployment_object.slug

        score = ret['score']
        if score == None:
            pass
        else:
            score_object = Score.objects.get(pk=score)
            ret['score'] = score_object.slug

        ret['created_by'] = UserSerializer(instance.created_by).data
        # return ret

        # Permission details
        permission_details = get_permissions(
            user=self.context['request'].user,
            model=self.Meta.model.__name__.lower(),
        )
        ret['permission_details'] = permission_details
        return ret

    class Meta(object):
        model = DatasetScoreDeployment
        exclude = (

            'id',
            # 'trainer'
        )


class TrainerNameListSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        ret = super(TrainerNameListSerializer, self).to_representation(instance)
        ret['count'] = TrainAlgorithmMapping.objects.filter(
            trainer=instance.id,
            deleted=False
        ).count()
        return ret

    class Meta(object):
        model = Trainer
        fields = (
            'slug',
            'name'
        )


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class UserListSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super(UserListSerializer, self).to_representation(instance)
        return ret

    class Meta(object):
        model = User
        fields = ("username", "id", "email")


class OutlookTokenSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super(OutlookTokenSerializer, self).to_representation(instance)
        return ret

    class Meta(object):
        model = OutlookToken
        exclude = ['id']
