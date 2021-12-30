
from rest_framework import pagination
from rest_framework.response import Response
from rest_framework import status


class CustomPagination(pagination.PageNumberPagination):

    page_size = 1

    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'links': {'next': self.get_next_link(),
                      'previous': self.get_previous_link()},
            'count': self.page.paginator.count,

            'result': data
        }, status=status.HTTP_200_OK
        )
