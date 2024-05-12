import mimetypes
from django.shortcuts import render
from .models import *
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import createuserform, loginform, UserProfileForm
from django.http import HttpResponse, HttpResponseNotFound
from django.templatetags.static import static
from pathlib import Path
import os


# Create your views here.
@login_required(login_url='/login')
def home(request):
    Tags = tag.objects.all()
    products = product.objects.all()
    user_info = profileUser.objects.get(user=request.user)
    #user_info.img = 
    cart = shoppingcart.objects.filter(user=request.user)
    if cart.exists():
        cart = cart[0]
        items = cart.products.all()
    else:
        items = {}

    content = {'products': products,
               'tags': Tags,
               'cart-items': items,
               'profileuser': user_info,
               'link': "/media/"}

    return render(request, 'freshfoods/index.html', content)

@login_required(login_url='/login')
def profile(request):
    content = {}
    return render(request, 'freshfoods/profile.html', content)

def login_user(request):
    if request.method == "POST":
        form = loginform(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request,user=user)
                message = 'login succesfull!'
                return redirect('/')
            else:
                message = 'account does not exist!'
                return redirect('register')
        else:
            message = 'something went wrong! \n please try again!'
    else:
        form = loginform
        message = ''

    content = {'form': form, 'message': message}
    return render(request, 'freshfoods/login.html', content)

def logout_user(request):
    logout(request)
    return redirect('/')

def register_user(request):
    if request.method == "POST":
        user_form = createuserform(request.POST)
        if user_form.is_valid():
            username = user_form.cleaned_data['username']
            password = user_form.cleaned_data['password1']
            user_form.save()
            user = authenticate(username=username, password=password)
            profile = profileUser(user=user)
            profile.save()
            return redirect('login')    
        else: 
            message = 'something went wrong! \n please try again!'
    else:
        user_form = createuserform
        message = ''

    content = {'user_form': user_form, 'message': message}
    return render(request, 'freshfoods/register.html', content)

@login_required(login_url='/login')
def settings(request):
    profile = ""
    content = {}
    return render(request, 'freshfoods/profile.html', content)

@login_required(login_url='/login')
def profile(request):
    return render(request, 'freshfoods/profile.html')

def cart_add_item(request, id):
    item = product.objects.get(id=id)
    cart = shoppingcart.objects.filter(user=request.user)
    if cart.exists():
        cart = cart[0]
        item_cart = cart_item.objects.all().filter(item=item, user=request.user)
        if item_cart.exists():
            item_cart = item_cart[0]
            item_cart.quantity += 1
        else:
            item_cart = cart_item(quantity=1, user=request.user)
            item_cart.item = item    
        item_cart.save()
        cart.products.add(item_cart)
    else:
        item_cart = cart_item(quantity=1, user=request.user)
        item_cart.item = item 
        item_cart.save() 
        cart = shoppingcart(user=request.user, )
        cart.save()
        cart.products.add(item_cart)

    item_cart.save()  
    cart.total_items += 1
    cart.save()

    return HttpResponse(status=200)

def cart_item_remove(request, id):
    produc = product.objects.get(id=id)
    item = cart_item.objects.get(user=request.user, item=produc)
    item.quantity -= 1
    item.save()

    return HttpResponse(status=200)

def cart_items_remove(request,id):
    produc = product.objects.get(id=id)
    item = cart_item.objects.all().filter(user=request.user, item=produc)[0]
    cart = shoppingcart.objects.get(user=request.user)
    cart.products.remove(item)
    cart.save()
    item.delete()
    print(item)
    return HttpResponse(status=200)

def get_item(request, id):
    produc = product.objects.get(id=id)
    item = cart_item.objects.filter(user=request.user, item=produc)
    if item.exists():
        item = item[0]
        num = item.quantity
    else:
        num = 0

    return HttpResponse(num, status=200)
@login_required(login_url='/login')
def shopping_cart(request):
    cart = shoppingcart.objects.filter(user=request.user).prefetch_related("products")
    totalitem = 0
    totalprice = 0

    if cart.exists():
        cart = cart[0]
        for i in cart.products.all():
            print(i)
            item = i.item
            totalitem += i.quantity
            if item.discount == 0:
                item.price = round((float(item.price) * i.quantity), 2)
            else:
                item.price = round(float(item.price) - ((item.discount / 100) * float(item.price)* i.quantity), 2)
            
            totalprice += item.price
    else:
        cart = {}

    content = {'cart': cart, 
               'totalitem': totalitem, 
               'totalprice': round(totalprice, 2),
               'link': "/media/",}
    
    return render(request, 'freshfoods/shopping_cart.html', content)


def clear_shopping_cart(request):
    cart = shoppingcart.objects.all().filter(user=request.user)
    items = cart_item.objects.all().filter(user=request.user)

    cart.delete()
    items.delete()
    return HttpResponse(status=200)

# def serve_static_file(request, path):
#     file_path = os.path.join('static_files', path)
#     if os.path.exists(file_path):
#         with open(file_path, 'rb') as f:
#             return HttpResponse(f.read(), content_type=mimetypes.guess_type(file_path)[0])
#     else:
#         return HttpResponseNotFound()
    

# def serve_media_file(request, path):
#     file_path = os.path.join('media_files', path)
#     if os.path.exists(file_path):
#         with open(file_path, 'rb') as f:
#             return HttpResponse(f.read(), content_type=mimetypes.guess_type(file_path)[0])
#     else:
#         return HttpResponseNotFound()

