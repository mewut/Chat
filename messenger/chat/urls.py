from .views import ApiUsers, ApiRooms
from rest_framework.routers import DefaultRouter
from django.urls import path, include


# https://ilyachch.gitbook.io/django-rest-framework-russian-documentation/overview/navigaciya-po-api/routers


router = DefaultRouter()
router.register('rooms', ApiRooms)
router.register('users', ApiUsers)

urlpatterns = [
    path('api/', include(router.urls)),
]
