from ast import Pass
import email
from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    avatar = models.ImageField(default='default-profile-pic.png', upload_to='profile_images')
    bio = models.TextField(max_length=200, blank=True)
    location = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.user.username
    
    # To resize avatars:
    def save(self, *args, **kwargs):
        super().save()
        
        img = Image.open(self.avatar.path)
        
        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)