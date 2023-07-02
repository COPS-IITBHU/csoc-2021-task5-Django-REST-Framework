from django.urls import path
from .views import *



urlpatterns = [
    path('todo/', TodoListView.as_view()),
    path('todo/<int:id>/', TodoView.as_view()),
    path('todo/create/', TodoCreateView.as_view()),
    path('todo/<int:id>/add-collaborators/', TodoAddCollaboratorsView.as_view()),
    path('todo/<int:id>/remove-collaborators/', TodoRemoveCollaboratorsView.as_view())
]