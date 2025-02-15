from rest_framework import serializers
from . models import Category,Product,Order,Cart, CartItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name','slug']

class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','category','name','description','price','stock','slug','image']

    def create(self, validated_data):
        products = Product.objects.create(**validated_data)
        products.save()
        return products



class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'product', 'quantity', 'status', 'total_price', 'ordered_at']
        read_only_fields = ['total_price', 'ordered_at']

    def validate_status(self, value):
        if self.instance and self.instance.status == 'CANCELED' and value != 'CANCELED':
            raise serializers.ValidationError("Cannot change the status of a canceled order.")
        return value


class CartSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Cart
        fields = ['id', 'username', 'created_at']
        read_only_fields = ['user']
    
    def validate(self, data):
        user = self.context['request'].user
        if Cart.objects.filter(user=user).exists():
            raise serializers.ValidationError("A cart already exists for this user.")
        return data

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
    

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id','cart','product','quantity','added_at']
        read_only_fields = ['cart', 'added_at']


    def create(self, validated_data):
        user = self.context['request'].user

        cart, created = Cart.objects.get_or_create(user=user)

        product = validated_data['product']
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, product=product,
            defaults={'quantity': validated_data.get('quantity', 1)}
        )

        if not created:
            cart_item.quantity += validated_data.get('quantity', 1)
            cart_item.save()
        return cart_item
    

    # def create(self, validated_data):
    #     user = self.context['request'].user
    #     cart = Cart.objects.get(user=user)

       
    #     validated_data['cart'] = cart

    #     cart_item = CartItem.objects.create(**validated_data)
    #     cart_item.save()
    #     return cart_item
    
    