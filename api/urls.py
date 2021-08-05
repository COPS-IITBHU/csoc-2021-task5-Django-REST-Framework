from django.urls import path
from .views import TodoCreateView, TodoListView, TodoView, AddCollaboratorView, RemoveCollaboratorView

"""
TODO:
Add the urlpatterns of the endpoints, required for implementing
Todo GET (List and Detail), PUT, PATCH and DELETE.
"""

urlpatterns = [
    path('todo/create/', TodoCreateView.as_view()),
    path('todo/', TodoListView.as_view()),
    path('todo/<int:pk>/', TodoView.as_view()),
    path('todo/<int:pk>/add-collaborators', AddCollaboratorView.as_view()),
    path('todo/<int:pk>/remove-collaborators', RemoveCollaboratorView.as_view()),
]