import json

from rest_framework import generics, permissions, serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView, Http404
from rest_framework.viewsets import ModelViewSet
from api.dyn_api.helpers import Utils
from config.pagination import CustomPagination

from .models import Brand, Cart, CartProduct, Category, Currency, Payment, Product
from .serializers import CartSerializer, CurrencySerializer, PaymentSerializer, ProductSerializer, BrandSerializer, CategorySerializer
#     AddCartItemSerializer,
#     BrandSerializer,
    # CartSerializer,
#     CatalogProductSerializer,
#     CategorySerializer,
#     CheckoutSerializer,
#     CustomerOrderSerializer,
# )
from .services import PrepaidForgeError, get_or_create_cart
# from .tasks import process_order_task, sync_products_task


# class CategoryListView(generics.ListAPIView):
#     queryset = Category.objects.filter(parent__isnull=True)
#     serializer_class = CategorySerializer


# class BrandListView(generics.ListAPIView):
#     queryset = Brand.objects.all()
#     serializer_class = BrandSerializer


# class ProductListView(generics.ListAPIView):
#     serializer_class = CatalogProductSerializer

#     def get_queryset(self):
#         queryset = PartnerProduct.objects.select_related("partner", "product__brand", "product__category").filter(
#             is_active=True,
#             partner__is_active=True,
#             product__is_active=True,
#         )
#         category_slug = self.request.query_params.get("category")
#         brand_slug = self.request.query_params.get("brand")
#         partner_code = self.request.query_params.get("partner")
#         if category_slug:
#             queryset = queryset.filter(product__category__slug=category_slug)
#         if brand_slug:
#             queryset = queryset.filter(product__brand__slug=brand_slug)
#         if partner_code:
#             queryset = queryset.filter(partner__code=partner_code)
#         return queryset
from rest_framework import serializers






class ProductView(APIView):
    queryset = Product.objects.filter(active=True, in_stock=True, qty__gt=0)
    serializer_class = ProductSerializer
    # pagination_class = CustomPagination
    
    def paginate_queryset(self, queryset, request):
        if not hasattr(self, "pagination_class") or self.pagination_class is None:
            return None, None

        paginator = self.pagination_class(request)

        page = paginator.paginate_queryset(
            queryset=queryset,
            request=request,
            view=self,
        )

        return page, paginator
    # lookup_field = "sku"
    
    def get(self, request):
        
        try:
            queryset = self.queryset
            serializer_class = self.serializer_class
            # serializer = ProductSerializer(queryset, context={"request": request}, many=True)
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
            queryset = queryset.order_by("price")
            # QuerySet paginieren.
            page, paginator = self.paginate_queryset(queryset, request)
            # Wenn Pagination aktiv ist, nur aktuelle Seite serialisieren.
            if page is not None:
                serializer = serializer_class(instance=page, many=True)

                return paginator.get_paginated_response(serializer.data)

            # Fallback, falls pagination_class = None ist.
            serializer = serializer_class(instance=queryset, context={"request": request}, many=True)

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
    
    
    
class BrandView(APIView):
    queryset = Brand.objects.filter(active=True, in_stock=True)
    serializer_class = BrandSerializer
    # pagination_class = CustomPagination
    
    def paginate_queryset(self, queryset, request):
        if not hasattr(self, "pagination_class") or self.pagination_class is None:
            return None, None

        paginator = self.pagination_class(request)

        page = paginator.paginate_queryset(
            queryset=queryset,
            request=request,
            view=self,
        )

        return page, paginator
    # lookup_field = "sku"
    
    def get(self, request):
        
        try:
            queryset = self.queryset
            serializer_class = self.serializer_class
            # serializer = ProductSerializer(queryset, context={"request": request}, many=True)
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
            serializer = serializer_class(instance=queryset, context={"request": request}, many=True)

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
    

# class CartViewSet(ModelViewSet):
#     serializer_class = CartSerializer
#     queryset = Cart.objects.all()
    
#     def get_cart_object(self):
#         return get_or_create_cart(self.request)
    
    
#     def list(self, request, *args, **kwargs):
#         """
#         GET /api/cart/
#         Gibt aktuellen Warenkorb zurück.
#         """
#         cart = self.get_cart_object()
#         serializer = self.get_serializer(cart)
#         return Response(serializer.data)
    
#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         context["request"] = self.request
#         return context
    

