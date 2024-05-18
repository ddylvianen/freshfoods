from datetime import datetime
import mimetypes
from django.shortcuts import get_object_or_404, render
from .models import *
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import createuserform, loginform, UserProfileForm
from django.http import HttpResponse, HttpResponseNotFound
from django.core.exceptions import ObjectDoesNotExist



# Create your views here.
@login_required(login_url='/login')
def home(request):
    Tags = tag.objects.all()
    products = product.objects.all()
    user_info = profileUser.objects.get(user=request.user)
    try:
        cart = shoppingcart.objects.get(user=request.user)
        totalitem = cart.total_item()
    except ObjectDoesNotExist:
        items = {}
        totalitem = 0

    content = {'products': products,
               'tags': Tags,
               'total': totalitem,
               'profileuser': user_info,
               'link': "/media/",}

    return render(request, 'freshfoods/index.html', content)

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
                return redirect('fresh:register')
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
            return redirect('fresh:login')    
        else: 
            message = 'something went wrong! \n please try again!'
    else:
        user_form = createuserform
        message = ''

    content = {'user_form': user_form, 'message': message}
    return render(request, 'freshfoods/register.html', content)

@login_required(login_url='/login')
def settings(request):
    profile = profileUser.objects.get(user=request.user)
    content = {'profile': profile,
               'link': "/media/"}
    return render(request, 'freshfoods/profile.html', content)

@login_required(login_url='/login')
def profile(request):
    profile = profileUser.objects.get(user=request.user)
    content = {'profile': profile,
               'link': "/media/"}
    return render(request, 'freshfoods/profile.html', content)

def cart_add_item(request, id):
    item = product.objects.get(id=id)
    deff_item_cart = {'quantity': 0, 'user': request.user, 'item': item, 'invoice': "", "price": 0}
    item_cart = cart_item.objects.get_or_create(item=item, user=request.user, invoice='', defaults=deff_item_cart)[0]
    
    item_cart.save()
    item_cart.price_item()
    item_cart.add_item()
    item_cart.save()

    deff_cart = {"user": request.user}
    cart = shoppingcart.objects.get_or_create(user=request.user, defaults=deff_cart)[0]
    
    cart.save()
    cart.products.add(item_cart) 
    cart.save()

    return HttpResponse(status=200)

def cart_item_remove(request, id):
    produc = product.objects.get(id=id)
    cart_item.objects.get(user=request.user, item=produc, invoice="").remove_item()

    return HttpResponse(status=200)

def cart_items_remove(request, id):
    produc = product.objects.get(id=id)
    cart_item.objects.get(user=request.user, item=produc, invoice="").delete()
    return HttpResponse(status=200)


def get_item(request, id):
    produc = product.objects.get(id=id)
    try:
        item = cart_item.objects.get(user=request.user, invoice="", item=produc)
        item.price_item()
        num = item.quantity
    except ObjectDoesNotExist:
        num = 0

    return HttpResponse(num, status=200)

@login_required(login_url='/login')
def shopping_cart(request):
    profile = profileUser.objects.get(user=request.user)
    try:
        cart = shoppingcart.objects.get(user=request.user)
        print(cart.products)
        totalitem = cart.total_item()
        totalprice = cart.total_price()
    except ObjectDoesNotExist:
        totalitem = 0
        totalprice = 0
        cart = {}

    content = {'cart': cart, 
               'totalitem': totalitem, 
               'totalprice': round(totalprice, 2),
               'profile': profile,
               'link': "/media/",}
    
    return render(request, 'freshfoods/shopping_cart.html', content)


def clear_shopping_cart(request):
    shoppingcart.objects.all().filter(user=request.user).delete()
    return HttpResponse(status=200)

def create_order(request):
    inv = f"#{request.user} {datetime.today()}"
    print(inv)
    user_order = order(user=request.user, invoice=inv)
    products = cart_item.objects.filter(user=request.user, invoice="")
    cart = shoppingcart.objects.get(user=request.user)
    user_order.save()

    products.update(invoice=inv)
    cart.delete()

    user_order.product.bulk_create(objs=products)
    user_order.save()
    return HttpResponse(status=200)

