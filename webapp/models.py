from django.db import models
from authentication.models import Guest , Manager
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.

# models for Restaurant 

class Restaurant(models.Model) :

    name = models.CharField(max_length=100)
    description = models.TextField()
    address = models.TextField()
    open_time = models.TimeField()
    close_time = models.TimeField()
    contact_email = models.EmailField()
    contact_no = PhoneNumberField()
    rating = models.FloatField(default=0)
    profile_img = models.ImageField()

    def __str__(self) :
        return self.name


# Representing restaurant's Menu items         

class MenuItems(models.Model) :

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField(default=0)
    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE)

    def __str__(self) :
        return f'{ self.restaurant } - {self.name}'


# Representing resturants Table's 

class Table(models.Model) :

    seats_no = models.IntegerField()
    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE)
    is_free = models.BooleanField()

    def __str__ (self) :
        return f'{self.restaurant} - {self.seats_no}'


# Representing user reviews for a restaurant 

class Reviews(models.Model) :

    comment = models.TextField()
    user = models.ForeignKey(Guest,on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE)
    time_stamp =  models.DateTimeField(auto_now_add=True)

    def __str__ (self) :
          return f'{self.user.username} {self.restaurant.name}'

# Representing related images of a restaurant 

class RelatedImages(models.Model) :

    image = models.ImageField()
    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE)
    
    def __str__ (self) :
          return f'{self.restaurant} {self.id}'

# Representing reservation of user for a table in restaurant 

class Reservation(models.Model) :

   guest = models.ForeignKey(Guest,on_delete=models.CASCADE)
   restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE)
   table = models.ForeignKey(Table,on_delete=models.CASCADE)
   date = models.DateField()
   start_time = models.TimeField()
   end_time = models.TimeField()
   booked_date= models.DateTimeField(auto_now_add=True)

   def __str__ (self) :
          return f'{self.restaurant.name} {self.guest.username}'
 
 # to be updated 
   def is_active(self) :
       return self 
