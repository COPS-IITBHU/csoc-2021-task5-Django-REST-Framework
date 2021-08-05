from django.urls import path
from .views import TodoCreateView, TodoEditView, TodoListView, TodoAddCollaborators, TodoRemoveCollaborators

"""
TODO:
Add the urlpatterns of the endpoints, required for implementing
Todo GET (List and Detail), PUT, PATCH and DELETE.
"""

urlpatterns = [
    path('todo/', TodoListView.as_view()),
    path('todo/<int:pk>/', TodoEditView.as_view()),
    path('todo/create/', TodoCreateView.as_view()),
    path('todo/<int:pk>/add-collaborators/', TodoAddCollaborators.as_view()),
    path('todo/<int:pk>/remove-collaborators/', TodoRemoveCollaborators.as_view()),
]