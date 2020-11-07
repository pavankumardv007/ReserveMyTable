from django.urls import path
from . import  views

urlpatterns = [
    path('',views.index,name="index"),
    path('login_guest',views.login_guest,name="guest_login"),
    path('login_manager',views.login_manager,name="manager_login"),
    path('list',views.res_list,name="list"),
    path('detail',views.res_detail,name="detail"),
    path('guest',views.guest,name="guest"),
]