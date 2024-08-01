from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class MessageBord(models.Model):
    suscribers = models.ManyToManyField(User, related_name='messagebord')

    def __str__(self):
        return str(self.id)
    
class Message(models.Model):
    message = models.ForeignKey(MessageBord, related_name='message',on_delete=models.CASCADE )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
    body = models.CharField(max_length=2000)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created']
        
    def __str__(self):
        return self.author.username