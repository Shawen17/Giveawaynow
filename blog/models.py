from django.db import models
from django.contrib.auth.models import User,update_last_login
from django.contrib.auth.signals import user_logged_in



def update_first_login(sender,user,**kwargs):
    if user.last_login is None:
        kwargs['request'].session['first_login']=True
    update_last_login(sender,user,**kwargs)

user_logged_in.disconnect(update_last_login)
user_logged_in.connect(update_first_login)



class Blog(models.Model):
    title=models.CharField(max_length=100,unique=True)
    date=models.DateField(auto_now=True)
    image=models.ImageField(upload_to='givers/images',default='car1.jpg')
    description=models.CharField(max_length=200)
    story=models.TextField()
    genre=models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Comment(models.Model):
    #user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='comments')
    post=models.ForeignKey(Blog,on_delete=models.CASCADE,related_name='comments')
    email = models.EmailField(max_length=100)
    body= models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'comment {self.body} by {self.email}'
