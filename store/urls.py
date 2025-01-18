from django.urls import path
from .views import ProductCreateView,CategoryView,OrderCreateView,CartView,CartItemView


urlpatterns = [
    path('product/',ProductCreateView.as_view()),
    path('category/',CategoryView.as_view()),
    path('order/',OrderCreateView.as_view()),
    path('cart/',CartView.as_view()),
    path('cartitem/',CartItemView.as_view()),
]