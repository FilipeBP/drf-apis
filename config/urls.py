from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from rest_framework import routers
from addresses.viewsets import AddressViewSet

router = routers.DefaultRouter()
router.register(r'address', AddressViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls))
]
