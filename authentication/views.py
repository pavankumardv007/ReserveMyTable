from os import name
from django.shortcuts import render , redirect
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import * 
from webapp.models import Restaurant

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
     
     if request.method == "POST" :
          username = request.POST['username']
          password = request.POST['password']
          user = auth.authenticate(request,username= username,password = password)
          if user is not None : 
               auth.login(request,user)
               return redirect('/restaurant_list')
          else : 
               messages.error(request,"Invalid Credentials")

     return render(request,'authentication/login_guest.html') 

def login_manager(request) :

     if request.user.is_authenticated : 
          return redirect('/restaurant_list')
     
     if request.method == "POST" :
          username = request.POST['username']
          password = request.POST['password']
          # check if the user is a manager 
          user_exists = User.objects.get(username=username)
          manager = Manager.objects.filter(user_id=user_exists.id)
          if manager : 
            user = auth.authenticate(request,username= username,password = password)
            if user is not None : 
               auth.login(request,user)
               return redirect('/restaurant_list')
            else : 
               messages.error(request,"Invalid Credentials")
          else : 
            messages.error(request,"Please register as manager to Continue ")
          return render(request, 'authentication/login_manager.html')
     return render(request,'authentication/login_manager.html')  

def register_guest(request) :
     
     if request.user.is_authenticated : 
          return redirect('/restaurant_list')

     context = {'username': ''}
     if request.method == "POST" :
          
          username = request.POST['username']
          password1 = request.POST['password1']
          password2 = request.POST['password2']
          context['username'] = username

          if password1 == password2: 
               
               if not username.isalnum():
                  messages.error(request, 'Username must not be blank and must contain only letters and numbers')
               elif len(password1) < 6:
                  messages.error(request, 'Password length must be atleast 6')
               elif User.objects.filter(username=username).exists():
                  messages.error(request, f'The username {username} is already taken')
               else :
                  new_user = User.objects.create_user(username=username,password=password1)
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
          profile = request.POST['profile']
          open_time = request.POST['open_time']
          close_time = request.POST['close_time']
          city = request.POST['city']
          state = request.POST['state']
          address = city + ' ' + state 
     
          context['username']  = username 
          context['email']  = email
          context['res_name']  = res_name
          context['res_email']  = res_email
          context['desc']  = desc
          context['contact']  = contact
          context['profile']  = profile
          context['open_time']  = open_time
          context['colse_time']  = close_time
          context['city']  = city
          context['state']  = state

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
               elif not contact.isnumeric() or contact[0] < '6' or len(contact) != 10:
                  messages.error(request, 'Enter a valid 10 digit phone number')
               else :
                  new_user = User.objects.create_user(username=username,email=email,password=password1)
                  new_user.save()
                  new_res = Restaurant.objects.create(name=res_name,description=desc,address=address,open_time=open_time,close_time=close_time,contact_email=res_email,contact_no=contact,profile_img=profile)
                  new_res.save()
                  new_manager = Manager.objects.create(user=new_user,restaurant=new_res)
                  new_manager.save()
                  messages.success(request, 'Registration successful! Please log in')
                  return redirect('/login_manager')
          else:
               messages.error(request, 'Passwords do not match')
          return render(request, 'authentication/register_manager.html', context=context)
                
     return render(request,'authentication/register_manager.html',context=context)

def logout(request) :
     auth.logout(request)
     messages.error(request,"Logged out succcesfully ! ")
     return redirect('index')

def restaurant_list(request) :
     return render(request,'webapp/restaurant_list.html')  