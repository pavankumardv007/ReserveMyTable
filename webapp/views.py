from django.shortcuts import render , redirect
from .models import *
from authentication.models import *
from django.contrib import messages

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

def create_reservation(request,id) :
     guest = Guest.objects.get(user_id=request.user.id) 
     restaurant = Restaurant.objects.get(id=id) 
     no_of_people = request.POST['no_of_people']
     date = request.POST['date']
     time = request.POST['time']

     reservation = Reservation.objects.create(guest=guest,restaurant=restaurant,no_of_people=no_of_people,date=date,time=time)
     messages.success(request,'Reservation created Succesfully')
     return redirect('/my_reservations')

def my_reservations(request):
     reservations = Reservation.objects.filter(guest=request.user.id) 
     context = {
          'reservations' : reservations
     }
     return render(request,'webapp/my_reservations.html',context=context)


def get_reservations(request):
     manager = Manager.objects.get(user_id=request.user.id)
     res_id = manager.restaurant_id
     reservations = Reservation.objects.filter(restaurant=res_id) 
     context = {
          'reservations' : reservations
     }
     return render(request,'webapp/reservations.html',context=context)