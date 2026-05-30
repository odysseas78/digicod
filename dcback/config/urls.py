import os
from django.conf import settings
from pprint import pprint
from django.conf.urls.static import static
from django.urls import path, include
from eshop.views import SocialLoginView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenVerifyView,
)
from django.views.decorators.csrf import csrf_exempt
from api.views.views import ApiView
from django.urls import re_path, resolve
from config.consumers import NotificationConsumer
from loguru import logger
from api.dyn_api.views import DynamicAPI



# handler404 = 'eshop.views.view_404'

# def logfn1(name,path='logs/'):
#     logger.add(f"{path}/{name}.log", backtrace=True, diagnose=True, filter=lambda record: record["extra"].get("name") == name)
#     return logger.bind(name=name)



urlpatterns = [
    # path('', index),
    # path('api/', include('eshop_api.urls')),
    # path('api/', include('api.dyn_api.urls')),
    # path('api/', include('apps.shop.urls')),
    # path("api/graphql/", GraphQLView.as_view(graphiql=True, schema=eshop.graphql.frontend.index.schema)),
    # path("graphql", GraphQLView.as_view(graphiql=True)),
    # path('api/a/', GraphQl.as_view(graphiql=True, schema=eshop.graphql.frontend.index.schema)),
    # path('api/b/', GraphQl2.as_view(graphiql=True, schema=eshop.graphql.frontend.index_priv.schema)),
    # path('api/c/', ApiView.as_view()),
    # path('password/reset/confirm/<str:uid>/<str:token>', password_reset),
    
    # JWT auth
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # path('api/auth/', include('djoser.urls')),
    # path('api/auth/', include('djoser.urls.authtoken')),
    # path('api/auth/', include('djoser.urls.jwt')),
    # path('api/auth/social/login/', SocialLoginView.as_view(), name='token_verify')
]




# urlpatterns = []


# websocket_urlpatterns = [
#     # re_path(r"ws/updates/(?P<user_id>\w+)/$", consumers.UpdateConsumer.as_asgi()),
#     re_path(r"ws/updates/", consumers.UpdateConsumer.as_asgi()),
# ]

# websocket_urlpatterns = [
#     re_path(r"ws/notifications/$", NotificationConsumer.as_asgi()),
# ]
