from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):

    username = models.CharField(max_length=50,unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    email = models.EmailField(max_length=300)
    password = models.CharField(max_length=8)


    USERNAME_FIELD = "username"
    REQUIRED_FIELD = ['username','password']
    EMAIL_FIELD = 'email'

class UserProfile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to="images", null=True, blank=True)
    bio = models.TextField() 
    city = models.CharField(max_length=50)
    date_of_birth = models.DateField(auto_now=False, auto_now_add=False,null=True,blank=True)

    def __str__(self):
        return self.bio
    