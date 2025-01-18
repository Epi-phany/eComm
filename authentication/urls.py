from django.urls import path
from .views import RegisterView,LoginView,UserListView,UserProfileView


urlpatterns = [
    path('signup/',RegisterView.as_view(),name='signup'),
    path('login/',LoginView.as_view(),name='login'),
    path('profile/',UserProfileView.as_view(),name='profile'),
    path('userlist/',UserListView.as_view()),
]