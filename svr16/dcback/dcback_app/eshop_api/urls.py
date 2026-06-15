from eshop_api.main.router import main_router, extra_urlpatterns
from eshop_api.adminka.urls import admin_router

urlpatterns = []
urlpatterns += main_router.urls
urlpatterns += admin_router.urls
urlpatterns.extend(extra_urlpatterns)
