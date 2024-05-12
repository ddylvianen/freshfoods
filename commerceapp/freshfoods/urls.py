from django.urls import path
from . import views

app_name= 'fresh'
urlpatterns = [
    path('', views.home, name='home'),
    path('profile', views.profile, name='profile'),
    path('shopping_cart', views.shopping_cart, name='shopping_cart'),
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('register', views.register_user, name='register'),
    path("get/cart/item/<int:id>", views.get_item, name='item-cart'),
    path('add/item/<int:id>/', views.cart_add_item, name='add_cart_item'),
    path('clear-cart', views.clear_shopping_cart, name='clear_shopping_cart'),
    path('remove/item/<int:id>', views.cart_item_remove, name='remove-item'),
    path('remove/all/item/<int:id>', views.cart_items_remove, name='item_remove'),
    # path('static_files/<path:path>', views.serve_static_file, name='serve_static_file'),
]