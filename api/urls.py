from django.db import router
from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'collaborations', CollaborationListViewSet, basename='collaboration')
router.register(r'todo', TodoViewSet, basename='todo')
router.register(r'collaborations/update', CollaborationUpdateViewSet, basename='collaboration')

urlpatterns = [
    path(r'', include(router.urls)),
    path('todo/create', TodoCreateView.as_view()),
]