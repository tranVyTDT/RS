from django.contrib.auth import authenticate
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers, viewsets, permissions
from user.models import CustomUser
from .serializers import SignupSerializer, LoginSerializer

class UserViewSet(viewsets.ViewSet):

    @action(detail= False, methods = ['post'])
    def signup(self, request):
        try:
            is_username_exist = CustomUser.objects.get(username=request.data['username'])
            return Response({ 'error': 'username exist, select forget password' })
        except:
            pass

        user = request.user

        if user.is_anonymous:
            serializer = SignupSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
                    
            return Response({ 'error': 'invalid field' })
        else:
            try:
                role = request.data.pop('role')
                if role not in  ['staff', 'director']:
                    return Response({ 'error': 'invalid role' })
            except:
                return Response({ 'error': 'missing role' })


            if 'director' in user.account_type or user.is_superuser:
                serializer = SignupSerializer(data = request.data)
                if serializer.is_valid():
                    serializer.save(role= role)
                    return Response(serializer.data)
                return Response({ 'error': 'invalid field' })
            else:
                return Response({ 'error': 'you dont have permission' })
        
    @action(detail= False, methods= ['post'])
    def login(self, request):
        username = request.data.get('username', None)
        password= request.data.get('password', None)
        
        user = authenticate(username= username, password= password)

        if user:
            serializer = LoginSerializer(user)
            return Response(serializer.data)
        return Response({ 'error': 'wrong password or username' })