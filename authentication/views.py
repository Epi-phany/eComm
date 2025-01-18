from rest_framework import generics,status
from rest_framework.response import Response
from .serializers import UserRegisterSerializer,MyTokenObtainSerializer,UserListSerializer,UserProfileSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import CustomUser,UserProfile
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response({
            "user": UserRegisterSerializer(user, context=self.get_serializer_context()).data,
            "message": "User created successfully.Login to get your token",
            },status= status.HTTP_201_CREATED)
        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainSerializer


class UserProfileView(generics.CreateAPIView):
    queryset = UserProfile
    serializer_class = UserProfileSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({
            "user": UserProfileSerializer(context=self.get_serializer_context()).data,
            "message": "Profile successfilly",
            },status= status.HTTP_201_CREATED)
        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class UserListView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

