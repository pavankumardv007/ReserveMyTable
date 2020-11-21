from django.shortcuts import render , redirect
from .models import *
from authentication.models import *
from django.contrib import messages
import datetime 
import pytz 

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
     return redirect('/my_reservations/active')

def my_reservations_active(request):
     reservations = Reservation.objects.filter(guest=request.user.id) 
     active = []
     date = datetime.date.today()
     time = datetime.datetime.now(pytz.timezone('Asia/Kolkata')).time()
     print(date,time)
     for res in reservations :
          if res.date >  date  :
               res.is_active = True
               active.append(res)
          elif res.date == date and res.time >= time :
               res.is_active = True
               active.append(res)

     context = {
          'reservations' : active
     }
     return render(request,'webapp/my_reservations.html',context=context)

def my_reservations_history(request):
     reservations = Reservation.objects.filter(guest=request.user.id) 
     completed = []
     date = datetime.date.today()
     time = datetime.datetime.now(pytz.timezone('Asia/Kolkata')).time()
     for res in reservations :
          if res.date <  date  :
               res.is_active = False
               completed.append(res)
          elif res.date == date and res.time < time :
               res.is_active = False
               completed.append(res)     

     context = {
          'reservations' : completed
     }
     return render(request,'webapp/my_reservations.html',context=context)


def get_reservations_active(request):
     manager = Manager.objects.get(user_id=request.user.id)
     res_id = manager.restaurant_id
     reservations = Reservation.objects.filter(restaurant=res_id) 
     active = []
     date = datetime.date.today()
     time = datetime.datetime.now(pytz.timezone('Asia/Kolkata')).time()
     for res in reservations :
          if res.date >  date  :
               res.is_active = True
               active.append(res)
          elif res.date == date and res.time >= time :
               res.is_active = True
               active.append(res)

     context = {
          'reservations' : active
     }
     return render(request,'webapp/reservations.html',context=context)

def get_reservations_completed(request):
     manager = Manager.objects.get(user_id=request.user.id)
     res_id = manager.restaurant_id
     reservations = Reservation.objects.filter(restaurant=res_id) 
     completed = []
     date = datetime.date.today()
     time = datetime.datetime.now(pytz.timezone('Asia/Kolkata')).time()
     for res in reservations :
          if res.date <  date  :
               res.is_active = False
               completed.append(res)
          elif res.date == date and res.time < time :
               res.is_active = False
               completed.append(res)  
     
     context = {
          'reservations' : completed
     }
     return render(request,'webapp/reservations.html',context=context)
     

def reservation_accept(request,id) :
     reservation = Reservation.objects.get(id=id)
     reservation.status = True
     reservation.save()
     messages.success(request,"status updated succesfully")
     return redirect('/reservations')

def reservation_reject(request,id) :
     reservation = Reservation.objects.get(id=id)
     reservation.status = False 
     reservation.save()
     messages.success(request,"status updated succesfully")
     return redirect('/reservations')

def edit_restaurant_details(request,id) :
    restaurant = Restaurant.objects.get(id=id)
    if request.method == 'POST' :
         return render(request,'webapp/edit_details.html',context={ 'res' : restaurant })
    else :
         # converting time to 24 hrs format 
     #     o_time = str(restaurant.open_time)
     #     in_time = datetime.datetime.strptime(o_time, "%I:%M %p")
     #     restaurant.open_time = datetime.datetime.strftime(in_time, "%H:%M")
     #     c_time = str(restaurant.close_time)
     #     in_time = datetime.datetime.strptime(c_time, "%I:%M %p")
     #     restaurant.close_time = datetime.datetime.strftime(in_time, "%H:%M")
         return render(request,'webapp/edit_details.html',context={ 'res' : restaurant })
