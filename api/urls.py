from django.urls import path
from .views import *

"""
TODO:
Add the urlpatterns of the endpoints, required for implementing
Todo GET (List and Detail), PUT, PATCH and DELETE.
"""

urlpatterns = [
    path('todo/create/', TodoCreateView.as_view()),
    path('todo/', TodoAllView.as_view()),
    path('todo/<int:id>/', TodoDetailView.as_view()),
    path('todo/<int:id>/add-collaborators/', AddCollab.as_view()),
    path('todo/<int:id>/remove-collaborators/', RemoveCollab.as_view()),
]