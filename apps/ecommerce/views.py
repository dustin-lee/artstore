from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.forms import formset_factory
from .models import Gen_user, Log_user, Gen_user_product, Log_user_product, Cart_product, Cart, Order, Product, Order_product, Log_user, Billing, Shipping
import stripe

def index(request):
    return render(request, 'ecommerce/index.html')

def home(request):
    request.session['logged_user'] = ''
    return render(request, 'ecommerce/home.html')

def admin(request):
    return render(request, 'ecommerce/admin.html')

def register(request):
    if request.method == "POST":
        form_errors = AdminUser.objects.validate(request.POST)

        if len(form_errors) > 0:
            for error in form_errors:
                messages.error(request, error)
        else:
            AdminUser.objects.register(request.POST)
            messages.success(request, "You have successfully registered! Please login to continue")

    return redirect('/admin')

def login(request):
    if request.method == "POST":
        user = AdminUser.objects.login(request.POST)
        if not user:
            messages.error(request, "Not login credentials!")
        else:
           request.session['logged_user'] = user.id
           return redirect('/orders')

def logout(request):
    if 'logged_user' in request.session:
        request.session['logged_user'] = ''
        request.session.pop('logged_user')
    return redirect('/')

def productpage(request):
    if request.method == 'GET':
        products = Product.objects.all()
        context = {'products': products}
    return render(request, 'ecommerce/productpage.html', context)

def description(request, id):
    if request.method == 'POST':
        products = Product.objects.filter(id=id)
        context = {'meep': products }
        return render(request, 'ecommerce/description.html', context)

def shoppingcart(request, id):
    if request.method == 'POST':
        products = Product.objects.filter(id=id)
        context = {'meep' : products}
    return render(request, 'ecommerce/shoppingcart.html', context)


def products(request):
    return render(request, 'ecommerce/products.html')

def orders(request):
    orders = Order.objects.all()
    context = {
        'orders': orders,
    }
    return render(request, 'ecommerce/orders.html', context)

def display(request, id):
    orders = Order.objects.filter(id=id)
    context = {
        'orders': orders,
    }
    return render(request, 'ecommerce/display.html', context)

def addproduct(request):
    if request.method == 'POST':
        print '*'
        Product.objects.create(name=request.POST['name'], description=request.POST['description'], categories=request.POST['categories'], price=request.POST['price'], quantity=request.POST['quantity'], image=request.FILES['image2'])
        print '**'
        return redirect ('/inventory')

def editproduct(request):
    if request.method == 'POST':
        Product.objects.create(name=request.POST['name'], description=request.POST['description'], categories=request.POST['categories'], price=request.POST['price'], quantity=request.POST['quantity'], image=request.FILES['image'])
        return redirect ('/inventory')

def delete(request, id):
    remove = Product.objects.get(id=id)
    if request.method == 'POST':
        remove.delete()
        return redirect ('/inventory')

def inventory(request):
    if request.method == 'GET':
        products = Product.objects.all()
        context = {'products': products}
    return render(request, 'ecommerce/inventory.html', context)

def checkout(request):
    if request.method == 'GET':
        return render(request, 'ecommerce/checkout.html')

    if request.method == 'POST':
        token = request.POST['stripeToken']
        # order = Order.objects.get(id=id)
        shipping = Shipping.objects.create(name=request.POST['name'], address= request.POST['address'], city= request.POST['city'], state= request.POST['state'], zipcode=request.POST['zipcode'])
        billing = Billing.objects.create(address= request.POST['address2'], city= request.POST['city2'], state= request.POST['state2'], zipcode=request.POST['zipcode2'], token= token)
        try:
            charge = stripe.Charge.create(
                amount=1000, # Amount in cents
                currency="usd",
                source=token,
                description="Example charge"
            )
        except stripe.error.CardError as e:
            pass
        return redirect ('/home')
        #Add id to param and id=order.id to redirect
