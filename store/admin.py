from django.contrib import admin
from . models import Product,Category,Order,Cart,CartItem

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Cart)
admin.site.register(CartItem)