class CartViewSet(ModelViewSet):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()

    def get_serializer_context(self):
        """
        Wird automatisch bei self.get_serializer(...) benutzt.
        Dadurch bekommt der Serializer immer request im context.
        """
        context = super().get_serializer_context()
        context["request"] = self.request
        return context
    def get_cart_object(self):
        """
        Aktuellen Cart aus Cookie/User/Session holen oder erstellen.
        """
        return get_or_create_cart(self.request)

    def list(self, request, *args, **kwargs):
        """
        GET /api/cart/
        Gibt aktuellen Warenkorb zurück.
        """
        cart = self.get_cart_object()
        serializer = self.get_serializer(cart)
        return Response({"cart":serializer.data})

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        cart = self.get_cart_object()
        product_id = request.data.get("product_id")
        product = Product.objects.filter(id=product_id).first()
        day = request.data.get("action")
        print(product_id)
        match day:
            case "add":
                    qty = int(request.data.get("qty"))
                    item = CartProduct.objects.filter(cart=cart, product=product).first()
                    if not item and qty > 0:
                        item = CartProduct(cart=cart, product=product, qty=qty, title=product.title, item_price=product.price)
                        item.save()
                        cart.save()
                        cart.products.add(item)
                        item.save()
                        cart.save()
                    elif item:
                        item.qty = qty
                        item.save()
                        cart.save()
                        if item.qty == 0:
                            item.delete()
                            cart.save()
            case "remove":
                cpqs = CartProduct.objects.filter(cart=cart, product=product)
                cpqs.delete()
                cart.save()
            case "purge":
                cpqs = CartProduct.objects.filter(cart=cart)
                cpqs.delete()
                cart.save()
            case "currency":
                currency_id = serializer.validated_data.get("currency_id")
                cart.currency = currency_id
                cart.save()
            case "payment":
                payment_id = serializer.validated_data.get("payment_id")
                cart.payment_method = payment_id
                cart.save()
            case _:
                return Response(
                    {"detail": "Invalid cart action."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        response_serializer = self.get_serializer(cart)
        return Response(
            {"cart":response_serializer.data},
            status=status.HTTP_200_OK,
        )
        
        
# def post(self, request):
#         actions = ["add", "remove", "purge", "currency", "payment"]
#         serializer = CartSerializer(data=request.data, context={"request": request})
#         serializer.is_valid(raise_exception=True)
#         cart = get_or_create_cart(request)
#         p_id = serializer.validated_data.get("id")
#         product = Product.objects.filter(id=p_id)
       
#         day =  serializer.validated_data.get("action")
#         match day:
#             case "add":
#                     qty = serializer.validated_data.get("qty")
#                     item, created = CartProduct.objects.get_or_create(cart=cart, product=product, defaults={"qty": qty})
#                     if created:
#                         cart.products.add(product)
#                         cart.save()
#                     else:
#                         item.qty = qty
#                         if item.qty == 0:
#                             item.delete()
#                         cart.save()
#             case "remove":
#                 cpqs = CartProduct.objects.filter(cart=cart, product=product)
#                 cpqs.delete()
#                 cart.save()
#             case "purge":
#                 cpqs = CartProduct.objects.filter(cart=cart)
#                 cpqs.delete()
#                 cart.save()
#             case "currency":
#                 currency_id = serializer.validated_data.get("currency_id")
#                 cart.currency = currency_id
#                 cart.save()
#             case "payment":
#                 payment_id = serializer.validated_data.get("payment_id")
#                 cart.payment_method = payment_id
#                 cart.save()
#                             # if existing_currencies and partner_product.currency not in existing_currencies:
#         #     return Response({"detail": "Mixed currencies in one cart are not supported."}, status=status.HTTP_400_BAD_REQUEST)
#         return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)


class CategoryView(APIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    def get(self, request):
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset, context={"request": request}, many=True)
        
        return Response(serializer.data)
    
class CurrencyView(APIView):
    serializer_class = CurrencySerializer
    
    def get(self, request):
        queryset = Currency.objects.filter(active=True)
        serializer = self.serializer_class(queryset, context={"request": request}, many=True)
        
        return Response(serializer.data)
    
class PaymentView(APIView):
    serializer_class = PaymentSerializer
    
    def get(self, request):
        queryset = Payment.objects.filter(enabled=True)
        serializer = self.serializer_class(queryset, context={"request": request}, many=True)
        
        return Response(serializer.data)

# class CartItemAddView(APIView):
#     def post(self, request):
#         serializer = AddCartItemSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         cart = get_or_create_cart(request)
#         partner_product = serializer.validated_data["partner_product_id"]
#         quantity = serializer.validated_data["quantity"]

#         existing_currencies = {item.partner_product.currency for item in cart.items.select_related("partner_product")}
#         if existing_currencies and partner_product.currency not in existing_currencies:
#             return Response({"detail": "Mixed currencies in one cart are not supported."}, status=status.HTTP_400_BAD_REQUEST)

#         item, created = cart.items.get_or_create(partner_product=partner_product, defaults={"quantity": quantity})
#         if not created:
#             item.quantity += quantity
#             item.save(update_fields=["quantity", "updated_at"])
#         return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)


# class CartDeleteView(APIView):
#     def delete(self, request, pk):
#         cart = get_or_create_cart(request)
#         cart.items.filter(pk=pk).delete()
#         return Response(CartSerializer(cart).data)


# class CheckoutView(APIView):
#     def post(self, request):
#         serializer = CheckoutSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         cart = get_or_create_cart(request)
#         try:
#             order = create_order_from_cart(cart, serializer.validated_data, request_user=request.user)
#         except PrepaidForgeError as exc:
#             return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

#         guest_orders = request.session.get("guest_order_numbers", [])
#         if order.number not in guest_orders:
#             guest_orders.append(order.number)
#             request.session["guest_order_numbers"] = guest_orders[-10:]

#         process_order_task.delay(order.id)
#         return Response(CustomerOrderSerializer(order).data, status=status.HTTP_201_CREATED)


# class OrderDetailView(generics.RetrieveAPIView):
#     serializer_class = CustomerOrderSerializer
#     lookup_field = "number"

#     def get_queryset(self):
#         queryset = CustomerOrder.objects.select_related("customer__user").prefetch_related("items__codes")
#         if self.request.user.is_authenticated:
#             return queryset.filter(customer__user=self.request.user)
#         guest_orders = self.request.session.get("guest_order_numbers", [])
#         return queryset.filter(number__in=guest_orders)


# class AdminSyncProductsView(APIView):
#     permission_classes = [permissions.IsAdminUser]

#     def post(self, request):
#         sync_products_task.delay()
#         return Response({"detail": "Product sync started."}, status=status.HTTP_202_ACCEPTED)
