from rest_framework import serializers
from  post.models import Post
import random


class PostSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        fields= ['post_id', 'title', 'content', 'category', 'upload', 'is_approve_staff', 'is_approve_director']
        read_only_fields = ['is_approve_staff', 'is_approve_director']
        extra_kwargs = {
            'content': {'write_only': True}
        }
    
    def create(self, validated_data):
        user = self.context.get('user')
        try:
            upload = validated_data['upload']
        except:
            upload = None
        post = Post.objects.create( 
            author = user,
            post_id = validated_data['post_id'],
            title = validated_data['title'],
            content = validated_data['content'],
            category = validated_data['category'],
            upload = None
        )
        return post

    

class DetailPostSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        fields= ['post_id', 'title', 'content', 'category', 'upload', 'is_approve_staff', 'is_approve_director']
        read_only_fields = ['post_id', 'is_approve_staff', 'is_approve_director']
        # extra_kwargs = {
        #     'is_approve_staff': {'write_only': True},
        #     'is_approve_director': {'write_only': True}
        # }

    def update(self, instance, validated_data):
        
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.category = validated_data.get('category', instance.category)
        instance.upload = validated_data.get('upload', instance.upload)
        instance.save()

        approve = validated_data.get('approve', None)

        if approve:
            user = self.context.get('user')
            if user.is_superuser or 'director' in user.account_type:
                if approve == "no":
                    instance.delete()
                else:
                    instance.is_approve_staff = True
                    instance.is_approve_director = True
                    instance.approve_director = user
                    instance.save()
            if 'staff' in user.account_type:
                if approve == 'no':
                    instance.delete()
                else:
                    instance.is_approve_staff = True
                    instance.approve_staff = user
                    instance.save()

        return instance

    
    