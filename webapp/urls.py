from django.urls import path
from . import  views

urlpatterns = [
    path('',views.index,name="index"),
    path('list',views.res_list,name="list"),
    path('restaurants/<int:id>',views.res_detail,name="detail"),
    path('guest',views.guest,name="guest"),
]