from django.shortcuts import render , redirect
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from .models import * 
from webapp.models import *

# Create your views here.

def validateEmail(email):
    try:
        validate_email( email )
        return True
    except ValidationError:
        return False

def login_guest(request) :

     if request.user.is_authenticated : 
          return redirect('/restaurant_list')
     
     context = {'username': ''}
     if request.method == "POST" :
          username = request.POST['username']
          context['username'] = username
          password = request.POST['password']
          user = auth.authenticate(request,username= username,password = password)
          if user is not None : 
               auth.login(request,user)
               return redirect('/restaurants')
          else : 
               messages.error(request,"Invalid Credentials")

     return render(request,'authentication/login_guest.html',context=context) 

def login_manager(request) :

     if request.user.is_authenticated : 
          return redirect('/restaurant_list')
     
     context = {'username': ''}
     if request.method == "POST" :
          username = request.POST['username']
          context['username'] = username
          password = request.POST['password']
          user = auth.authenticate(request,username= username,password = password)
          if user is not None  :
            user_exists = User.objects.get(username=username)
            manager = Manager.objects.get(user_id=user_exists.id) 
            if manager : 
               auth.login(request,user)
               res_id = manager.restaurant_id
               return redirect(f'/restaurant_edit/{res_id}')
            else : 
               messages.error(request,"Please register as manager to Continue")
          else : 
            messages.error(request,"Invalid Credentials")
          return render(request, 'authentication/login_manager.html',context=context)
     return render(request,'authentication/login_manager.html',context=context)  

def register_guest(request) :
     
     if request.user.is_authenticated : 
          return redirect('/restaurant_list')

     context = {'username': '' , 'email' : ''}
     if request.method == "POST" :
          
          username = request.POST['username']
          email = request.POST['email']
          password1 = request.POST['password1']
          password2 = request.POST['password2']
          context['username'] = username
          context['email'] = email

          if password1 == password2: 
               
               if not username.isalnum():
                  messages.error(request, 'Username must not be blank and must contain only letters and numbers')
               elif len(password1) < 6:
                  messages.error(request, 'Password length must be atleast 6')
               elif User.objects.filter(username=username).exists():
                  messages.error(request, f'The username {username} is already taken')
               elif not validateEmail(email):
                  messages.error(request, f'The email { email } is not valid')
               elif User.objects.filter(email=email).exists():
                  messages.error(request, f'The email {email} is already taken')
               else :
                  new_user = User.objects.create_user(username=username,password=password1,email=email)
                  new_user.save()
                  new_guest = Guest.objects.create(user=new_user)
                  new_guest.save()
                  messages.success(request, 'Registration successful! Please log in')
                  return redirect('/login_guest')
          else:
               messages.error(request, 'Passwords do not match')
          return render(request, 'authentication/register_guest.html', context=context)
     return render(request,'authentication/register_guest.html', context=context)

