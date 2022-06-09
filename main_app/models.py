from ast import Pass
import email
from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import uuid
from datetime import datetime
from django.urls import reverse
from django.utils import timezone

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id = models.IntegerField(primary_key=True, default=uuid.uuid4)
    avatar = models.ImageField(default='default-profile-pic.png', upload_to='profile_images')
    bio = models.TextField(max_length=200, blank=True)
    location = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.user.username
    
    # To resize avatars:
    def save(self, *args, **kwargs):
        super().save()
        
        img = Image.open(self.avatar.path)
        
        if img.height > 1080 or img.width > 1080:
            new_img = (1080, 1080)
            img.thumbnail(new_img)
            img.save(self.avatar.path)
            
class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(null=True, blank=True, upload_to='post_images')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.user
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
    
    
class Like(models.Model):
    post_id = models.CharField(max_length=500)
    user = models.CharField(max_length=100)
    
    def __str__(self):
        return self.user