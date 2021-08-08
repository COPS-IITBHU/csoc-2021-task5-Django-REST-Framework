from django.urls import path
from .views import TodoCreateView,TodoGetAllView,TodoByIdView,TodoCollaboratorView, RemoveAllCollaboratorView,removeACollaboratorView, userAsCollaboratorView

"""
TODO:
Add the urlpatterns of the endpoints, required for implementing
Todo GET (List and Detail), PUT, PATCH and DELETE.
"""

urlpatterns = [
    path('todo/create/', TodoCreateView.as_view()),
    path('todo/<int:id>', TodoByIdView.as_view()),
    path('todo/', TodoGetAllView.as_view()),
    path('todo/<int:id>/collaborators', TodoCollaboratorView.as_view()),
    path('todo/user_as_collaborator', userAsCollaboratorView.as_view()),
    path('todo/<int:id>/remove_all_collaborators', RemoveAllCollaboratorView.as_view()),
    path('todo/remove_a_collaborator_by_its_id/<int:id>', removeACollaboratorView.as_view()),
]