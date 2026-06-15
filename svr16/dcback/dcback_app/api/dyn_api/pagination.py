# dyn_api/pagination.py

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class DynamicPagination(PageNumberPagination):
    """
    Pagination-Klasse für die dynamische API.

    Beispiele:

        /api/product/?page=1
        /api/product/?page=2
        /api/product/?page=1&page_size=20

    page_size:
        Standardanzahl pro Seite.

    page_size_query_param:
        Erlaubt dem Client, die Seitengröße selbst zu setzen.

    max_page_size:
        Maximale erlaubte Seitengröße.
    """

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        """
        Eigene Response-Struktur.

        Standard DRF wäre:
            count, next, previous, results

        Hier machen wir es passend zu deinem Stil:
            data, pagination, success
        """

        return Response(
            {
                "data": data,
                "pagination": {
                    "count": self.page.paginator.count,
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                    "current_page": self.page.number,
                    "total_pages": self.page.paginator.num_pages,
                    "page_size": self.get_page_size(self.request),
                },
                "success": True,
            },
            status=200,
        )