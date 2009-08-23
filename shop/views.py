from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from shop.models import Product
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.db import connection, transaction

@login_required
def create_product(request):
    return render_to_response('product/form.html', {'action': 'add', 'button': 'Dodaj'})

@login_required
def add_product(request):
    product = Product(name = request.POST['name'], price = request.POST['price'])
    product.save()
    return render_to_response('product/form.html', {'action': 'add', 'button': 'Dodaj', 'message': 'Dodano produkt'})

@login_required
def edit_product(request, product_id):
    product = Product.objects.get(id=product_id)
    return render_to_response('product/form.html', {'action': 'update', 'id': product_id, 'button': 'Edytuj', 'product': product})

@login_required
def update_product(request, product_id):
    product = Product.objects.get(id=product_id)
    product.name = request.POST['name']
    product.price = request.POST['price']
    product.save()
    return render_to_response('product/form.html', {'action': 'update', 'id': product_id, 'button': 'Edytuj', 'product': product, 'message': 'Zmiany zostaly zapisane'})

@login_required
def delete_product(request, product_id):
    Product.objects.get(id=product_id).delete()
    return HttpResponseRedirect('/products/')

@transaction.commit_on_success
def register(request):
    from shop.forms import RegisterForm
    from shop.models import Client

    if request.POST:
        form = RegisterForm(request.POST)
        print form.errors
        
        if form.is_valid():
            user = User.objects.create_user(request.POST['login'], request.POST['email'], request.POST['passwd'])
            user.is_staff = False
            user.is_active = True
            user.is_superuser = False
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.save()
            
            client = Client(user=user, fullname='niepotrzebne ale dla testow ok :)')
            client.save()

            return HttpResponseRedirect('/login')
    else:
        form = RegisterForm()
    return render_to_response('auth/register.html', {'form': form})

def login(request):
    from shop.forms import LoginForm
    from django.contrib.auth import login, authenticate

    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            login(request, user)
        return HttpResponseRedirect('products/')
    else:
        form = LoginForm()
    return render_to_response('auth/login.html', {'form': form})

@login_required
def logout(request):
    from django.contrib.auth import logout
    
    logout(request)
    return HttpResponseRedirect('/')

@login_required
@transaction.commit_on_success
def add_to_card(request, product_id):
    from shop.models import Client
    
    product = Product.objects.all().get(id=product_id)
    client = Client.objects.all().get(user=request.user)
    client.products.add(product)
    client.save()
    return render_to_response('product/card.html', {'message': 'Dodano produkt do koszyka', 'client_products': client.products.all()})

@login_required
def card(request):
    from shop.models import Client
    
    return render_to_response('product/card.html', {'client_products': Client.objects.get(user=request.user).products.all()})
