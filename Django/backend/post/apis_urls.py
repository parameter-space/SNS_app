from django.urls import path, include
from .apis import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', PostViewSet)

# http://127.0.0.1:8000/api/posts/ get요청이나 post요청으로 read와 create를 할 수 있다.
# http://127.0.0.1:8000/api/posts/<int:pk>/ put요청이나 delete요청으로 update와 delete를 할 수 있다. 
urlpatterns = [
    path('', include(router.urls)),
]