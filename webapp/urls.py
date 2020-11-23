from django.urls import path
from . import  views

urlpatterns = [
    path('',views.index,name="index"),
    path('list',views.res_list,name="list"),
    path('search',views.res_search,name="search"),
    path('restaurants/<int:id>',views.res_detail,name="detail"),
    path('create_reservation/<int:id>',views.create_reservation,name="reservation"),
    path('my_reservations/active',views.my_reservations_active,name="history"),
    path('my_reservations/history',views.my_reservations_history,name="history"),
    path('reservations/active',views.get_reservations_active,name="reservations"),
    path('reservations/completed',views.get_reservations_completed,name="reservations"),
    path('reservation_accept/<int:id>',views.reservation_accept,name="accept"),
    path('reservation_reject/<int:id>',views.reservation_reject,name="reject"),
    path('reservation_delete/<int:id>',views.reservation_delete,name="reservarition_delete"),
    path('reservation_edit/<int:id>',views.reservation_edit,name="reservarition_edit"),
    path('edit_details/<int:id>',views.edit_restaurant_details,name="edit_detail"),
    path('edit_menu/<int:id>',views.edit_restaurant_menu,name="edit_menu"),
    path('edit_profile/<int:id>',views.edit_restaurant_profile,name="edit_profile"),
    path('edit_about/<int:id>',views.edit_restaurant_about,name="edit_about"),
    path('add_relatedimg/<int:id>',views.add_related_image,name="add_related"),
    path('delete_restaurant/<int:id>',views.delete_restaurant,name="delete"),
    path('create_review/<int:id>',views.create_review,name="review"),

]