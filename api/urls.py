from django.urls import path
from .views import TodoCreateView, TodoGetView, TodoOperationsView, TodoAddCollabView, TodoRemoveCollabView 

"""
TODO:
Add the urlpatterns of the endpoints, required for implementing
Todo GET (List and Detail), PUT, PATCH and DELETE.
"""

urlpatterns = [
    path('todo/create/', TodoCreateView.as_view()),
    path('todo/', TodoGetView.as_view()),
    path('todo/<int:id>/', TodoOperationsView.as_view()),
    path('todo/<int:id>/add-collaborators/', TodoAddCollabView.as_view()),
    path('todo/<int:id>/remove-collaborators/', TodoRemoveCollabView.as_view())
]