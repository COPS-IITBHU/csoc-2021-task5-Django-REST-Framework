from rest_framework.permissions import BasePermission
from .models import Todo

class AllUsers(BasePermission):
    def has_object_permission(self, request, view, object):
        todo = Todo.objects.filter(id = object.id)
        if todo:
            if request.user == todo[0].creator or request.user in todo[0].collaborators.all():
                return True
        return False
class Creator(BasePermission):
    def has_permission(self, request, view):
        todo = Todo.objects.filter(id = view.kwargs['id'])
        if todo:
            if request.user == todo[0].creator:
                return True
        return False


