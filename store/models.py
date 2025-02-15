from django.db import models
from authentication.models import CustomUser

User = CustomUser

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return f'{self.name} ${self.price}'


class Order(models.Model):
    STATUS = [
        ('PENDING', 'Pending'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELED', 'Canceled'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    status = models.CharField(max_length=30,choices=STATUS,default='PENDING')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    ordered_at = models.DateTimeField(auto_now_add=True)

    # def save(self, *args, **kwargs):
    #     self.total_price = self.quantity * self.product.price
    #     super().save(*args, **kwargs)
    def save(self, *args, **kwargs):
        if self.pk:  
            previous_status = Order.objects.get(pk=self.pk).status
            if previous_status != self.status:
                OrderStatusHistory.objects.create(order=self, status=self.status)
            self.total_price = self.quantity * self.product.price
            super().save(*args, **kwargs)
    def cancel(self):
        if self.status not in ['PENDING']:
            raise ValueError("Only pending orders can be canceled.")
        self.status = 'CANCELED'
        self.save()

    def ship(self):
        if self.status != 'PENDING':
            raise ValueError("Only pending orders can be shipped.")
        self.status = 'SHIPPED'
        self.save()

    def __str__(self):
        return f'Order of {self.product.name}'
    

class OrderStatusHistory(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='status_history')
    status = models.CharField(max_length=30, choices=Order.STATUS)
    changed_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.order} - {self.status} at {self.changed_at}'

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user.username}" if self.user else "Guest Cart"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'

    def get_total_price(self):
        return self.quantity * self.product.price