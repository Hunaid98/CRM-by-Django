from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from .models import *
from .form import OrderForm, CreateUserForm, CustomerForm
from .filters import OrderFilter
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users, admin_only

# Create your views here.


@unauthenticated_user
def registerpage(request):   
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='customer')
            user.groups.add(group)
            Customer.objects.create(
                user=user,
                name = user.username
            )

            messages.success(request, 'Account was created for '+ username)
            return redirect('login')
                


    context = {'form':form}
    return render(request, 'account/register.html',context)

@unauthenticated_user
def loginpage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR Password is incorrect.')   

    context = {}
    return render(request, 'account/login.html',context)

def logoutuser(request):
    logout(request)

    return redirect('login')

@login_required(login_url= 'login')
@allowed_users(allowed_roles=['customer'])
def userpage(request):
    orders = request.user.customer.order_set.all()

    total_order =orders.count()

    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    print('working:',orders)

     
    context = {'orders':orders,'total_order': total_order, 
    'delivered': delivered , 'pending':pending}
    return render(request, 'account/user.html', context)


@login_required(login_url= 'login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    user = request.user.customer
    form = CustomerForm(instance=user)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES,instance= user)
        if form.is_valid():
            form.save()

    context ={'form':form}
    return render(request, 'account/account_setting.html',context)



@login_required(login_url= 'login')
@admin_only
def home(request):
    ordar = Order.objects.all()
    custo = Customer.objects.all()

    total_customer = custo.count()
    total_order = ordar.count()

    delivered = ordar.filter(status='Delivered').count()
    pending = ordar.filter(status='Pending').count()

    context = {'ordar': ordar, 'custo':custo, 'total_customer':total_customer, 'total_order': total_order, 
    'delivered': delivered , 'pending':pending }
    return render(request,'account/dashboard.html', context)

@login_required(login_url= 'login')
@allowed_users(allowed_roles=['admin'])
def product(request):
    products = Products.objects.all()

    return render(request,'account/products.html',{'products': products }) 

@login_required(login_url= 'login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)
    orders = customer.order_set.all()
    order_count = orders.count()

    myfilter = OrderFilter(request.GET, queryset=orders)
    orders = myfilter.qs

    context = {'customer':customer, 'orders':orders,'order_count':order_count,'myfilter':myfilter}
    return render(request,'account/customer.html', context) 

@login_required(login_url= 'login')
@allowed_users(allowed_roles=['admin'])
def createorder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields= ('product', 'status'), extra = 10)
    customerr = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset= Order.objects.none() ,instance = customerr)
    #Forms = OrderForm(initial={'customer':customerr})
    if request.method == 'POST':
        formset = OrderFormSet(request.POST, instance = customerr)
        if formset.is_valid():

            formset.save() 
            return redirect('/')
    
    context={'formset':formset}
    return render(request, 'account/order_form.html', context)


@login_required(login_url= 'login')
@allowed_users(allowed_roles=['admin'])
def UpdateOrder(request, pk):
    order = Order.objects.get(id=pk)
    Forms = OrderForm(instance = order)
    if request.method == 'POST':
        #print('printing POST :' , request.POST)
        Forms = OrderForm(request.POST, instance = order)
        if Forms.is_valid():
            Forms.save() 
            return redirect('/')


    context={'Forms':Forms}
    return render(request, 'account/order_form.html', context)


@login_required(login_url= 'login')
@allowed_users(allowed_roles=['admin'])
def deleteorder(request, pk):
    order = Order.objects.get(id=pk) 
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {'item':order}
    return render(request, 'account/delete.html',context)