from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from authentication.models import *
# Create your views here.

def index(request) :
     return render(request,'webapp/index.html')

   

def res_list(request):
     res = Restaurant.objects.all()
     print(res)
     return render(request,'webapp/restaurant_list.html',context={ 'res' : res })

def res_detail(request,id):
     context = { 'res' : '', 'manager' : ''}
     restaurant = Restaurant.objects.get(id=id)
     manager = Manager.objects.get(restaurant_id=id)
     user = User.objects.get(id=manager.user_id)
     context['res'] = restaurant
     context['manager'] = user
     return render(request,'webapp/restaurant.html',context=context)

def guest(request):
     return render(request,'webapp/guest_form.html')


