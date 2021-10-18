from rest_framework import serializers
from user.models import CustomUser
from .decentralization import UserGroupPermission

class SignupSerializer(serializers.ModelSerializer):
    password2= serializers.CharField(style= {'input_type': 'password'}, write_only= True)

    class Meta:
        model = CustomUser
        fields = ['username', 'profile_name', 'password', 'password2', 'sex', 'birthday', 'address', 'phone', 'email']

    def create(self, validated_data):
        password = validated_data['password']
        password2 = validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({ 'error': "password must match" })
        
        new_user = CustomUser(  
                                username=validated_data['username'],
                                profile_name=validated_data['profile_name'],
                                sex=validated_data['sex'],
                                birthday=validated_data['birthday'],
                                address=validated_data['address'],
                                phone=validated_data['phone'],
                                email=validated_data['email'],
                            )

        new_user.set_password(password)
        new_user.is_active = True

        role = validated_data.get('role', None)
        if role == 'staff':
            new_user.groups.add(UserGroupPermission.get_staff_group())
        elif role == 'director':
            new_user.groups.add(UserGroupPermission.get_director_group())
        
        new_user.save()
        return new_user


class LoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields= ('access_token', 'refresh_token')
        read_only_fields = ['access_token', 'refresh_token']