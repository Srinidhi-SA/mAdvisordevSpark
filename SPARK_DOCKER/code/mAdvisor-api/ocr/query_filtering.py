"""
Commomly used queries implementations for increased re-usability.
"""
# from itertools import chain
# from builtins import object
import ast

from django.contrib.auth.models import User
from rest_framework.response import Response


# from api.exceptions import creation_failed_exception, update_failed_exception
# from django.db.models import Q

# -------------------------------------------------------------------------------
# pylint: disable=too-many-ancestors
# pylint: disable=no-member
# pylint: disable=too-many-return-statements
# pylint: disable=too-many-locals
# pylint: disable=too-many-branches
# pylint: disable=unused-argument
# pylint: disable=line-too-long
# pylint: disable=too-few-public-methods
# pylint: disable=literal-comparison
# -------------------------------------------------------------------------------


class QueryCommonFiltering:
    """
    Performs commonly used query filtering.
    """
    query_set = None
    request = None
    sorted_by = None
    ordering = ""
    filter_fields = None
    name = None
    status = None
    confidence = None
    first_name = None
    fields = None
    time = None
    assignee = None
    reviewStatus = None
    template = None
    accuracy = None
    field_count = None
    project = None

    def __init__(self, query_set=None, request=None):
        self.query_set = query_set
        self.request = request
        # self.top_3 = query_set

        if 'name' in request.query_params:
            temp_name = self.request.query_params.get('name')
            if temp_name is None or temp_name is "":
                self.name = self.name
            else:
                self.name = temp_name

        if 'first_name' in request.query_params:
            temp_name = self.request.query_params.get('first_name')
            if temp_name is None or temp_name is "":
                self.first_name = self.first_name
            else:
                self.first_name = temp_name

        if 'status' in request.query_params:
            temp_name = self.request.query_params.get('status')
            if temp_name is None or temp_name is "":
                self.status = self.status
            else:
                self.status = temp_name

        if 'reviewStatus' in request.query_params:
            temp_name = self.request.query_params.get('reviewStatus')
            if temp_name is None or temp_name is "":
                self.reviewStatus = self.reviewStatus
            else:
                self.reviewStatus = temp_name

        if 'confidence' in request.query_params:
            temp_name = self.request.query_params.get('confidence')
            if temp_name is None or temp_name is "":
                self.confidence = self.confidence
            else:
                self.confidence = temp_name

        if 'sorted_by' in self.request.query_params:
            temp_name = self.request.query_params.get('sorted_by')
            if temp_name is None or temp_name is "":
                self.sorted_by = self.sorted_by
            else:
                if temp_name in ['name', 'created_at', 'updated_at']:
                    self.sorted_by = temp_name

        if 'ordering' in self.request.query_params:
            temp_name = self.request.query_params.get('ordering')
            if temp_name is None or temp_name is "":
                self.ordering = self.ordering
            else:
                if temp_name in ["-"]:
                    self.ordering = temp_name

        if 'filter_fields' in request.query_params:
            temp_app_filter = self.request.query_params.get('filter_fields')
            if temp_app_filter is None or temp_app_filter is "" or temp_app_filter is []:
                self.filter_fields = self.filter_fields
            else:
                self.filter_fields = temp_app_filter

        if 'fields' in request.query_params:
            temp_name = self.request.query_params.get('fields')
            if temp_name is None or temp_name is "":
                self.fields = self.fields
            else:
                self.fields = temp_name

        if 'time/word' in request.query_params:
            temp_name = self.request.query_params.get('time/word')
            if temp_name is None or temp_name is "":
                self.time = self.time
            else:
                self.time = temp_name

        if 'assignee' in request.query_params:
            temp_name = self.request.query_params.get('assignee')
            if temp_name is None or temp_name is "":
                self.assignee = self.assignee
            else:
                self.assignee = temp_name

        if 'template' in request.query_params:
            temp_name = self.request.query_params.get('template')
            if temp_name is None or temp_name is "":
                self.template = self.template
            else:
                self.template = temp_name

        if 'accuracy' in request.query_params:
            temp_name = self.request.query_params.get('accuracy')
            if temp_name is None or temp_name is "":
                self.accuracy = self.accuracy
            else:
                self.accuracy = temp_name

        if 'field_count' in request.query_params:
            temp_name = self.request.query_params.get('field_count')
            if temp_name is None or temp_name is "":
                self.field_count = self.field_count
            else:
                self.field_count = temp_name

        if 'project' in request.query_params:
            temp_name = self.request.query_params.get('project')
            if temp_name is None or temp_name is "":
                self.project = self.project
            else:
                self.project = temp_name

    def execute_common_filtering_and_sorting_and_ordering(self):
        """
        Method that handles filtering, sorting and ordering.
        """
        if self.first_name is not None:
            self.query_set = self.query_set.filter(first_name__icontains=self.first_name)
        if self.name is not None:
            self.query_set = self.query_set.filter(name__icontains=self.name)
        if self.confidence is not None:
            operator, value = self.confidence[:3], self.confidence[3:]
            if operator == 'GTE':
                self.query_set = self.query_set.filter(confidence__gte=float(value))
            if operator == 'LTE':
                self.query_set = self.query_set.filter(confidence__lte=float(value))
            if operator == 'EQL':
                self.query_set = self.query_set.filter(confidence=float(value))
        if self.status is not None:
            status_mapping_dict = {'R': 'ready_to_recognize', 'A': 'ready_to_assign', 'V1': 'ready_to_verify(L1)',
                                   'C1': 'l1_verified', 'V2': 'ready_to_verify(L2)', 'E': 'ready_to_export'}
            print(status_mapping_dict[self.status])
            self.query_set = self.query_set.filter(status=status_mapping_dict[self.status])
        if self.reviewStatus is not None:
            status_mapping_dict = {'created': ['created'], 'pendingL1': ['submitted_for_review(L1)'],
                                   'pendingL2': ['submitted_for_review(L2)'], 'reviewedL1': ['reviewerL1_reviewed'],
                                   'reviewedL2': ['reviewerL2_reviewed'],
                                   'rejected': ['reviewerL2_rejected', 'reviewerL1_rejected']}
            self.query_set = self.query_set.filter(status__in=status_mapping_dict[self.reviewStatus])
        if self.fields is not None:
            operator, value = self.fields[:3], self.fields[3:]
            if operator == 'GTE':
                self.query_set = self.query_set.filter(fields__gte=float(value))
            if operator == 'LTE':
                self.query_set = self.query_set.filter(fields__lte=float(value))
            if operator == 'EQL':
                self.query_set = self.query_set.filter(fields=float(value))
        if self.assignee is not None:
            self.query_set = self.query_set.filter(assignee=User.objects.get(username=self.assignee))
        if self.time is not None:
            self.query_set = self.query_set.filter(time_taken=float(self.time))
        if self.template is not None:
            try:
                self.query_set = self.query_set.filter(classification=self.template)
            except:
                self.query_set = self.query_set.filter(ocr_image__classification=self.template)
        if self.filter_fields is not None:
            self.filter_fields = self.filter_fields.replace(',', '\",\"').replace('[', '[\"').replace(']', '\"]')
            self.filter_fields = ast.literal_eval(self.filter_fields)
            final_query_set = self.query_set.none()

            for tag in self.filter_fields:
                query_set_temp = self.query_set.filter(tags__icontains=tag).distinct()
                final_query_set = (final_query_set | query_set_temp).distinct()
            self.query_set = final_query_set
        if self.sorted_by is not None:
            query_args = "{0}{1}".format(self.ordering, self.sorted_by)
            self.query_set = self.query_set.order_by(query_args)

        if self.accuracy is not None:
            operator, value = self.accuracy[:3], self.accuracy[3:]
            if operator == 'GTE':
                self.query_set = self.query_set.filter(ocrimage__confidence__gte=float(value))
            if operator == 'LTE':
                self.query_set = self.query_set.filter(ocrimage__confidence__lte=float(value))
            if operator == 'EQL':
                self.query_set = self.query_set.filter(ocrimage__confidence=int(value))

        if self.field_count is not None:
            operator, value = self.field_count[:3], self.field_count[3:]
            if operator == 'GTE':
                self.query_set = self.query_set.filter(ocr_image__fields__gte=int(value))
            if operator == 'LTE':
                self.query_set = self.query_set.filter(ocr_image__fields__lte=int(value))
            if operator == 'EQL':
                self.query_set = self.query_set.filter(ocr_image__fields=int(value))

        if self.project is not None:
            self.query_set = self.query_set.filter(ocr_image__project__name__icontains=self.project)

        return self.query_set


