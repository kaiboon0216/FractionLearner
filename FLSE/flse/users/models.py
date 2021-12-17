from django.db import models
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) #make sure no duplicate username 
    image = models.ImageField(default="default.png", upload_to="profile_pics") #specify this is image
    
    def __str__(self):#make data in database readable 
        return f"{self.user.username} Profile"

    def save(self, *args, **kwargs):#saves user profile
        super().save(*args, **kwargs)