# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import absolute_import

from builtins import object
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from api.user_helper import UserSerializer
from django.contrib.auth.models import User
from django.conf import settings

from api.models import Dataset
from .helper import convert_to_json, convert_time_to_human
from api.helper import get_job_status, get_message
import copy
import simplejson as json

from api.utils import get_permissions


class DatasetSerializer(serializers.ModelSerializer):

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
        get_job_status(instance)
        ret = super(DatasetSerializer, self).to_representation(instance)
        ret = convert_to_json(ret)
        ret = convert_time_to_human(ret)
        ret['created_by'] = UserSerializer(instance.created_by).data

        try:
            # ret['message'] = get_message(instance.job)
            message_list = json.loads(instance.job.message_log)
            if message_list[-1]['globalCompletionPercentage'] == -1:
                ret['message'] = get_message(instance.job)
            else:
                ret['message'] = json.loads(instance.job.message_log)
        except:
            ret['message'] = None
        try:
            initial_messages = instance.job.messages
            ret['initial_messages'] = json.loads(initial_messages)
        except:
            ret['initial_messages'] = None

        if instance.viewed == False and instance.status=='SUCCESS':
            instance.viewed = True
            instance.save()

        if instance.datasource_type=='fileUpload':
            PROCEED_TO_UPLOAD_CONSTANT = settings.PROCEED_TO_UPLOAD_CONSTANT
            try:
                from api.helper import convert_to_humanize
                ret['file_size']=convert_to_humanize(instance.input_file.size)
                if(instance.input_file.size < PROCEED_TO_UPLOAD_CONSTANT or ret['status']=='SUCCESS'):
                    ret['proceed_for_loading']=True
                else:
                    ret['proceed_for_loading'] = False
            except:
                ret['file_size']=-1
                ret['proceed_for_loading'] = True

        try:
            ret['job_status'] = instance.job.status
        except:
            ret['job_status'] = None

        if 'request' in self.context:
            # permission details
            permission_details = get_permissions(
                user=self.context['request'].user,
                model=self.Meta.model.__name__.lower(),
            )
            ret['permission_details'] = permission_details

        return ret

    class Meta(object):
        model = Dataset
        exclude = ( 'id', 'updated_at',)


class DataListSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        get_job_status(instance)
        ret = super(DataListSerializer, self).to_representation(instance)
        ret['brief_info'] = instance.get_brief_info()

        try:
            ret['completed_percentage']=get_message(instance.job)[-1]['globalCompletionPercentage']
            ret['completed_message']=get_message(instance.job)[-1]['shortExplanation']
        except:
            ret['completed_percentage'] = 0
            ret['completed_message']="Analyzing Target Variable"
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
        model = Dataset
        fields = (
            "slug",
            "name",
            "created_at",
            "updated_at",
            "input_file",
            "datasource_type",
            "bookmarked",
            "analysis_done",
            "file_remote",
            "status",
            "viewed"
        )


class DataNameListSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        ret = super(DataNameListSerializer, self).to_representation(instance)
        #metadata=json.loads(instance.meta_data)
        #ret['Target']=metadata['headers']
        return ret

    class Meta(object):
        model = Dataset
        fields = (
            "slug",
            "name"
        )
