from rest_framework import generics,status
from rest_framework.response import Response
from .serializers import UserRegisterSerializer,MyTokenObtainSerializer,UserListSerializer,UserProfileSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import CustomUser,UserProfile
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, IsAdminUser

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
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserProfileSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, 
                            {"message":"Profile successfully created"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserListView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsAdminUser]

