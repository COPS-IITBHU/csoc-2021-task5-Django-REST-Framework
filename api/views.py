from django.http.response import HttpResponse
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from .serializers import *
from .models import Todo
from django.http import HttpResponse
from django.contrib.auth.models import User
from rest_framework import mixins
from rest_framework.response import Response


# class for the cloolabartor view 
class TodoAddCollaboratorsView(generics.GenericAPIView):
    # check for the authenticity 
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TodoCollaboratorsSerializer



    # function for the post

    def post(self, request, id):
        serializer = TodoCollaboratorsSerializer(data=request.data)


        # checking the validity of the serializer
        if serializer.is_valid(raise_exception=True):     
            usernames = request.data['usernames'].replace(' ','').split(',')
            # setting and getitng the list of users 
            usernames = set(usernames)


            usernames = list(usernames)





            try:
                todo = Todo.objects.get(id=id)
                # getting the ids 
            except:
                # returning with the error code of 404 
                return Response({ "todo": "Not able to found" }, status=404)

            # checking the equality ( same )
            if request.user == todo.creator:

                all_users = []
                for user in User.objects.all():
                    all_users.append(user.username)
                    
                response = {
                    "successful": [], "alreadyExist": [], "incorrectUsername":[]
                }


                # finding user in all the users 
                for user in usernames:
                    if user in todo.collaborators:
                        # telling the already existing 
                        response['alreadyExist'].append(user)
                    elif user not in all_users:
                        # returning incorrect username 
                        response['incorrectUsername'].append(user)
                    else:
                        # returning successful 
                        response['successful'].append(user)
                        todo.collaborators.append(user)
                        todo.save()


                # checking which exist means either it is successful, alreadyExists or incorrectUsername 
                if not response['successful']:
                    del response['successful']


                if not response['alreadyExist']:
                    del response['alreadyExist']


                if not response['incorrectUsername']:
                    del response['incorrectUsername']
                return Response(response, status=200)


            # otherwise returning the not found response 

            else:
                # return HttpResponse ('not able to find ')
                return Response({ "todo": "Not able to found" }, status=404)





class TodoRemoveCollaboratorsView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TodoCollaboratorsSerializer
    


    def post(self, request, id):



        serializer = TodoCollaboratorsSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):     
            usernames = request.data['usernames'].replace(' ','').split(',')
            # same getting and setting the users 
            usernames = set(usernames)
            usernames = list(usernames)


            try:
                todo = Todo.objects.get(id=id)
            except:
                return Response({ "todo": "Not found" }, status=404)
                # returning with the error code of 404


            if request.user == todo.creator:
                all_users = []
                for user in User.objects.all():
                    all_users.append(user.username)
                response = {
                    "successful": [], "incorrectUsername":[]
                }

                # finding the user in users 
                for user in usernames:
                    if user in todo.collaborators:
                        response['successful'].append(user)
                        todo.collaborators.remove(user)
                        todo.save()
                    else:
                        response['incorrectUsername'].append(user)

                        
                if not response['successful']:
                    del response['successful']
                if not response['incorrectUsername']:
                    del response['incorrectUsername']
                return Response(response, status=200)



            else:
                # return HttpResponse ('not able to find ')

                return Response({ "todo": "Not found" }, status=404)









class TodoView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TodoSerializer

    def get(self, request, id):
        try:
            todo = Todo.objects.get(id=id)
        except:
            return Response({ "todo": "Not able to found" }, status=404)
        if request.user == todo.creator or str(request.user) in todo.collaborators:
            serializer = TodoSerializer(todo)
            return Response(serializer.data, status=200)
        else:
            # return HttpResponse ('not able to find ')
            return Response({"todo": "Not able to found" }, status=404)
    



    def put(self, request, id):
        try:
            todo = Todo.objects.get(id=id)
        except:
            return Response({ "todo": "Not able to found" }, status=404)


        if request.user == todo.creator or str(request.user) in todo.collaborators:
            # assigning
            serializer = TodoSerializer(todo ,data=request.data)


            if serializer.is_valid(raise_exception=True):
                # for saving the serializer
                serializer.save()
            return Response(serializer.data, status=200)

        else:
            # return HttpResponse ('not able to find ')

            return Response({"todo": "Not able to found" }, status=404)
    




    def patch(self, request, id):
        try:
            todo = Todo.objects.get(id=id)
        except:
            return Response({ "todo": "Not able to found" }, status=404)


        if request.user == todo.creator or str(request.user) in todo.collaborators:
            serializer = TodoSerializer(todo ,data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                # saving
                serializer.save()
            return Response(serializer.data, status=200)
        else:
            # return HttpResponse ('not able to find ')
            return Response({"todo": "Not able to found" }, status=404)
    




    def delete(self, request, id):

        
        try:
            todo = Todo.objects.get(id=id)
        except:
            return Response({ "todo": "Not able to found" }, status=404)
            
        if request.user == todo.creator or str(request.user) in todo.collaborators:
            todo.delete()
            return Response({ "todo": "removed successfully" }, status=200)



        else:
            # return HttpResponse ('not able to find ')

            return Response({"todo": "Not able to found" }, status=404)





class TodoListView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TodoListSerializer
    queryset = Todo.objects.all()





    def get(self, request):


        todos_self = Todo.objects.filter(creator__exact=request.user)
        serializers_self = TodoListSerializer(todos_self, many=True)
        todos_other = Todo.objects.filter(collaborators__contains=request.user)
        serializers_other = TodoListSerializer(todos_other, many=True)
        return Response({
            "createdTODOs": serializers_self.data,
            "collaboratedTODOs": serializers_other.data
        }, status=200)




class TodoCreateView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = TodoCreateSerializer




    def post(self, request):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # checking the validity
        return Response(serializer.save(), status=200)
