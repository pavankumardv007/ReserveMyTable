from django.shortcuts import render

# Create your views here.

def login_guest(request) :
     return render(request,'authentication/login_guest.html') 

def login_manager(request) :
     return render(request,'authentication/login_manager.html')  

def register_guest(request) :
     return render(request,'authentication/register_guest.html') 

def register_manager(request) :
     return render(request,'authentication/register_manager.html')  