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
        fields = ['id','product','quantity','status','total_price','ordered_at']
        read_only_fields = ['total_price']

    def create(self,validated_data):
            orders = Order.objects.create(**validated_data)
            orders.save()
            return orders
        
    def update(self,instance,validated_data):
            instance.product = validated_data.get('product',instance.product)
            instance.quantity = validated_data.get('quantity',instance.quantity)
            instance.status = validated_data.get('status',instance.status)
            instance.ordered_at = validated_data.get('ordered_at',instance.ordered_at)
            instance.save()
            return instance

class CartSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Cart
        fields = ['id', 'username', 'created_at']
        read_only_fields = ['user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id','cart','product','quantity','added_at']
    
    # def create(self,validated_data):
    #      cart_item = CartItem.objects.create(**validated_data)
    #      cart_item.save()
    #      return cart_item
    
    def create(self, validated_data):
        user = self.context['request'].user
        cart = Cart.objects.get(user=user)

       
        validated_data['cart'] = cart

        cart_item = CartItem.objects.create(**validated_data)
        cart_item.save()
        return cart_item