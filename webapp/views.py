from django.shortcuts import render , redirect
from .models import *
from authentication.models import *
from django.contrib import messages
import datetime 
import pytz 
from django.contrib import auth


# Create your views here.

def index(request) :
     return render(request,'webapp/index.html')


def res_list(request):
     res = Restaurant.objects.all()
     print(res)
     return render(request,'webapp/restaurant_list.html',context={ 'res' : res })

def res_detail(request,id):
     context = { 'res' : '', 'manager' : '','about':'','related_img' : ''}
     restaurant = Restaurant.objects.get(id=id)
     manager = Manager.objects.get(restaurant_id=id)
     about = About.objects.get(restaurant_id=id)
     user = User.objects.get(id=manager.user_id)
     images = RelatedImages.objects.filter(restaurant_id=id)
     context['res'] = restaurant
     context['manager'] = user
     context['about'] = about
     context['related_img'] = images
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
          'reservations' : active,
           'is_active' : True 
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
          'reservations' : completed,
           'is_active' : False
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

def reservation_edit(request,id) :
     reservation = Reservation.objects.get(id=id)
     if request.method == 'POST' :
           reservation.date = request.POST['date']
           reservation.time = request.POST['time']
           reservation.no_of_people = request.POST['no_of_people']
           reservation.save()
           messages.success(request,"Reservation details updated succesfully ! ")
           return  redirect('/my_reservations/active')
     else :
          return render(request,'webapp/edit_reservation.html',context={ 'reservation' : reservation })


def reservation_delete(request,id) :
     reservation = Reservation.objects.get(id=id)
     reservation.delete()
     messages.success(request,"reservation deleted Succesfully ! ")
     return redirect('/my_reservations/active')

def edit_restaurant_details(request,id) :
    restaurant = Restaurant.objects.get(id=id)
    if request.method == 'POST' :
           restaurant.name = request.POST['res_name']
           restaurant.description = request.POST['desc']
           restaurant.city = request.POST['city']
           restaurant.state = request.POST['state']
           restaurant.open_time = request.POST['open_time']
           restaurant.close_time = request.POST['close_time']
           restaurant.contact_email = request.POST['res_email']
           restaurant.contact_no = request.POST['contact']
           restaurant.location_url = request.POST['location_url']
           restaurant.save()
           messages.success(request,"Restaurnt details updated succesfully ! ")
           return  redirect(f'/restaurant_edit/{ id }')
    else :
          return render(request,'webapp/edit_details.html',context={ 'res' : restaurant })


def edit_restaurant_menu(request,id) :
     restaurant = Restaurant.objects.get(id=id)
     restaurant.menu_img = request.FILES['menu']
     restaurant.save()
     messages.success(request,"Restaurnt menu updated succesfully ! ")
     return  redirect(f'/restaurant_edit/{ id }')

def edit_restaurant_profile(request,id) :
     restaurant = Restaurant.objects.get(id=id)
     restaurant.profile_img = request.FILES['profile']
     restaurant.save()
     messages.success(request,"Restaurnt profile updated succesfully ! ")
     return  redirect(f'/restaurant_edit/{ id }')

def edit_restaurant_about(request,id) :
    about = About.objects.get(restaurant_id=id)
    if request.method == 'POST' :
           about.cuisine = request.POST['cuisine']
           about.payment_methods = request.POST['payment_methods']
           about.website = request.POST['website']
           about.landmark = request.POST['landmark']
           about.features = request.POST['features']
           about.best_selling_items = request.POST['best_selling']
           about.save()
           messages.success(request,"Restarant About updated succesfully ! ")
           return  redirect(f'/restaurant_edit/{ id }')
    else :
          return render(request,'webapp/edit_about.html',context={ 'res' : about , 'id' : id })

def add_related_image(request,id) :
     restaurant = Restaurant.objects.get(id=id)
     img = request.FILES['related']
     image = RelatedImages.objects.create(image=img,restaurant=restaurant)
     messages.success(request,"Related Image Added succesfully ! ")
     return  redirect(f'/restaurant_edit/{ id }')

def delete_restaurant(request,id) :
    auth.logout(request)
    restaurant = Restaurant.objects.get(id=id)
    manager = Manager.objects.get(restaurant_id=id)
    user = User.objects.get(id=manager.user_id)
    user.delete()
    restaurant.delete()
    messages.success(request,"Restarant deleted succesfully ! ")
    return render(request,'webapp/index.html')
    


