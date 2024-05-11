from django.contrib import admin
from .models import *

admin.site.register(product)
admin.site.register(shoppingcart)
admin.site.register(order)
admin.site.register(tag)
admin.site.register(profileUser)
admin.site.register(cart_item)

