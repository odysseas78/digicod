
import os, django, sys
# sys.path.insert(0, '/home/dcback')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from config.urls import websocket_urlpatterns
from config.middleware.middlewares import TokenAuthMiddleware
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
# from rest_framework.authentication import TokenAuthentication



from channels.security.websocket import AllowedHostsOriginValidator
from loguru import logger

# def logfn1(name,path='logs/'):
#     logger.add(f"{path}/{name}.log", backtrace=True, diagnose=True, filter=lambda record: record["extra"].get("name") == name)
#     return logger.bind(name=name)




django_asgi_app = get_asgi_application()



application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            TokenAuthMiddleware(URLRouter(websocket_urlpatterns))
        ),
    }
)
