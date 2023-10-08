from django.db import models
from users.models import User
# Create your models here.

class Thought(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=None,blank=True,null=True)
    shared_with = models.ManyToManyField(User,related_name="thoughts",null=True,blank=True)

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    thoughts = models.ForeignKey(Thought, on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return self.text
    

