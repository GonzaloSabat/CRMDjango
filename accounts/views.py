from multiprocessing import context
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
# Create your views here.
from .models import *
from .forms import OrderForm
from .filters import OrderFilter

def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    
    customers_total = Customer.objects.count()
    orders_total = Order.objects.count()
    
    delivered_orders = Order.objects.filter(status="Delivered").count()
    # delivered_orders = orders.filter(status='Delivered').count() # Another way of doing it
    pending_orders = Order.objects.filter(status="Pending").count()
    # pending_orders = orders.filter(status='Pending').count() # Another way of doing this
    
    context = {'orders':orders,'customers':customers,
               'orders_total':orders_total,'delivered_orders':delivered_orders,
                'pending_orders':pending_orders,'customers_total':customers_total}
    return render(request, 'accounts/dashboard.html', context)

def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products':products})

def customer(request,pk):
    customer = Customer.objects.get(id=pk)
    
    orders = customer.order_set.all() # We query all the orders
    customer_total = orders.count()
    
    myFilter = OrderFilter(request.GET, queryset=orders) # Throw them in this filter and based on what
    # the request data is, we're going to filter this data.
    orders = myFilter.qs # We rebuild the variable with the filtered down data.
    
    context = {'customer':customer,'orders':orders,'customer_total':customer_total,'myFilter':myFilter}
    return render(request, 'accounts/customer.html', context)

def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product','status'), extra=10) # We give it the Parent Model, Child Model and fields we want to allow for the child object 
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    # form = OrderForm(initial={'customer':customer}) # With initial, we make sure the customer field's already filled when creating a new order from the customer profile.
    
    if request.method == 'POST':
        formset = OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save() #Saving the form directly into the database.
            return redirect('/')
        
    context={'formset':formset}
    return render(request, 'accounts/order_form.html', context)

def updateOrder(request, pk):
    
    order = Order.objects.get(id = pk) # With both these lines, we can make sure that when we 
    form = OrderForm(instance = order) # go to the form view, we see the pre-filled form
    
    if request.method == 'POST':
        form = OrderForm(request.POST,instance=order) # Without instance=order, it'd create another order on update, instead of updating the same.
        if form.is_valid():
            form.save() #Saving the form directly into the database.
            return redirect('/')

    context = {'form' : form}
    return render(request, 'accounts/order_form.html', context)


def deleteOrder(request,pk):
    
    order = Order.objects.get(id = pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    
    context={'item':order}
    return render(request, 'accounts/delete_form.html', context)
