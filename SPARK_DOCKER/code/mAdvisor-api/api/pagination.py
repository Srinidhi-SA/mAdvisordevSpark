from __future__ import division
from past.utils import old_div
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.conf import settings
from api.utils import get_permissions

# -------------------------------------------------------------------------------
# pylint: disable=too-many-ancestors
# pylint: disable=no-member
# pylint: disable=too-many-return-statements
# pylint: disable=too-many-locals
# pylint: disable=too-many-branches
# pylint: disable=unused-argument
# pylint: disable=line-too-long
# pylint: disable=too-many-statements
# pylint: disable=arguments-differ
# -------------------------------------------------------------------------------


class CustomPagination(PageNumberPagination):

    def __init__(self):
        self.top_3 = None
        self.view = None
        self.request = None
        self.queryset = None
        self.list_serializer = None

    def get_paginated_response(self, data):
        return None

    def modified_get_paginate_response(self, page):
        # TODO: move the below exception handeling to some util function
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
                                             type='list'
                                             )

        return Response({
            'data': pagination["current_data"],
            'total_number_of_pages': pagination['count'],
            'current_page': pagination['current_page'],
            'current_page_size': pagination['current_page_size'],
            'current_item_count': len(pagination["current_data"]),
            'top_3': self.top_3,
            'permission_details': permission_details
        })

    def get_page_count(self, page, page_number=1, page_size=10):
        if page_size < 1:
            page_size = 1
        total_data_count = len(page)
        if total_data_count < 1:
            return {
                "count": 0,
                "current_page": 0,
                "current_page_size": 0,
                "current_data": []
            }
        total_number_of_pages = (old_div((total_data_count - 1), page_size)) + 1
        if page_number > total_number_of_pages:
            page_number = 1
            page_size = 10
        initial_count = (page_number - 1) * page_size
        end_count = initial_count + page_size
        page_data = page[initial_count:end_count]
        serialized_page_data = self.list_serializer(page_data, many=True, context={"request": self.request})
        return {
            "count": total_number_of_pages,
            "current_page": page_number,
            "current_page_size": page_size,
            "current_data": serialized_page_data.data
        }

    def add_top_3(self, query_set):
        top_3_query_set_serializer = self.list_serializer(query_set, many=True, context={"request": self.request})
        top_3_query_set_serializer_data = top_3_query_set_serializer.data
        self.top_3 = top_3_query_set_serializer_data

    def paginate_queryset(self,
                          queryset,
                          request,
                          view=None,
                          list_serializer=None
                          ):
        self.request = request
        self.view = view
        self.queryset = queryset
        self.list_serializer = list_serializer
        return queryset
