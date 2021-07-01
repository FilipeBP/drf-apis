from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from rest_framework import routers

from addresses.viewsets import AddressViewSet
from clients.viewsets import ClientViewSet

router = routers.DefaultRouter()
router.register(r'addresses', AddressViewSet)
router.register(r'clients', ClientViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls))
]
