from django.urls import path
from .views import CollaboratorAdder, CollaboratorRemover, TodoCreateView, TodoFunctions, TodoList

"""
TODO:
Add the urlpatterns of the endpoints, required for implementing
Todo GET (List and Detail), PUT, PATCH and DELETE.
"""

urlpatterns = [
    path('todo/', TodoList.as_view()),
    path('todo/create/', TodoCreateView.as_view()),
    path('todo/<int:id>/', TodoFunctions.as_view()),
    path('todo/<int:id>/add-collaborators/', CollaboratorAdder.as_view()),
    path('todo/<int:id>/remove-collaborators/', CollaboratorRemover.as_view()),
]