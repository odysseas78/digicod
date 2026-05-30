# import json

# from rest_framework import generics, permissions, serializers, status
# from rest_framework.response import Response
# from rest_framework.views import APIView, Http404

# from api.dyn_api.helpers import Utils
# from config.pagination import CustomPagination

# from apps.shop.models import Cart, Product
# from apps.shop.serializers import CartSerializer, CurrencySerializer, ProductSerializer
# #     AddCartItemSerializer,
# #     BrandSerializer,
#     # CartSerializer,
# #     CatalogProductSerializer,
# #     CategorySerializer,
# #     CheckoutSerializer,
# #     CustomerOrderSerializer,

# def ggg(self, request):
#    try:
#       queryset = self.queryset
#       serializer_class = self.serializer_class
#       # serializer = ProductSerializer(queryset, context={"request": request}, many=True)
#       reserved_params = {
#             "page",
#             "page_size",
#             "ordering",
#             "limit",
#       }

#       raw_params = request.query_params.dict()

#       filters = {
#             key: value
#             for key, value in raw_params.items()
#             if key not in reserved_params
#       }

#       if filters:
#             queryset = queryset.filter(**filters)
#       queryset = queryset.order_by("id")
#       # QuerySet paginieren.
#       page, paginator = self.paginate_queryset(queryset, request)
#       # Wenn Pagination aktiv ist, nur aktuelle Seite serialisieren.
#       if page is not None:
#             serializer = serializer_class(instance=page, many=True)

#             return paginator.get_paginated_response(serializer.data)

#       # Fallback, falls pagination_class = None ist.
#       serializer = serializer_class(instance=queryset, many=True)

#       return Response(
#             data={
#                "data": serializer.data,
#                "success": True,
#             },
#             status=200,
#       )

#    except KeyError:
#       return Response(
#             data={
#                "message": "Bad request.",
#                "success": False,
#             },
#             status=400,
#       )

#    except Http404:
#       return Response(
#             data={
#                "message": "object with given id not found.",
#                "success": False,
#             },
#             status=404,
#       )

# def make_serializer(model, fields=None, exclude=None, extra_fields=None):
#     extra_fields = extra_fields or {}

#     meta_attrs = {
#         "model": model,
#     }

#     if fields is not None:
#         meta_attrs["fields"] = fields
#     elif exclude is not None:
#         meta_attrs["exclude"] = exclude
#     else:
#         meta_attrs["fields"] = "__all__"

#     Meta = type("Meta", (), meta_attrs)

#     attrs = {
#         "Meta": Meta,
#         **extra_fields,
#     }

#     return type("DynamicProductSerializer", (serializers.ModelSerializer,), attrs)

# class DefView(APIView):
#    #  queryset = Product.objects.filter(active=True, in_stock=True, qty__gt=0)
#    #  serializer_class = ProductSerializer
#    #  pagination_class = CustomPagination
    
#     def paginate_queryset(self, queryset, request):
#         if self.pagination_class is None:
#             return None, None

#         paginator = self.pagination_class(request)

#         page = paginator.paginate_queryset(
#             queryset=queryset,
#             request=request,
#             view=self,
#         )

#         return page, paginator
#     # lookup_field = "sku"
    
#     def get(self, request):
#         self.begin(request)
#         try:
#             queryset = self.queryset
#             serializer_class = self.serializer_class
#             # serializer = ProductSerializer(queryset, context={"request": request}, many=True)
#             reserved_params = {
#                 "page",
#                 "page_size",
#                 "ordering",
#                 "limit",
#             }

#             raw_params = request.query_params.dict()

#             filters = {
#                 key: value
#                 for key, value in raw_params.items()
#                 if key not in reserved_params
#             }

#             if filters:
#                 queryset = queryset.filter(**filters)
#             queryset = queryset.order_by("id")
#             # QuerySet paginieren.
#             page, paginator = self.paginate_queryset(queryset, request)
#             # Wenn Pagination aktiv ist, nur aktuelle Seite serialisieren.
#             if page is not None:
#                 serializer = serializer_class(instance=page, many=True)

#                 return paginator.get_paginated_response(serializer.data)

#             # Fallback, falls pagination_class = None ist.
#             serializer = serializer_class(instance=queryset, many=True)
#             self.end(request)
#             return Response(
#                 data={
#                     "data": serializer.data,
#                     "success": True,
#                 },
#                 status=200,
#             )
         
#         except KeyError:
#             return Response(
#                 data={
#                     "message": "Bad request.",
#                     "success": False,
#                 },
#                 status=400,
#             )

#         except Http404:
#             return Response(
#                 data={
#                     "message": "object with given id not found.",
#                     "success": False,
#                 },
#                 status=404,
#             )
            