def get_listed_data(
        viewset=None,
        request=None,
        list_serializer=None,
):
    """

    :param viewset: use to  get_queryset() / pagination_class
    :param request: use to query_params
    :param list_serializer: pass Listing Serializer
    :return:
    """
    query_set = viewset.get_queryset()

    # common filtering
    qcf = QueryCommonFiltering(
        query_set=query_set,
        request=request
    )

    query_set = qcf.execute_common_filtering_and_sorting_and_ordering()

    if 'page' in request.query_params:
        if request.query_params.get('page').lower() == 'all':
            serializer = list_serializer(query_set, context={'request': request}, many=True)
            return Response({
                "data": serializer.data,
                "total_number_of_pages": 1,
                "current_page": 1
            })
    page_class = viewset.pagination_class()
    page = page_class.paginate_queryset(
        queryset=query_set,
        request=request,
        list_serializer=list_serializer,
        view=viewset
    )

    resp = page_class.modified_get_paginate_response(page)
    return resp


def get_userlisted_data(
        viewset=None,
        request=None,
        list_serializer=None,
        role=None
):
    """

    :param viewset: use to  get_queryset() / pagination_class
    :param request: use to query_params
    :param list_serializer: pass Listing Serializer
    :return:
    """
    query_set = viewset.get_queryset(request, role)

    # common filtering
    qcf = QueryCommonFiltering(
        query_set=query_set,
        request=request
    )

    query_set = qcf.execute_common_filtering_and_sorting_and_ordering()

    if 'page' in request.query_params:
        if request.query_params.get('page').lower() == 'all':
            serializer = list_serializer(query_set, many=True)
            return Response({
                "data": serializer.data,
                "total_number_of_pages": 1,
                "current_page": 1
            })
    page_class = viewset.pagination_class()
    page = page_class.paginate_queryset(
        queryset=query_set,
        request=request,
        list_serializer=list_serializer,
        view=viewset
    )

    resp = page_class.modified_get_paginate_response(page)
    return resp