def register_manager(request) :

     if request.user.is_authenticated : 
          return redirect('/restaurant_list')

     context = {'username': '','email' :'','res_name':'','res_email':'','desc':'','contact':'','profile':'','open_time':'','close_time':'','city':'','state':''}
     if request.method == "POST" :
          username = request.POST['username']
          email = request.POST['email']
          password1 = request.POST['password1']
          password2 = request.POST['password2']
          res_name = request.POST['res_name']
          res_email = request.POST['res_email']
          desc = request.POST['desc']
          contact = request.POST['contact']
          profile = request.FILES['profile']
          open_time = request.POST['open_time']
          close_time = request.POST['close_time']
          city = request.POST['city']
          state = request.POST['state']
          location_url = request.POST['location_url']
          # handel error for state 
          context['username']  = username 
          context['email']  = email
          context['res_name']  = res_name
          context['res_email']  = res_email
          context['desc']  = desc
          context['contact']  = contact
          context['profile']  = profile
          context['open_time']  = open_time
          context['close_time']  = close_time
          context['city']  = city
          context['state']  = state
          context['location_url']  = location_url

          if password1 == password2: 
               
               if not username.isalnum():
                  messages.error(request, 'Username must not be blank and must contain only letters and numbers')
               elif len(password1) < 6:
                  messages.error(request, 'Password length must be atleast 6')
               elif len(location_url) <= 2:
                  messages.error(request, 'Please provide the link of google map location of the restaurant')
               elif User.objects.filter(username=username).exists():
                  messages.error(request, f'The username {username} is already taken')
               elif not validateEmail(email):
                  messages.error(request, f'The email { email } is not valid')
               elif User.objects.filter(email=email).exists():
                  messages.error(request, f'The email {email} is already taken')
               elif not contact.isnumeric() or contact[0] < '6' or len(contact) != 10:
                  messages.error(request, 'Enter a valid 10 digit phone number')
               else :
                  new_user = User.objects.create_user(username=username,email=email,password=password1,is_staff=True)
                  new_user.save()
                  new_res = Restaurant.objects.create(name=res_name,description=desc,state=state,city=city,open_time=open_time,close_time=close_time,contact_email=res_email,contact_no=contact,profile_img=profile,location_url=location_url)
                  new_res.save()
                  new_manager = Manager.objects.create(user=new_user,restaurant=new_res)
                  res_about = About.objects.create(restaurant=new_res,cuisine='',payment_methods='', features='',landmark='',website='', best_selling_items='')
                  res_about.save()
                  new_manager.save()
                  messages.success(request, 'Registration successful! Please log in')
                  return redirect('/login_manager')
          else:
               messages.error(request, 'Passwords do not match')
          return render(request, 'authentication/register_manager.html', context=context)
                
     return render(request,'authentication/register_manager.html',context=context)

def logout(request) :
     auth.logout(request)
     messages.success(request,"Logged out succcesfully ! ")
     return redirect('index')

def restaurant_list(request) :
     restaurants = Restaurant.objects.all()
     print(restaurants)
     context = { 'restaurants' : restaurants }  
     return render(request,'webapp/restaurant_list.html',context=context)  

@login_required
def restaurant_edit(request,id) :
     
     restaurant = Restaurant.objects.get(id=id)
     manager = Manager.objects.get(restaurant_id=id)
     user = User.objects.get(id=manager.user_id)
     about = About.objects.get(restaurant_id=id)
     images = RelatedImages.objects.filter(restaurant_id=id)
     reviews = Reviews.objects.filter(restaurant_id=restaurant)
     context = {'res' :  restaurant,'manager' : user , 'about' : about, 'related_img' : images}
     ones = 0 ; tows = 0  ; threes = 0 ; fours = 0 ; fives = 0 
     for review in reviews : 
          rating = review.rating 
          if rating == 1 :
             ones += 1 
          elif rating == 2 :
             tows += 1 
          elif rating == 3 :
             threes +=1 
          elif rating ==4 :
               fours +=1 
          else : 
               fives += 1 
     if reviews  :
        total = len(reviews)
        context['onesper'] = (ones/total)*100
        context['towsper']  = (tows/total)*100
        context['threesper'] = (threes/total)*100
        context['foursper'] = (fours/total)*100
        context['fivesper'] = (fives/total)*100
     context['ones'] = ones 
     context['tows'] = tows 
     context['threes'] = threes 
     context['fours'] = fours 
     context['fives'] = fives
     context['reviews'] = reviews
     s = 's'
     n = 's'
     for i in range(int(restaurant.rating)-1) : 
          s += 's' 
     for i in range(5-int(restaurant.rating)-1) : 
          n += 's'
     context['s'] = s 
     context['n'] = n 
     return render(request,'webapp/restaurant_edit.html', context=context)  

@login_required
def reset_password (request) : 
     user = User.objects.get(username=request.POST['username'])
     user.set_password('new password')
     user.save()
     return redirect('/restaurants')