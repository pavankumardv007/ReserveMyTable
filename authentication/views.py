from django.shortcuts import render , redirect
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import connection
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import * 

# Create your views here.

def login_guest(request) :

     if request.user.is_authenticated : 
          return redirect('index')
     
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
     return render(request,'authentication/login_manager.html')  

def register_guest(request) :
     
     if request.user.is_authenticated : 
          return redirect('index')

     context = {'username': ''}
     if request.method == "POST" :
          
          username = request.POST.get('username')
          password1 = request.POST.get('password1')
          password2 = request.POST.get('password2')
          context['username'] = username

          if password1 == password2: 
               
               if not username.isalnum():
                  messages.error(request, 'Username must not be blank and must contain only letters and numbers')
               elif len(password1) < 6:
                  messages.error(request, 'Password length must be atleast 6')
               elif User.objects.filter(username=username).exists():
                  messages.error(request, f'The username {username} is already taken')
               else :
                  print('reached')
                  new_user = User.objects.create_user(username=username,password=password1)
                  new_user.save()
                  new_guest = Guest.objects.create(user=new_user)
                  new_guest.save()
                  messages.success(request, 'Registration successful! Please log in.')
                  return redirect('/login_guest')
          else:
               messages.error(request, 'Passwords do not match')
          return render(request, 'authentication/register_guest.html', context=context)
     return render(request,'authentication/register_guest.html', context=context)

def register_manager(request) :
     return render(request,'authentication/register_manager.html')

def logout(request) :
     auth.logout(request)
     messages.error(request,"Logged out succcesfully ! ")
     return redirect('index')

def restaurant_list(request) :
     return render(request,'webapp/restaurant_list.html')  