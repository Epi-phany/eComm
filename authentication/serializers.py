from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from .models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken

#User = get_user_model()
User = CustomUser

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','firstname','lastname','username','email','mobile','password']
        extra_kwargs = {'password':{'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    def update(self,instance,validated_data):
        instance.email = validated_data.get('email',instance.email)
        instance.username = validated_data.get('username',instance.username)
        instance.firstname = validated_data.get('firstname',instance.firstname)
        instance.lastname = validated_data.get('lastname',instance.lastname)
        instance.mobile = validated_data.get('mobile',instance.mobile)
        password = validated_data.get('password',None)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

class MyTokenObtainSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'), username=username, password=password)

            if not user:
                raise serializers.ValidationError('Invalid credentials,check username or password')
            refresh = RefreshToken.for_user(user)
            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        else:
            raise serializers.ValidationError('Must include "username" and "password"')
        

