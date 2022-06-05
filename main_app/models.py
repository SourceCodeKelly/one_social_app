from ast import Pass
import email
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
#class Profile(models.Model):
 #   user = models.ForeignKey(User, on_delete=models.CASCADE)
  #  id_user = models.IntegerField()
   # email = models.CharField(max_length=100)
    #bio = models.TextField(blank=True)
    #profileimg = models.ImageField(upload_to='profile_images', default='default-profile-pic.png')
    #location = models.CharField(max_length=100, blank=True)
    
    #def __str__(self):
     #   return self.user.username