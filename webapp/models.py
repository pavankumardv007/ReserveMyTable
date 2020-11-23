from django.db import models
from authentication.models import Guest , Manager
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.

# models for Restaurant 

class Restaurant(models.Model) :

    name = models.CharField(max_length=100)
    description = models.TextField()
    city = models.TextField()
    state = models.TextField(default=False)
    open_time = models.TimeField()
    close_time = models.TimeField()
    contact_email = models.EmailField()
    contact_no = PhoneNumberField()
    rating = models.FloatField(default=0)
    profile_img = models.FileField()
    menu_img = models.FileField(default=False)
    location_url = models.TextField(default=False)

    def __str__(self) :
        return self.name

# Representing about section of Restaurants 

class About(models.Model) :
    
    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE)
    payment_methods = models.TextField(default=False)
    cuisine = models.TextField(default=False)
    features = models.TextField(default=False)
    landmark = models.TextField(default=False)
    website = models.TextField(default=False)
    best_selling_items = models.TextField(default=False)

    def __str__(self) :
        return self.name


# Representing user reviews for a restaurant 

class Reviews(models.Model) :

    comment = models.TextField()
    user = models.ForeignKey(Guest,on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE)
    time_stamp =  models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

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
   no_of_people = models.IntegerField(default=1)
   date = models.DateField()
   time = models.TimeField()
   booked_date= models.DateTimeField(auto_now_add=True)
   status = models.BooleanField(default=False)

   def __str__ (self) :
          return f'{self.restaurant.name} {self.guest.username}'

