from rest_framework import generics,status
from rest_framework.views import APIView
from rest_framework.response import Response
from . models import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import permissions
from . serializers import ProductCreateSerializer,CategorySerializer,OrderSerializer,CartItemSerializer,CartSerializer


class ProductCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer

class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class OrderCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status']  # Filter by status
    search_fields = ['product__name']  # Search by product name
    ordering_fields = ['ordered_at', 'total_price']  # Sort by date or price

    def get_queryset(self):
        # Return orders belonging to the logged-in user
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically associate the logged-in user with the order
        serializer.save(user=self.request.user)
class CartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user)
        if not created:
            return Response(
                {"detail": "You already have a cart.", "cart_id": cart.id},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CartItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        cart, created = Cart.objects.get_or_create(user=user)
        
        serializer = CartItemSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            cart_item = serializer.save()
            return Response(
                {"message": "Item added to cart.", "item": CartItemSerializer(cart_item).data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            return Response({"message": "No cart found for this user."}, status=status.HTTP_404_NOT_FOUND)

        items = cart.items.all()
        serializer = CartItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class CartItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return CartItem.objects.filter(cart__user=user)