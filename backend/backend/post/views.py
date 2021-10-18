from collections import namedtuple
from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers, viewsets, permissions
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from post.models import Post
from .serializers import PostSerializer, DetailPostSerializer



class PostViewSet(viewsets.ViewSet):

    parser_classes = (MultiPartParser,FormParser,JSONParser)

    def get_permissions(self):
        """
            Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list':
            permission_classes = []
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def list(self, request):
        posts = Post.objects.all()
        # filter if has, get_approve_staff(posts), get_approve_director(posts)
        name_id = request.GET.get('name_id', None)
        if name_id:
            posts.filter(Q(post_id = name_id) | Q(title = name_id))
            
        serializer = PostSerializer(posts, many= True)
        return Response(serializer.data)

    def retrieve(self, request, pk = None):
  
        try:
            post = Post.objects.get(post_id = pk)
        except:
            return Response({ 'error': 'post is not exist' })
        
        serializer = DetailPostSerializer(post)
        return Response(serializer.data)


    def create(self, request):
        serializer = PostSerializer(data = request.data, context = {'user': request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
                
        return Response({ 'error': 'invalid field' })

    
    def update(self, request, pk = None):
        try:
            post = Post.objects.get(post_id = pk)
        except:
            return Response({ 'error': 'post is not exist' })
            
        if len(request.user.account_type) == 0 and request.user.is_superuser == False:
            if request.user.id != post.author.id:
                return Response({ 'error': 'must be the owner' })

            serializer = DetailPostSerializer(post, data = request.data, context = {'user': request.user})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response({ 'error': 'invalid field' })

        try:
            approve = request.data.pop('approve')
            if approve not in ['yes', 'no']:
                return Response({ 'error': 'approve is not valid' })
        except:
            return Response({ 'error': 'approve missing field' })

        user = request.user

        serializer = DetailPostSerializer(post, data = request.data, context = {'user': request.user})
        if serializer.is_valid():
            serializer.save(approve = approve)
            return Response(serializer.data)
  
        return Response({ 'error': 'invalid field' })
    
    @action(detail= False, methods = ['get'])
    def list_post_receive(self, request):
        posts = Post.objects.filter(Q(is_approve_staff = False) & Q(is_approve_director = False))
        serializer = PostSerializer(posts, many= True)
        return Response(serializer.data)
    


    @action(detail= False, methods = ['get'])
    def list_post_agree(self, request):
        posts = Post.objects.filter(Q(is_approve_staff = True) & Q(is_approve_director = False))
        serializer = PostSerializer(posts, many= True)
        return Response(serializer.data)
