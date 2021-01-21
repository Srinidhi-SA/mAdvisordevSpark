"""
OCR Pagination
"""
from past.utils import old_div
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.conf import settings
from ocr.permission import get_permissions

# -------------------------------------------------------------------------------
# pylint: disable=too-many-ancestors
# pylint: disable=no-member
# pylint: disable=too-many-return-statements
# pylint: disable=too-many-locals
# pylint: disable=arguments-differ
# pylint: disable=unused-argument
# pylint: disable=line-too-long
# pylint: disable=too-many-statements
# -------------------------------------------------------------------------------


class CustomOCRPagination(PageNumberPagination):
    """
    OCR Pagination
    """
    def __init__(self):
        self.query_set = None
        self.request = None
        self.view = None
        self.list_serializer = None

    def modified_get_paginate_response(self, page):
        """
        Desc:
        """
        try:
            page_number = int(self.request.query_params.get('page_number', settings.PAGENUMBER))
        except ValueError:
            page_number = settings.PAGENUMBER
        try:
            page_size = int(self.request.query_params.get('page_size', settings.PAGESIZE))
        except ValueError:
            page_size = settings.PAGESIZE
        pagination = self.get_page_count(page, page_number, page_size)
        permission_details = get_permissions(user=self.request.user,
                                             model=self.list_serializer.Meta.model.__name__.lower(),
                                             type='list')

        return Response({
            'data': pagination["current_data"],
            'total_number_of_pages': pagination['count'],
            'current_page': pagination['current_page'],
            'current_page_size': pagination['current_page_size'],
            'current_item_count': len(pagination["current_data"]),
            'total_data_count': pagination['total_data_count'],
            'permission_details': permission_details
        })

    def get_page_count(self, page, page_number=1, page_size=10):
        """
        Desc:
        """
        if page_size < 1:
            page_size = 1
        total_data_count = len(page)
        if total_data_count < 1:
            return {
                "count": 0,
                "current_page": 0,
                "current_page_size": 0,
                "total_data_count": total_data_count,
                "current_data": []
            }
        total_number_of_pages = (old_div((total_data_count - 1), page_size)) + 1
        if page_number > total_number_of_pages:
            page_number = 1
            page_size = 10
        initial_count = (page_number - 1) * page_size
        end_count = initial_count + page_size
        page_data = page[initial_count:end_count]
        serialized_page_data = self.list_serializer(page_data, many=True,
                                                    context={"request": self.request})

        data = [i for i in serialized_page_data.data if i]
        total_data_count = len(data)
        # pylint: disable= line-too-long
        return {
            "count": total_number_of_pages,
            "current_page": page_number,
            "current_page_size": page_size,
            "current_data": data,
            "total_data_count": total_data_count
        }

    def paginate_queryset(self, queryset, request, view=None, list_serializer=None):
        """
        Desc:
        """
        self.request = request
        self.view = view
        self.query_set = queryset
        self.list_serializer = list_serializer
        return self.query_set