def get_image_list_data(viewset, queryset, request, serializer):
    """
    Method that returns paginated response pertaining to images GET call.
    """
    qcf = QueryCommonFiltering(
        query_set=queryset,
        request=request
    )
    query_set = qcf.execute_common_filtering_and_sorting_and_ordering()

    if 'page' in request.query_params:
        if request.query_params.get('page').lower() == 'all':
            serializer = serializer(query_set, many=True)
            return Response({
                "data": serializer.data,
                "total_number_of_pages": 1,
                "current_page": 1
            })
    page_class = viewset.pagination_class()
    page = page_class.paginate_queryset(
        queryset=query_set,
        request=request,
        list_serializer=serializer,
        view=viewset
    )

    resp = page_class.modified_get_paginate_response(page)
    return resp


def get_specific_listed_data(
        viewset=None,
        request=None,
        list_serializer=None,
        role=None,
        user_type=None
):
    """

    :param viewset: use to  get_queryset() / pagination_class
    :param request: use to query_params
    :param list_serializer: pass Listing Serializer
    :return:
    """
    query_set = viewset.get_specific_reviewer_qyeryset(request, role, user_type)

    # common filtering
    qcf = QueryCommonFiltering(
        query_set=query_set,
        request=request
    )

    query_set = qcf.execute_common_filtering_and_sorting_and_ordering()

    if 'page' in request.query_params:
        if request.query_params.get('page').lower() == 'all':
            serializer = list_serializer(query_set, many=True)
            return Response({
                "data": serializer.data,
                "total_number_of_pages": 1,
                "current_page": 1
            })
    page_class = viewset.pagination_class()
    page = page_class.paginate_queryset(
        queryset=query_set,
        request=request,
        list_serializer=list_serializer,
        view=viewset
    )

    resp = page_class.modified_get_paginate_response(page)
    return resp


def get_reviewer_data(
        viewset=None,
        request=None,
        list_serializer=None,
):
    """

    :param viewset: use to  get_queryset() / pagination_class
    :param request: use to query_params
    :param list_serializer: pass Listing Serializer
    :return:
    """
    query_set = viewset.get_specific_reviewer_detail_queryset(request)

    # common filtering
    qcf = QueryCommonFiltering(
        query_set=query_set,
        request=request
    )

    query_set = qcf.execute_common_filtering_and_sorting_and_ordering()

    if 'page' in request.query_params:
        if request.query_params.get('page').lower() == 'all':
            serializer = list_serializer(query_set, many=True)
            return Response({
                "data": serializer.data,
                "total_number_of_pages": 1,
                "current_page": 1
            })
    page_class = viewset.pagination_class()
    page = page_class.paginate_queryset(
        queryset=query_set,
        request=request,
        list_serializer=list_serializer,
        view=viewset
    )

    resp = page_class.modified_get_paginate_response(page)
    return resp


