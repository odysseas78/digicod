# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.urls import path
from api.dyn_api.views import DynA, DynP

urlpatterns = [
    # path('dyn/<str:model_name>/'  , DynA.as_view()),
    # path('dyn/<str:model_name>/<str:id>/' , DynA.as_view()),
    
    # path('dyn/<str:model_name>/'  , DynP.as_view()),
    # path('dyn/<str:model_name>/<str:id>/' , DynP.as_view()),
]
