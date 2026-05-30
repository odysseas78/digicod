from django.conf import settings
from django.http import SimpleCookie
from rest_framework.permissions import IsAuthenticated
from api.dyn_api.views_d import DynamicAPI
from .helpers import Utils

from config.pagination import CustomPagination



class DynA(DynamicAPI):
    def __init__(self):
        # self.pagination_class = None
        self.DYNAMIC_API = getattr(settings, "DYNAMIC_API")
        


class DynP(DynamicAPI):
    
    permission_classes = [IsAuthenticated]
            
