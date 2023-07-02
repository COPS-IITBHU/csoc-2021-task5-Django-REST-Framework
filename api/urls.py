from django.urls import path
from .views import (TodoCreateView,TodoListView,TodoDetail,TodoAddCollabs,TodoRemoveCollabs)

"""
TODO:
Add the urlpatterns of the endpoints, required for implementing
Todo GET (List and Detail), PUT, PATCH and DELETE.
"""

urlpatterns = [
    path('todo/create/', TodoCreateView.as_view()),
    path('todo/',TodoListView.as_view()),
    path('todo/<int:id>/', TodoDetail.as_view()),
    path('todo/<int:id>/add-collaborators/',TodoAddCollabs.as_view()),
    path('todo/<int:id>/remove-collaborators/',TodoRemoveCollabs.as_view()),
]