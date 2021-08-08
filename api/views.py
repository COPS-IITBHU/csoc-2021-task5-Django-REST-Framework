from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from .serializers import TodoCreateSerializer, TodoItemSerializer, TodoCollaboratorSerializer, UserAsCollaboraterSerializer
from .models import Todo, collaboratorOfTodo
from django.http import HttpResponse


"""
TODO:
Create the appropriate View classes for implementing
Todo GET (List and Detail), PUT, PATCH and DELETE.
"""

class TodoByIdView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TodoItemSerializer
    
    def get_object(self,user, id):
        try:
            # t = Todo.objects.get(id = id)
            # if t is None:
            #     return Response({"Todo with the given id does not exist."},status = status.HTTP_404_NOT_FOUND)
            return Todo.objects.get(id = id, creator =user)
        except:
            return None 

    def get(self, request, id = None):
        todo = self.get_object(request.user, id)
        if todo is None:
             t = Todo.objects.get(id = id)
             if collaboratorOfTodo.objects.filter(todo = t, collaborator = request.user).exists():
                todo = t
             else:
                return Response({"You do not have permission to view this todo."},status = status.HTTP_400_BAD_REQUEST) 
        if todo is not None:        
            serializer = self.get_serializer(todo)
            return Response(serializer.data, status = status.HTTP_200_OK)
        


    def put(self, request, id):
        todo = self.get_object(request.user, id)
        if todo is None:
             t = Todo.objects.get(id = id)
             if collaboratorOfTodo.objects.filter(todo = t, collaborator = request.user).exists():
                todo = t
             else:
                return Response({"You do not have permission to update this todo."},status = status.HTTP_400_BAD_REQUEST)    
        if todo is not None:    
            serializer = self.get_serializer(todo, data = request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
          
        

    def patch(self, request, id = None):
        todo = self.get_object(request.user, id)
        if todo is None:
            t = Todo.objects.get(id = id)
            if collaboratorOfTodo.objects.filter(todo = t, collaborator = request.user).exists():
                todo = t
            else:
                return Response({"You do not have permission to update this todo."},status = status.HTTP_400_BAD_REQUEST)     
        if todo is not None: 
            serializer = self.get_serializer(todo, data = request.data, partial =True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
           


    def delete(self, request, id = None):
        todo = self.get_object(request.user, id)
        if todo is None:
            t = Todo.objects.get(id = id)
            if collaboratorOfTodo.objects.filter(todo = t, collaborator = request.user).exists():
                todo = t
            else:
                return Response({"You do not have permission to delete this todo."},status = status.HTTP_400_BAD_REQUEST)     
        if todo is not None: 
            todo.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)



class TodoGetAllView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TodoItemSerializer
    

    def get(self,request):
        allTodos = Todo.objects.filter(creator = request.user)
        todosDueToCollaboration = collaboratorOfTodo.objects.filter(collaborator = request.user)
        serializer_collaborator = UserAsCollaboraterSerializer(todosDueToCollaboration , many =True)
        serializer = self.get_serializer(allTodos, many =True)

        responseBody = []
       
        for x in serializer.data:
            responseBody.append(x)

        for x in serializer_collaborator.data:
            todo = Todo.objects.get(id = x['todo'])
            creatorOfTodo = todo.creator
            responseBody.append({'id' : todo.id , 'title' : todo.title , 'Todo_creator' : creatorOfTodo.username})

        return Response(responseBody, status = status.HTTP_200_OK)





class TodoCreateView(generics.GenericAPIView):
    """
    TODO:
    Currently, the /todo/create/ endpoint returns only 200 status code,
    after successful Todo creation.

    Modify the below code (if required), so that this endpoint would
    also return the serialized Todo data (id etc.), alongwith 200 status code.
    """
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TodoCreateSerializer

    def post(self, request):
        """
        Creates a Todo entry for the logged in user.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        responseBody = {
            'id' : data.id,
            'title' : data.title
        }
        return Response(responseBody, status=status.HTTP_201_CREATED)



class TodoCollaboratorView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TodoCollaboratorSerializer

    def get_object(self, user,id):
        try:
            return Todo.objects.get(id = id, creator =user)
        except:
            return None  

    def get(self, request, id):
        todo = self.get_object(request.user, id)
        if todo is None:
            t = Todo.objects.get(id = id)
            if collaboratorOfTodo.objects.filter(todo = t, collaborator = request.user).exists():
                todo = t
            else:
                return Response({"You do not have permission to view collaborators of this todo."},status = status.HTTP_400_BAD_REQUEST) 
        if todo is not None:         
            allCollaboratorsOfTodo = collaboratorOfTodo.objects.filter(todo = todo)
            serializer = TodoCollaboratorSerializer(allCollaboratorsOfTodo, many =True)
            return Response(serializer.data, status = status.HTTP_200_OK)          

    def post(self, request, id):
        todo = self.get_object(request.user,id)
        if todo is not None:
            Data = request.data
            user = request.user
            if(user.username == Data['collaborator_username']):
                return Response({"You cannot become the collaborator as you are the creator of this todo"},status = status.HTTP_400_BAD_REQUEST)
            else:
                serializer = TodoCollaboratorSerializer(data = request.data, context = {"todo" : todo})
                serializer.is_valid(raise_exception=True)
                newCollaborator = serializer.create()
                if newCollaborator is not None:
                    return Response(serializer.data)
                else:
                    return  Response({"Entered user is already a collaborator of this todo."}, status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"You do not have permission to add collaborators to this todo"},status = status.HTTP_400_BAD_REQUEST)




class RemoveAllCollaboratorView(generics.GenericAPIView):
        permission_classes = (permissions.IsAuthenticated, )
        serializer_class = TodoCollaboratorSerializer

        def delete(self, request, id):
            todo = Todo.objects.get(id = id)
            if (todo.creator != request.user):
                return Response({"You do not have permissions to delete collaborators of this todo."},status = status.HTTP_400_BAD_REQUEST)
            elif todo is not None:
                CollaboratorsToBeDeleted = collaboratorOfTodo.objects.filter(todo = todo)
                for c in CollaboratorsToBeDeleted:
                    c.delete()
                return Response({"All Collaborators of this todo deleted successfully"},status = status.HTTP_204_NO_CONTENT)
            
                   



class removeACollaboratorView(generics.GenericAPIView):
        permission_classes = (permissions.IsAuthenticated, )
        serializer_class = TodoCollaboratorSerializer  

        def delete(self, request, id):
            CollaboratorToBeDeleted = collaboratorOfTodo.objects.get(id = id)
            todo = CollaboratorToBeDeleted.todo
            if todo.creator == request.user:
                CollaboratorToBeDeleted.delete()
                return Response({"Collaborator deleted successfully"},status = status.HTTP_204_NO_CONTENT)
               
            else:
                return Response({"You do not have permissions to delete collaborator of this todo."},status = status.HTTP_400_BAD_REQUEST) 


class userAsCollaboratorView(generics.GenericAPIView):   
        permission_classes = (permissions.IsAuthenticated, )
        serializer_class = UserAsCollaboraterSerializer
        
        def get(self, request):
            todos = collaboratorOfTodo.objects.filter(collaborator = request.user)
            serializer = UserAsCollaboraterSerializer(todos , many =True)
            responseBody = []
            for x in serializer.data:
                todo = Todo.objects.get(id = x['todo'])
                creatorOfTodo = todo.creator
                responseBody.append({'Todo_id' : todo.id , 'Todo_title' : todo.title , 'Todo_creator' : creatorOfTodo.username})
            return Response(responseBody)
