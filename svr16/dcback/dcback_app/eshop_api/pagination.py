from collections import OrderedDict
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.response import Response


class CategoryProductsPagination(PageNumberPagination):

    page_size = 50000
    page_query_param = 'page'

class CategoryBrandsPagination(PageNumberPagination):

    page_size = 50000
    page_query_param = 'page'

class BrandProductsPagination(PageNumberPagination):

    page_size = 50000
    page_query_param = 'page'
    
class OrdersPagination(LimitOffsetPagination):

    max_limit = 15
    limit_query_param = 'take'
    offset_query_param = 'skip'
    
    # page_size_query_param = 'page_szize'
    page_size = 15
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('totalCount', self.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('data', data)
        ]))

class CustomerPagination(LimitOffsetPagination):

    max_limit = 15
    limit_query_param = 'take'
    offset_query_param = 'skip'
    
    # page_size_query_param = 'page_szize'
    page_size = 15
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('totalCount', self.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('data', data)
        ]))
        
        
        
class ProductsPagination(LimitOffsetPagination):

    max_limit = 15
    limit_query_param = 'take'
    offset_query_param = 'skip'
    
    # page_size_query_param = 'page_szize'
    page_size = 15
    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('totalCount', self.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('data', data)
        ]))
        
        
