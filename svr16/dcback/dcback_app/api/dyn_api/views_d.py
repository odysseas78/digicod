from django.conf import settings
from django.http import Http404, SimpleCookie
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from api.dyn_api.helpers import Utils
# from .pagination import DynamicPagination
from config.pagination import CustomPagination

def getCookies(request):
    cookies = SimpleCookie(request.headers.get('set-cookie'))
    polz = request.COOKIES.get('_polz') if request.COOKIES.get('_polz') else cookies.get('_polz').value if cookies.get('_polz') else None
    ccc = request.COOKIES.get('_ccc') if request.COOKIES.get('_ccc') else cookies.get('_ccc').value if cookies.get('_ccc') else None
    return {'polz':polz, 'ccc':ccc}

class DynamicAPI(APIView):
    DYNAMIC_API = getattr(settings, "DYNAMIC_API")
    pagination_class = CustomPagination

    def paginate_queryset(self, queryset, request):
        if self.pagination_class is None:
            return None, None

        paginator = self.pagination_class(request)

        page = paginator.paginate_queryset(
            queryset=queryset,
            request=request,
            view=self,
        )

        return page, paginator

    def get(self, request, **kwargs):
        model_name = kwargs.get("model_name")
        model_id = kwargs.get("id", None)
        print(getCookies(self.request))
        try:
            model_manager = Utils.get_manager(self.DYNAMIC_API, model_name)
            serializer_class = Utils.get_serializer(self.DYNAMIC_API, model_name)
            # ----------------------------------------------------
            if model_id is not None:
                try:
                    model_id = int(model_id)

                    if model_id < 0:
                        raise ValueError("Expect positive int")

                except ValueError as e:
                    return Response(
                        data={
                            "message": "Input Error = " + str(e),
                            "success": False,
                        },
                        status=400,
                    )

                thing = get_object_or_404(model_manager, id=model_id)

                serializer = serializer_class(instance=thing)

                return Response(
                    data={
                        "data": serializer.data,
                        "success": True,
                    },
                    status=200,
                )

            queryset = model_manager.all()

            reserved_params = {
                "page",
                "page_size",
                "ordering",
                "limit",
            }

            raw_params = request.query_params.dict()

            filters = {
                key: value
                for key, value in raw_params.items()
                if key not in reserved_params
            }

            if filters:
                queryset = queryset.filter(**filters)
            queryset = queryset.order_by("id")
            # QuerySet paginieren.
            page, paginator = self.paginate_queryset(queryset, request)
            # Wenn Pagination aktiv ist, nur aktuelle Seite serialisieren.
            if page is not None:
                serializer = serializer_class(instance=page, many=True)

                return paginator.get_paginated_response(serializer.data)

            # Fallback, falls pagination_class = None ist.
            serializer = serializer_class(instance=queryset, many=True)

            return Response(
                data={
                    "data": serializer.data,
                    "success": True,
                },
                status=200,
            )

        except KeyError:
            return Response(
                data={
                    "message": "Bad request.",
                    "success": False,
                },
                status=400,
            )

        except Http404:
            return Response(
                data={
                    "message": "object with given id not found.",
                    "success": False,
                },
                status=404,
            )


    def post(self, request, **kwargs):

        model_name = kwargs.get("model_name")

        try:
            serializer_class = Utils.get_serializer(self.DYNAMIC_API, model_name)
            serializer = serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()

                return Response(
                    data={
                        "message": "Record Created.",
                        "data": serializer.data,
                        "success": True,
                    },
                    status=201,
                )

            return Response(
                data={
                    "errors": serializer.errors,
                    "success": False,
                },
                status=400,
            )

        except KeyError:
            return Response(
                data={
                    "message": "Bad request.",
                    "success": False,
                },
                status=400,
            )


    def put(self, request, **kwargs):
        model_name = kwargs.get("model_name")
        model_id = kwargs.get("id", None)

        if model_id is None:
            return Response(
                data={
                    "message": "id is required for update.",
                    "success": False,
                },
                status=400,
            )

        try:
            model_manager = Utils.get_manager(self.DYNAMIC_API, model_name)
            serializer_class = Utils.get_serializer(self.DYNAMIC_API, model_name)

            thing = get_object_or_404(model_manager, id=model_id)

            serializer = serializer_class(
                instance=thing,
                data=request.data,
                partial=True,
            )

            if serializer.is_valid():
                serializer.save()

                return Response(
                    data={
                        "message": "Record Updated.",
                        "data": serializer.data,
                        "success": True,
                    },
                    status=200,
                )

            return Response(
                data={
                    "errors": serializer.errors,
                    "success": False,
                },
                status=400,
            )

        except KeyError:
            return Response(
                data={
                    "message": "Bad request.",
                    "success": False,
                },
                status=400,
            )

        except Http404:
            return Response(
                data={
                    "message": "object with given id not found.",
                    "success": False,
                },
                status=404,
            )

    def delete(self, request, **kwargs):
        model_name = kwargs.get("model_name")
        model_id = kwargs.get("id", None)

        if model_id is None:
            return Response(
                data={
                    "message": "id is required for delete.",
                    "success": False,
                },
                status=400,
            )

        try:
            model_manager = Utils.get_manager(self.DYNAMIC_API, model_name)
            thing = get_object_or_404(model_manager, id=model_id)
            thing.delete()
            return Response(
                data={
                    "message": "Record Deleted.",
                    "success": True,
                },
                status=200,
            )

        except KeyError:
            return Response(
                data={
                    "message": "this model is not activated or not exist.",
                    "success": False,
                },
                status=400,
            )

        except Http404:
            return Response(
                data={
                    "message": "object with given id not found.",
                    "success": False,
                },
                status=404,
            )
            