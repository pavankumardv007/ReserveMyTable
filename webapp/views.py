from django.shortcuts import render
from django.http import HttpResponse
from webapp.models import Restaurant
# Create your views here.

def index(request) :
     return render(request,'webapp/index.html')

def login_guest(request) :
     return render(request,'webapp/login_guest.html') 

def login_manager(request) :
     return render(request,'webapp/login_manager.html')     

def res_list(request):
     res = Restaurant.objects.all()
     print(res)
     return render(request,'webapp/restaurant_list.html',context={ 'res' : res })

def res_detail(request):
     return render(request,'webapp/restaurant.html')

def guest(request):
     return render(request,'webapp/guest_form.html')


