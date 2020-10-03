from django.shortcuts import render,redirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .models import *
from .forms import *
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only
# Create your views here.


#home view
@login_required(login_url='login')
@admin_only
def home(request):
	#query the orders and customers
	orders = Order.objects.all()
	customers = Customer.objects.all()

	total_customers = customers.count()
	total_orders = orders.count()

	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()
 
	context = {'orders':orders, 'customers':customers, 
		'total_orders':total_orders, 'delivered':delivered,
		'pending':pending}

	return render(request,'accounts/dashboard.html',context)

#products view
@login_required(login_url='login')
def products(request):
	products = Product.objects.all()
	return render(request,'accounts/products.html', {'products':products})

#login page
@unauthenticated_user
def loginPage(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request, username=username, password=password)
		
		if user is not None:
			login(request,user)
			return redirect('home')
			return render(request, 'accounts/login.html', context)

		else:
			messages.info(request, 'Incorrect Username OR Password ')

	context = {}
	return render(request, 'accounts/login.html', context)


#registration page
@unauthenticated_user
def registerPage(request):
	form = CreateUserForm()

	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()

			username = form.cleaned_data.get('username')

			
			messages.success(request, 'Account was created for ' + username)
			return redirect('login')

	context = {'form':form}
	return render(request, 'accounts/registration.html', context)

#logout the user
def logoutUser(request):
	logout(request)
	return redirect('login')


#customers view
@login_required(login_url='login')
def customers(request, pk):
	customer = Customer.objects.get(id=pk)
	orders = customer.order_set.all()

	orders_count = orders.count()

	myFilter = OrderFilter(request.GET, queryset=orders)
	orders = myFilter.qs
	context = {'customer':customer, 'orders':orders, 'orders_count':orders_count, 'myFilter':myFilter}
	return render(request, 'accounts/customers.html',context)

@login_required(login_url='login')
def createOrder(request):
	form = OrderForm()
	context = {'form':form}

	if request.method == 'POST':
		form = OrderForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')
	
	return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
def updateOrder(request, pk):

	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)

	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')


	context = {'form':form}
	return render(request,'accounts/order_form.html', context)

@login_required(login_url='login')
def deleteOrder(request,pk):

	order = Order.objects.get(id=pk)

	if request.method == 'POST':
		order.delete()
		return redirect('/')

	context = {'item':order}
	return render(request, 'accounts/delete.html', context)

@login_required
@allowed_users(allowed_roles=['customer'])
def userPage(request):
	orders = request.user.customer.order_set.all()

	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()

	print('ORDERS:', orders)
	context = {'orders':orders, 'customers':customers, 
		'total_orders':total_orders, 'delivered':delivered,
		'pending':pending}
	return render(request, 'accounts/user_page.html', context)


@login_required
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):

	customer = request.user.customer
	form = CustomerForm(instance=customer)

	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES, instance=customer)
		if form.is_valid():
			form.save
	context = {'form':form}
	return render(request, 'accounts/account_settings.html', context)