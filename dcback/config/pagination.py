from loguru import logger
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

logger.add("logs/paginator.log", backtrace=True, diagnose=True, filter=lambda record: record["extra"].get("name") == "paginator")
paginator = logger.bind(name="paginator")


DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 10

class CustomPagination(PageNumberPagination):
    page_size = DEFAULT_PAGE_SIZE
    page_size_query_param = 'page_size'

    def __init__(self, request):
        self.request = request
   
    def get_paginated_response(self, data):
        current_page = int(self.request.GET.get('page', DEFAULT_PAGE))
        current_page_size = int(self.request.GET.get('page_size', self.page_size))
        queryset = self.page.paginator.object_list
        model_name = queryset.model._meta.model_name

        response = Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'total': self.page.paginator.count,
            'page': current_page,
            'page_size': current_page_size,
            'results': data
        })
        if model_name == 'wallet':
            balance = queryset.first().balance
            response.data['Balance']=[float(balance), int(balance *13)]
        return response

