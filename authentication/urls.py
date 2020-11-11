from django.urls import path
from . import  views

urlpatterns = [
    path('restaurant_list',views.restaurant_list,name="list_view"),
    path('register_guest',views.register_guest,name="guest_register"),
    path('register_manager',views.register_manager,name="manager_register"),
    path('login_guest',views.login_guest,name="guest_login"),
    path('login_manager',views.login_manager,name="manager_login"),
    path('logout',views.logout,name="logout"),
]