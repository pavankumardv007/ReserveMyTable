from django.urls import path
from . import  views

urlpatterns = [
    path('',views.index,name="index"),
    path('list',views.res_list,name="list"),
    path('restaurants/<int:id>',views.res_detail,name="detail"),
    path('create_reservation/<int:id>',views.create_reservation,name="reservation"),
    path('my_reservations',views.my_reservations,name="history"),
    path('reservations',views.get_reservations,name="reservations"),

]