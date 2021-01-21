# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import

from builtins import str
from builtins import range
import random
import json

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import Http404, JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from api.exceptions import creation_failed_exception, update_failed_exception, retrieve_failed_exception, sharing_failed_exception
from api.models import Dataset
from api.pagination import CustomPagination
from api.utils import name_check
from .helper import convert_to_string
from .serializers import DatasetSerializer, DataListSerializer, DataNameListSerializer
from api.query_filtering import get_listed_data, get_retrieve_data
from .helper import add_transformation_setting_to_ui_metadata, add_ui_metadata_to_metadata
from .helper import convert_metadata_according_to_transformation_setting
from .helper import get_advanced_setting
from api.tasks import clean_up_on_delete

from api.permission import DatasetRelatedPermission
from guardian.shortcuts import assign_perm
from django.conf import settings


# Create your views here.

class DatasetView(viewsets.ModelViewSet, viewsets.GenericViewSet):

    def get_queryset(self):
        queryset = Dataset.objects.filter(
            created_by=self.request.user,
            deleted=False,
            status__in=['SUCCESS', 'INPROGRESS', 'FAILED']
        )

        return queryset

    def get_object_from_all(self):
        return Dataset.objects.get(
            slug=self.kwargs.get('slug'),
            created_by=self.request.user
        )

    def get_serializer_context(self):
        return {'request': self.request}

    serializer_class = DatasetSerializer
    lookup_field = 'slug'
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('bookmarked', 'deleted', 'datasource_type', 'name')
    pagination_class = CustomPagination
    permission_classes = (DatasetRelatedPermission,)

    def create(self, request, *args, **kwargs):

        # try:
        if 'data' in kwargs:
            data = kwargs.get('data')
            self.request = request
        else:
            data = request.data
        data = convert_to_string(data)
        response = []
        try:
            if data['mode'] == 'autoML':
                self.mode = 'autoML'
            elif data['mode'] == 'analyst':
                self.mode = 'analyst'
            else:
                self.mode = 'analyst'
            self.save()
        except:
            pass

        try:
            data['created_by'] = request.user.id
        except:
            # data['created_by'] = None
            pass

        if 'name' in data:
            should_proceed = name_check(data['name'])
            if should_proceed < 0:
                if should_proceed == -1:
                    return creation_failed_exception("Name is empty.")
                elif should_proceed == -2:
                    return creation_failed_exception("Name is very large.")
                elif should_proceed == -3:
                    return creation_failed_exception("Name have special_characters.")

        if 'input_file' in data:
            # data['input_file'] = request.FILES.get('input_file')
            files = request.FILES.getlist('input_file')
            for file in files:
                data['input_file'] = file
                data['datasource_type'] = 'fileUpload'
                if data['input_file'] is None:
                    data['name'] = data.get('name',
                                            data.get('datasource_type', "H") + "_" + str(random.randint(1000000, 10000000)))
                else:
                    data['name'] = data['input_file'].name[:-4].replace('.', '_')

                datasetname_list = []
                dataset_query = Dataset.objects.filter(deleted=False, created_by_id=request.user.id)
                for index, i in enumerate(dataset_query):
                    datasetname_list.append(i.name)
                if data['name'] in datasetname_list:
                    return creation_failed_exception("Dataset file name already exists!.")

                serializer = DatasetSerializer(data=data, context={"request": self.request})
                if serializer.is_valid():
                    dataset_object = serializer.save()
                    dataset_object.create()
                    response.append(serializer.data)
                else:
                    return creation_failed_exception(serializer.errors)
            return Response(response)

        elif 'datasource_details' in data:
            data['input_file'] = None
            if "datasetname" in data['datasource_details']:
                datasource_details = json.loads(data['datasource_details'])
                data['name'] = datasource_details['datasetname']
            else:
                data['name'] = data.get('name',
                                        data.get('datasource_type', "H") + "_" + str(random.randint(1000000, 10000000)))

        # question: why to use user.id when it can take, id, pk, object.
        # answer: I tried. Sighhh but it gave this error "Incorrect type. Expected pk value, received User."

        serializer = DatasetSerializer(data=data, context={"request": self.request})
        if serializer.is_valid():
            dataset_object = serializer.save()
            dataset_object.create()
            return Response(serializer.data)
        return creation_failed_exception(serializer.errors)
        # except Exception as err:
        #     return creation_failed_exception(err)

    def update(self, request, *args, **kwargs):
        data = request.data
        data = convert_to_string(data)

        if 'name' in data and not name_check(data['name']):
            return creation_failed_exception(
                "Name not correct. Only digits, letter, undescore and hypen allowed. No empty. Less then 100 characters.")

        if 'name' in data:
            datasetname_list = []
            dataset_query = Dataset.objects.filter(deleted=False, created_by_id=request.user.id)
            for index, i in enumerate(dataset_query):
                datasetname_list.append(i.name)
            if data['name'] in datasetname_list:
                return creation_failed_exception("Dataset file name already exists!.")

        try:
            instance = self.get_object_from_all()
            if 'deleted' in data:
                if data['deleted'] == True:
                    print('let us delete')
                    instance.deleted = True
                    instance.save()
                    clean_up_on_delete.delay(instance.slug, Dataset.__name__)
                    return JsonResponse({'message': 'Deleted'})
        except:
            return update_failed_exception("File Doesn't exist.")

        if 'subsetting' in data:
            if data['subsetting'] == True:
                subset_dataset_list = []
                dataset_query = Dataset.objects.filter(deleted=False, created_by_id=request.user.id)
                for index, i in enumerate(dataset_query):
                    subset_dataset_list.append(i.name)
                if data['name'] in subset_dataset_list:
                    return creation_failed_exception("Dataset file name already exists!.")
                return self.subsetting(request, instance)

        # question: do we need update method in views/ as well as in serializers?
        # answer: Yes. LoL
        serializer = self.serializer_class(instance=instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return update_failed_exception(serializer.errors)

    @detail_route(methods=['put'])
    def set_meta(self, request, slug=None):
        data = request.data
        data = convert_to_string(data)
        instance = self.get_object()
        serializer = self.serializer_class(instance=instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    @detail_route(methods=['get'])
    def get_meta(self, request, slug=None):
        user = request.user
        instance = self.get_object_from_all()
        serializer = self.serializer_class(instance=instance)
        return Response({
            'meta_data': serializer.data.get('meta_data'),
        })

    @detail_route(methods=['get'])
    def get_config(self, request, slug=None):
        instance = self.get_object()
        serializer = self.serializer_class(instance=instance)
        return Response(serializer.data.get('db_details'))

    @list_route(methods=['get'])
    def all(self, request):
        queryset = Dataset.objects.filter(
            created_by=self.request.user,
            deleted=False,
            status__in=['SUCCESS']
        )
        serializer = DataNameListSerializer(queryset, many=True, context={"request": self.request})
        return Response({
            "data": serializer.data
        })

    def list(self, request, *args, **kwargs):
        return get_listed_data(
            viewset=self,
            request=request,
            list_serializer=DataListSerializer
        )

    def retrieve(self, request, *args, **kwargs):
        # return get_retrieve_data(self)

        try:
            instance = self.get_object_from_all()
        except:
            return retrieve_failed_exception("File Doesn't exist.")

        if instance is None:
            return retrieve_failed_exception("File Doesn't exist.")

        serializer = DatasetSerializer(instance=instance, context={'request': request})
        object_details = serializer.data
        original_meta_data_from_scripts = object_details['meta_data']

        if original_meta_data_from_scripts is None:
            uiMetaData = None
        if original_meta_data_from_scripts == {}:
            uiMetaData = None
        else:
            permissions_dict = {
                'create_signal': request.user.has_perm('api.create_signal'),
                'subsetting_dataset': request.user.has_perm('api.subsetting_dataset')

            }
            uiMetaData = add_ui_metadata_to_metadata(original_meta_data_from_scripts, permissions_dict=permissions_dict)

        object_details['meta_data'] = {
            "scriptMetaData": original_meta_data_from_scripts,
            "uiMetaData": uiMetaData
        }

        if 'meta_data' in object_details:
            if "uiMetaData" in object_details['meta_data']:
                if object_details['meta_data']["uiMetaData"] is None:
                    pass
                else:
                    from config.settings import feature_engineering_settings
                    object_details['meta_data']["uiMetaData"].update({
                        "fe_config": {
                            "data_cleansing": feature_engineering_settings.data_cleansing_static,
                            "column_format": feature_engineering_settings.column_format,
                            "fe": feature_engineering_settings.feture_engineering_static
                        }
                    })

        if 'meta_data' in object_details:
            if "uiMetaData" in object_details['meta_data']:
                if object_details['meta_data']["uiMetaData"] is None:
                    pass
                else:
                    object_details['meta_data']["uiMetaData"][
                        'SKLEARN_CLASSIFICATION_EVALUATION_METRICS'] = settings.SKLEARN_CLASSIFICATION_EVALUATION_METRICS
                    object_details['meta_data']["uiMetaData"][
                        'SKLEARN_REGRESSION_EVALUATION_METRICS'] = settings.SKLEARN_REGRESSION_EVALUATION_METRICS

        return Response(object_details)

    def subsetting(self, request, instance=None):

        if instance is None:
            return creation_failed_exception("File Doesn't exist.")

        # try:
        data = request.data
        data = convert_to_string(data)

        temp_details = dict()
        if instance.datasource_type == "fileUpload":
            temp_details['input_file'] = instance.input_file
            temp_details['datasource_type'] = instance.datasource_type
            temp_details['file_remote'] = instance.file_remote
            temp_details['name'] = data.get('name', temp_details['input_file'].name)
        else:
            temp_details['input_file'] = None
            temp_details['datasource_details'] = instance.datasource_details
            temp_details['datasource_type'] = instance.datasource_type
            temp_details['name'] = data.get(
                'name',
                data.get('datasource_type', "NoName") + "_" + str(random.randint(1000000, 10000000))
            )
        temp_details['created_by'] = request.user.id

        serializer = DatasetSerializer(data=temp_details, context={"request": self.request})
        if serializer.is_valid():
            dataset_object = serializer.save()
            if 'filter_settings' in data:
                dataset_object.create_for_subsetting(
                    data['filter_settings'],
                    data.get('transformation_settings', {}),
                    instance.get_input_file(),
                    instance.get_metadata_url_config()
                )
            else:
                return creation_failed_exception({'error': 'no filter_settings'})
            return Response(serializer.data)
        # except Exception as err:
        #     return creation_failed_exception(err)
        # return creation_failed_exception(serializer.errors)

    @detail_route(methods=['get'])
    def share(self, request, *args, **kwargs):
        try:
            shared_id = request.GET['shared_id'].split(",")
            dataset_obj = Dataset.objects.get(slug=self.kwargs.get('slug'), created_by_id=request.user.id)
            dataset_name = dataset_obj.name
            shared_by=User.objects.get(id=request.user.id)
            import ast
            shared_by = ast.literal_eval(json.dumps(shared_by.username))

            if request.user.id in [int(i) for i in shared_id]:
                return sharing_failed_exception('Dataset should not be shared to itself.')
            sharedTo=list()
            for id in shared_id:
                sharedTo.append(User.objects.get(pk=id).username)
                import random,string
                if dataset_obj.shared is True:
                    dataset_details = {
                        'name': dataset_name + str(random.randint(1, 100)),
                        'input_file': dataset_obj.input_file,
                        'created_by': User.objects.get(pk=id).id,
                        'datasource_type': dataset_obj.datasource_type,
                        'datasource_details': dataset_obj.datasource_details,
                        'analysis_done': True,
                        'status': dataset_obj.status,
                        'subsetting': dataset_obj.subsetting,
                        'file_remote': dataset_obj.file_remote,
                        'shared': True,
                        'shared_by': shared_by,
                        'shared_slug': dataset_obj.shared_slug,
                        'meta_data': dataset_obj.meta_data
                    }
                    dataset_details = convert_to_string(dataset_details)
                    dataset_serializer = DatasetSerializer(data=dataset_details)
                    if dataset_serializer.is_valid():
                        shared_dataset_object = dataset_serializer.save()
                    else:
                        print(dataset_serializer.errors)
                else:
                    dataset_details = {
                        'name': dataset_name +'_shared'+ str(random.randint(1, 100)),
                        'input_file': dataset_obj.input_file,
                        'created_by': User.objects.get(pk=id).id,
                        'datasource_type': dataset_obj.datasource_type,
                        'datasource_details': dataset_obj.datasource_details,
                        'analysis_done': True,
                        'status': dataset_obj.status,
                        'subsetting': dataset_obj.subsetting,
                        'file_remote': dataset_obj.file_remote,
                        'shared': True,
                        'shared_by': shared_by,
                        'shared_slug': self.kwargs.get('slug'),
                        'meta_data': dataset_obj.meta_data
                    }
                    dataset_details = convert_to_string(dataset_details)
                    dataset_serializer = DatasetSerializer(data=dataset_details)
                    if dataset_serializer.is_valid():
                        shared_dataset_object = dataset_serializer.save()
                    else:
                        print(dataset_serializer.errors)
            return JsonResponse({'message': 'Dataset shared.','status': 'true','sharedTo':sharedTo})
        except Exception as err:
            print (err)
            return sharing_failed_exception('Dataset sharing failed.')

    @detail_route(methods=['put'])
    def meta_data_modifications(self, request, slug=None):
        data = request.data
        if 'config' not in data:
            return Response({'messgae': 'No config in request body.'})
        uiMetaData = data['uiMetaData']
        ts = data.get('config')

        uiMetaData = convert_metadata_according_to_transformation_setting(
            uiMetaData,
            transformation_setting=ts,
            user=request.user
        )

        uiMetaData["advanced_settings"] = get_advanced_setting(uiMetaData['varibaleSelectionArray'])
        return Response(uiMetaData)

    @detail_route(methods=['put'])
    def advanced_settings_modification(self, request, slug=None):
        data = request.data
        data = data.get('variableSelection')
        return Response(get_advanced_setting(data))

    @list_route(methods=['get'])
    def dummy_permission(self, request):
        queryset = Dataset.objects.filter(
            created_by=self.request.user,
            deleted=False,
            status__in=['SUCCESS']
        )
        # assign_perm('api.view_dataset', request.user)
        for insta in queryset:
            assign_perm('api.view_dataset', request.user, insta)

        return Response({})

    def createFromKylo(self, request, *args, **kwargs):
        try:
            data = kwargs.get('data')
            data = convert_to_string(data)

            if 'datasource_details' in data:
                data['input_file'] = None
                if "datasetname" in data['datasource_details']:
                    datasource_details = json.loads(data['datasource_details'])
                    data['name'] = datasource_details['datasetname']
                else:
                    data['name'] = data.get('name', data.get('datasource_type', "H") + "_" + str(
                        random.randint(1000000, 10000000)))

                # question: why to use user.id when it can take, id, pk, object.
                # answer: I tried. Sighhh but it gave this error "Incorrect type. Expected pk value, received User."
                data['created_by'] = request['user']

            serializer = DatasetSerializer(data=data, context={"request": request})
            if serializer.is_valid():
                dataset_object = serializer.save()
                dataset_object.create()
                return Response(serializer.data)
            return creation_failed_exception(serializer.errors)
        except Exception as err:
            return creation_failed_exception(err)