def get_specific_assigned_requests(
        viewset=None,
        request=None,
        list_serializer=None,
        username=None
):
    """

    :param viewset: use to  get_queryset() / pagination_class
    :param request: use to query_params
    :param list_serializer: pass Listing Serializer
    :return:
    """
    query_set = viewset.get_specific_assigned_queryset(username)

    # common filtering
    qcf = QueryCommonFiltering(
        query_set=query_set,
        request=request
    )

    query_set = qcf.execute_common_filtering_and_sorting_and_ordering()

    if 'page' in request.query_params:
        if request.query_params.get('page').lower() == 'all':
            serializer = list_serializer(query_set, many=True)
            return Response({
                "data": serializer.data,
                "total_number_of_pages": 1,
                "current_page": 1
            })
    page_class = viewset.pagination_class()
    page = page_class.paginate_queryset(
        queryset=query_set,
        request=request,
        list_serializer=list_serializer,
        view=viewset
    )

    resp = page_class.modified_get_paginate_response(page)
    return resp


def get_filtered_ocrimage_list(
        viewset=None,
        request=None,
        list_serializer=None,
        imageStatus=None,
        projectslug=None
):
    """

    :param viewset: use to  get_queryset() / pagination_class
    :param request: use to query_params
    :param list_serializer: pass Listing Serializer
    :return:
    """
    query_set = viewset.get_queryset_by_status(projectslug, imageStatus)

    # common filtering
    qcf = QueryCommonFiltering(
        query_set=query_set,
        request=request
    )

    query_set = qcf.execute_common_filtering_and_sorting_and_ordering()
    if 'page' in request.query_params:
        if request.query_params.get('page').lower() == 'all':
            serializer = list_serializer(query_set, many=True)
            return Response({
                "data": serializer.data,
                "total_number_of_pages": 1,
                "current_page": 1
            })
    page_class = viewset.pagination_class()
    page = page_class.paginate_queryset(
        queryset=query_set,
        request=request,
        list_serializer=list_serializer,
        view=viewset
    )

    resp = page_class.modified_get_paginate_response(page)
    return resp


def get_image_data(
        viewset=None,
        request=None,
        queryset=None,
        list_serializer=None,
):
    """

    :param viewset: use to  get_queryset() / pagination_class
    :param request: use to query_params
    :param list_serializer: pass Listing Serializer
    :return:
    """
    query_set = queryset

    # common filtering
    qcf = QueryCommonFiltering(
        query_set=query_set,
        request=request
    )

    query_set = qcf.execute_common_filtering_and_sorting_and_ordering()

    if 'page' in request.query_params:
        if request.query_params.get('page').lower() == 'all':
            serializer = list_serializer(query_set, many=True)
            return Response({
                "data": serializer.data,
                "total_number_of_pages": 1,
                "current_page": 1
            })
    page_class = viewset.pagination_class()
    page = page_class.paginate_queryset(
        queryset=query_set,
        request=request,
        list_serializer=list_serializer,
        view=viewset
    )

    resp = page_class.modified_get_paginate_response(page)
    return resp


def get_filtered_project_list(
        viewset=None,
        request=None,
        list_serializer=None,
        imageStatus=None,
        projectslug=None
):
    """

    :param viewset: use to  get_queryset() / pagination_class
    :param request: use to query_params
    :param list_serializer: pass Listing Serializer
    :return:
    """
    query_set = viewset.get_reviewer_queryset(user=request.user)

    # common filtering
    qcf = QueryCommonFiltering(
        query_set=query_set,
        request=request
    )

    query_set = qcf.execute_common_filtering_and_sorting_and_ordering()
    if 'page' in request.query_params:
        if request.query_params.get('page').lower() == 'all':
            serializer = list_serializer(query_set, context={'request': request}, many=True)
            return Response({
                "data": serializer.data,
                "total_number_of_pages": 1,
                "current_page": 1
            })
    page_class = viewset.pagination_class()
    page = page_class.paginate_queryset(
        queryset=query_set,
        request=request,
        list_serializer=list_serializer,
        view=viewset
    )

    resp = page_class.modified_get_paginate_response(page)
    return resp
